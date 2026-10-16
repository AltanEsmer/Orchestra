import datetime
import json
import os
import platform
import resource
import subprocess
import sys
import time
import warnings
from pathlib import Path

import sklearn
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.pipeline import Pipeline

from orchestra.data import LABELS, file_sha256, read_jsonl

MODEL_SEED = 42
SCORE_TOLERANCE = 1e-10
RUN_FILES = (
    "config.json",
    "provenance.json",
    "outcomes.json",
    "predictions.jsonl",
    "metrics.json",
    "confusion.json",
    "warnings.json",
    "timing.json",
)
THREAD_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")


def tfidf():
    return TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b\w+\b",
        stop_words=None,
        min_df=1,
        max_df=1.0,
        max_features=10000,
        ngram_range=(1, 1),
        norm="l2",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False,
    )


def build_b0(C, max_iter):
    # The dummy never reads X. It shares the TF-IDF step only so every family
    # is a (vectorizer, classifier) pipeline with the same fit/predict calls.
    return Pipeline(
        [("vec", tfidf()), ("clf", DummyClassifier(strategy="most_frequent"))]
    )


def build_l2(C, max_iter):
    clf = LogisticRegression(
        C=C,
        solver="lbfgs",
        l1_ratio=0.0,  # L2 penalty; `penalty` is deprecated in scikit-learn 1.9.1
        tol=1e-4,
        max_iter=max_iter or 100,
        fit_intercept=True,
        class_weight=None,
        random_state=MODEL_SEED,
    )
    return Pipeline([("vec", tfidf()), ("clf", clf)])


# One entry per family. retry_max_iter is the single bounded convergence retry
# applied to the whole family; None means the family has no iteration limit.
FAMILIES = {
    "B0": {"build": build_b0, "retry_max_iter": None, "score": "probability"},
    "L2": {"build": build_l2, "retry_max_iter": 1000, "score": "probability"},
}


def configuration_id(entry):
    if "C" in entry:
        return f"{entry['family']}-C{entry['C']:g}"
    return entry["family"]


def resolve_configurations(entries):
    resolved, seen = [], set()
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("family") not in FAMILIES:
            raise ValueError(f"unknown configuration {entry!r}")
        cid = configuration_id(entry)
        if cid in seen:
            raise ValueError(f"duplicate configuration {cid}")
        seen.add(cid)
        resolved.append({"id": cid, "family": entry["family"], "C": entry.get("C")})
    return resolved


def reorder_scores(pipeline, scores):
    """Return score columns in LABELS order; a class unseen in training scores 0."""
    columns = {label: i for i, label in enumerate(pipeline.classes_)}
    return [
        [float(row[columns[label]]) if label in columns else 0.0 for label in LABELS]
        for row in scores
    ]


def score(pipeline, texts, kind):
    method = (
        pipeline.predict_proba if kind == "probability" else pipeline.decision_function
    )
    return reorder_scores(pipeline, method(texts))


def metrics(y_true, y_pred):
    labels = list(LABELS)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )
    per_class = {
        label: {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1": float(f1[i]),
            "support": int(support[i]),
        }
        for i, label in enumerate(labels)
    }
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": sum(c["f1"] for c in per_class.values()) / len(labels),
        "per_class": per_class,
        "never_predicted": [label for label in labels if label not in set(y_pred)],
    }


def confusion(y_true, y_pred):
    counts = confusion_matrix(y_true, y_pred, labels=list(LABELS)).tolist()
    normalized = [[n / sum(row) if sum(row) else 0.0 for n in row] for row in counts]
    return {"labels": list(LABELS), "counts": counts, "normalized": normalized}


def fit_predict(entry, train, validation, max_iter=None):
    family = FAMILIES[entry["family"]]
    pipeline = family["build"](entry["C"], max_iter)
    started = time.perf_counter()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        pipeline.fit([r["text"] for r in train], [r["label"] for r in train])
        fit_seconds = time.perf_counter() - started
        texts = [r["text"] for r in validation]
        started = time.perf_counter()
        predictions = [str(p) for p in pipeline.predict(texts)]
        scores = score(pipeline, texts, family["score"])
        predict_seconds = time.perf_counter() - started
    return {
        "pipeline": pipeline,
        "predictions": predictions,
        "scores": scores,
        "fit_seconds": fit_seconds,
        "predict_seconds": predict_seconds,
        "warnings": [
            {"category": w.category.__name__, "message": str(w.message)} for w in caught
        ],
        "converged": not any(
            issubclass(w.category, ConvergenceWarning) for w in caught
        ),
        "max_iter": max_iter,
    }


def json_safe(value):
    return json.loads(json.dumps(value, default=repr))


def estimator_params(pipeline):
    return json_safe(
        {
            "vectorizer": pipeline.named_steps["vec"].get_params(),
            "classifier": pipeline.named_steps["clf"].get_params(),
        }
    )


def load_rows(path, label):
    rows, errors = read_jsonl(path)
    for row in rows:
        if not isinstance(row.get("query_id"), str):
            errors.append(f"{label} row without a string query_id")
        elif not isinstance(row.get("text"), str) or row.get("label") not in LABELS:
            errors.append(f"{label} {row['query_id']}: needs text and a known label")
    ids = [r.get("query_id") for r in rows]
    if len(set(ids)) != len(ids):
        errors.append(f"{label} repeats a query_id")
    if errors:
        raise ValueError("; ".join(errors))
    return sorted(rows, key=lambda r: r["query_id"])


def check_inputs(config, train, validation):
    with open(config["split_manifest"], encoding="utf-8") as file:
        manifest = json.load(file)
    parts = manifest["partitions"]
    for name, rows in (("train", train), ("validation", validation)):
        if [r["query_id"] for r in rows] != sorted(parts[name]):
            raise ValueError(f"{name} query_ids differ from the split manifest")
    # Hash only, never parsed: the dataset file also holds the sealed test rows.
    dataset = Path(config.get("dataset", ""))
    if dataset.is_file() and file_sha256(dataset) != manifest["dataset_sha256"]:
        raise ValueError("dataset hash differs from the split manifest")
    return manifest


def git(*args):
    root = Path(__file__).resolve().parents[2]
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
        )
    except OSError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def uv_version():
    try:
        done = subprocess.run(
            ["uv", "--version"], capture_output=True, text=True, check=False
        )
    except OSError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def peak_rss_bytes():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes, Linux kilobytes.
    return peak if sys.platform == "darwin" else peak * 1024


def now():
    return datetime.datetime.now(datetime.UTC).isoformat()


def provenance(config, manifest, started):
    lock = Path(__file__).resolve().parents[2] / "uv.lock"
    status = git("status", "--porcelain")
    return {
        "git_sha": git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else status != "",
        "python": sys.version,
        "uv": uv_version(),
        "uv_lock_sha256": file_sha256(lock) if lock.is_file() else None,
        "platform": platform.platform(),
        "cpu": platform.processor() or platform.machine(),
        "cpu_count": os.cpu_count(),
        "dataset_sha256": manifest["dataset_sha256"],
        "split_manifest_sha256": file_sha256(config["split_manifest"]),
        "train_sha256": file_sha256(config["train"]),
        "validation_sha256": file_sha256(config["validation"]),
        "seed": config["seed"],
        "model_seed": MODEL_SEED,
        "sklearn": sklearn.__version__,
        "thread_env": {name: os.environ.get(name) for name in THREAD_VARS},
        "started_utc": started,
        "ended_utc": now(),
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def try_fit(entry, train, validation, max_iter, results, errors):
    try:
        results[entry["id"]] = fit_predict(entry, train, validation, max_iter)
    except Exception as error:  # noqa: BLE001 - a failed configuration must not stop the run
        errors[entry["id"]] = f"{type(error).__name__}: {error}"


def run(config, run_id):
    if not run_id or Path(run_id).name != run_id or run_id in (".", ".."):
        raise ValueError(f"run id {run_id!r} must be a plain name")
    started = now()
    configurations = resolve_configurations(config["configurations"])
    train = load_rows(config["train"], "train")
    validation = load_rows(config["validation"], "validation")
    manifest = check_inputs(config, train, validation)
    out = Path(config["results_dir"]) / run_id
    out.mkdir(parents=True)  # refuses an existing run directory

    results = {}
    errors = {}
    attempts = {c["id"]: [] for c in configurations}
    for entry in configurations:
        try_fit(entry, train, validation, None, results, errors)
    # A family that did not converge is refit as a whole at the retry limit.
    for family, spec in FAMILIES.items():
        members = [c for c in configurations if c["family"] == family]
        failed = [
            c
            for c in members
            if c["id"] in results and not results[c["id"]]["converged"]
        ]
        if not failed or not spec["retry_max_iter"]:
            continue
        for entry in members:
            if entry["id"] in results:
                attempts[entry["id"]].append(summarize_attempt(results[entry["id"]]))
                del results[entry["id"]]
                try_fit(
                    entry, train, validation, spec["retry_max_iter"], results, errors
                )

    outcomes, all_metrics, all_confusion, all_warnings, timing = [], {}, {}, {}, {}
    resolved, lines = {}, []
    y_true = [r["label"] for r in validation]
    for entry in configurations:
        cid = entry["id"]
        result = results.get(cid)
        if result is None:
            status = "failed"
        else:
            attempts[cid].append(summarize_attempt(result))
            status = "ok" if result["converged"] else "unresolved_warning"
            resolved[cid] = estimator_params(result["pipeline"])
            all_metrics[cid] = metrics(y_true, result["predictions"])
            all_confusion[cid] = confusion(y_true, result["predictions"])
            all_warnings[cid] = result["warnings"]
            timing[cid] = {
                "fit_seconds": result["fit_seconds"],
                "predict_seconds": result["predict_seconds"],
            }
            kind = FAMILIES[entry["family"]]["score"]
            for row, prediction, scores in zip(
                validation, result["predictions"], result["scores"]
            ):
                lines.append(
                    json.dumps(
                        {
                            "configuration": cid,
                            "query_id": row["query_id"],
                            "label": row["label"],
                            "prediction": prediction,
                            "scores": scores,
                            "score_type": kind,
                        }
                    )
                    + "\n"
                )
        outcomes.append(
            {
                "id": cid,
                "status": status,
                "attempts": attempts[cid],
                "error": errors.get(cid),
            }
        )

    write_json(
        out / "config.json",
        {
            "config": config,
            "class_order": list(LABELS),
            "configurations": configurations,
            "resolved_params": resolved,
        },
    )
    write_json(
        out / "provenance.json",
        {"run_id": run_id, **provenance(config, manifest, started)},
    )
    write_json(out / "outcomes.json", outcomes)
    (out / "predictions.jsonl").write_text("".join(lines), encoding="utf-8")
    write_json(out / "metrics.json", all_metrics)
    write_json(out / "confusion.json", all_confusion)
    write_json(out / "warnings.json", all_warnings)
    write_json(
        out / "timing.json",
        {"peak_rss_bytes": peak_rss_bytes(), "configurations": timing},
    )
    # The manifest is written last, so its absence marks a partial run.
    write_json(
        out / "manifest.json",
        {
            "run_id": run_id,
            "complete": True,
            "files": {name: file_sha256(out / name) for name in RUN_FILES},
        },
    )
    return out, outcomes


def summarize_attempt(result):
    return {
        "max_iter": result["max_iter"],
        "converged": result["converged"],
        "warnings": result["warnings"],
    }


def load_run(directory):
    """Return (run dict, problems). Problems cover missing, partial, or altered files."""
    directory = Path(directory)
    try:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, [f"{directory}: no readable manifest.json (partial run)"]
    problems = []
    if manifest.get("complete") is not True:
        problems.append(f"{directory}: manifest is not marked complete")
    files = manifest.get("files", {})
    for name in RUN_FILES:
        path = directory / name
        if name not in files or not path.is_file():
            problems.append(f"{directory}: {name} missing")
        elif file_sha256(path) != files[name]:
            problems.append(f"{directory}: {name} does not match its manifest hash")
    if problems:
        return None, problems
    run = {}
    for name in RUN_FILES:
        text = (directory / name).read_text(encoding="utf-8")
        if name.endswith(".jsonl"):
            run[name] = [json.loads(line) for line in text.splitlines()]
        else:
            run[name] = json.loads(text)
    return run, []


def compare(left_dir, right_dir):
    left, problems = load_run(left_dir)
    right, more = load_run(right_dir)
    problems += more
    if problems:
        return problems
    diffs = []
    for key in ("config.json", "outcomes.json", "metrics.json", "confusion.json"):
        if left[key] != right[key]:
            diffs.append(f"{key} differs")
    for key in (
        "dataset_sha256",
        "split_manifest_sha256",
        "train_sha256",
        "validation_sha256",
    ):
        a, b = left["provenance.json"][key], right["provenance.json"][key]
        if a != b:
            diffs.append(f"provenance {key} differs")
    a, b = left["predictions.jsonl"], right["predictions.jsonl"]
    if len(a) != len(b):
        diffs.append(f"predictions.jsonl has {len(a)} vs {len(b)} rows")
    for number, (x, y) in enumerate(zip(a, b), start=1):
        rest_x = {k: v for k, v in x.items() if k != "scores"}
        rest_y = {k: v for k, v in y.items() if k != "scores"}
        if rest_x != rest_y:
            diffs.append(f"predictions.jsonl row {number}: {rest_x} vs {rest_y}")
        elif len(x["scores"]) != len(y["scores"]) or any(
            abs(p - q) > SCORE_TOLERANCE for p, q in zip(x["scores"], y["scores"])
        ):
            diffs.append(f"predictions.jsonl row {number}: scores differ beyond 1e-10")
    return diffs
