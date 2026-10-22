import datetime
import json
import math
import os
import platform
import resource
import statistics
import subprocess
import sys
import time
import warnings
from pathlib import Path

import numpy
import scipy
import sklearn
import threadpoolctl
from sklearn.dummy import DummyClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from orchestra.data import LABELS, file_sha256, read_jsonl
from orchestra.splits import check_materialized

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
PATH_KEYS = (
    "review",
    "collection_brief",
    "parent_dataset",
    "parent_manifest",
    "dataset",
    "sources",
    "train",
    "validation",
    "sealed_test",
    "split_manifest",
    "results_dir",
)
THREAD_VARS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
)
REQUIRED_IDS = ["B0", "B1"] + [
    f"{family}-C{c:g}" for family in ("L1", "L2", "S1", "L3") for c in (0.1, 1, 10)
]


TOKEN_SETTINGS = {
    "lowercase": True,
    "token_pattern": r"(?u)\b\w+\b",
    "stop_words": None,
    "min_df": 1,
    "max_df": 1.0,
    "max_features": 10000,
}
LATENCY_REPETITIONS = 30


def counts():
    return CountVectorizer(**TOKEN_SETTINGS, ngram_range=(1, 1))


def tfidf(ngram_range=(1, 1)):
    return TfidfVectorizer(
        **TOKEN_SETTINGS,
        ngram_range=ngram_range,
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


def build_b1(C, max_iter):
    clf = MultinomialNB(alpha=1.0, force_alpha=True, fit_prior=True)
    return Pipeline([("vec", counts()), ("clf", clf)])


def logistic(C, max_iter):
    return LogisticRegression(
        C=C,
        solver="lbfgs",
        l1_ratio=0.0,  # L2 penalty; `penalty` is deprecated in scikit-learn 1.9.1
        tol=1e-4,
        max_iter=max_iter or 100,
        fit_intercept=True,
        class_weight=None,
        random_state=MODEL_SEED,
    )


def build_l1(C, max_iter):
    return Pipeline([("vec", counts()), ("clf", logistic(C, max_iter))])


def build_l2(C, max_iter):
    return Pipeline([("vec", tfidf()), ("clf", logistic(C, max_iter))])


def build_l3(C, max_iter):
    return Pipeline([("vec", tfidf((1, 2))), ("clf", logistic(C, max_iter))])


def build_s1(C, max_iter):
    # LinearSVC's default multi_class="ovr" is the one-vs-rest strategy the
    # protocol asks for; it is not deprecated in 1.9.1, so it is left implicit
    # and appears in the exported resolved parameters.
    clf = LinearSVC(
        C=C,
        penalty="l2",
        loss="squared_hinge",
        dual="auto",
        tol=1e-4,
        max_iter=max_iter or 1000,
        fit_intercept=True,
        class_weight=None,
        random_state=MODEL_SEED,
    )
    return Pipeline([("vec", tfidf()), ("clf", clf)])


# One entry per family. retry_max_iter is the single bounded convergence retry
# applied to the whole family; None means the family has no iteration limit.
FAMILIES = {
    "B0": {"build": build_b0, "retry_max_iter": None, "score": "probability"},
    "B1": {"build": build_b1, "retry_max_iter": None, "score": "probability"},
    "L1": {
        "max_iter": 100,
        "build": build_l1,
        "retry_max_iter": 1000,
        "score": "probability",
    },
    "L2": {
        "max_iter": 100,
        "build": build_l2,
        "retry_max_iter": 1000,
        "score": "probability",
    },
    "S1": {
        "max_iter": 1000,
        "build": build_s1,
        "retry_max_iter": 10000,
        "score": "margin",
    },
    "L3": {
        "max_iter": 100,
        "build": build_l3,
        "retry_max_iter": 1000,
        "score": "probability",
    },
}


def configuration_id(entry):
    if "C" in entry:
        return f"{entry['family']}-C{entry['C']:g}"
    return entry["family"]


def resolve_configurations(entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError("configurations must be a non-empty list")
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
        "max_iter": getattr(pipeline.named_steps["clf"], "max_iter", None),
    }


def measure_latency(pipeline, texts):
    """One warm-up predict, then timed repeats over the whole validation batch."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        pipeline.predict(texts)
        times = []
        for _ in range(LATENCY_REPETITIONS):
            started = time.perf_counter()
            pipeline.predict(texts)
            times.append(time.perf_counter() - started)
    times.sort()
    return {
        "median_seconds": statistics.median(times),
        # nearest-rank 95th percentile
        "p95_seconds": times[math.ceil(0.95 * len(times)) - 1],
        "batch_size": len(texts),
        "repetitions": len(times),
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
    problems = check_materialized(manifest, {"train": train, "validation": validation})
    if problems:
        raise ValueError("; ".join(problems))
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


def provenance(config, manifest, started, rows):
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
        # Copied from the split manifest; run never opens the dataset file.
        "manifest_dataset_sha256": manifest["dataset_sha256"],
        "annotation_versions": sorted({r.get("annotation_version") for r in rows}),
        "split_manifest_sha256": file_sha256(config["split_manifest"]),
        "train_sha256": file_sha256(config["train"]),
        "validation_sha256": file_sha256(config["validation"]),
        "seed": config["seed"],
        "model_seed": MODEL_SEED,
        "sklearn": sklearn.__version__,
        "numpy": numpy.__version__,
        "scipy": scipy.__version__,
        "thread_env": {name: os.environ.get(name) for name in THREAD_VARS},
        "threadpools": json_safe(threadpoolctl.threadpool_info()),
        "started_utc": started,
        "ended_utc": now(),
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def try_fit(entry, train, validation, max_iter, results, errors, tried):
    # The limit actually used: the retry limit, else the family's own default.
    tried[entry["id"]] = max_iter or FAMILIES[entry["family"]].get("max_iter")
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
    errors, tried = {}, {}
    attempts = {c["id"]: [] for c in configurations}
    for entry in configurations:
        try_fit(entry, train, validation, None, results, errors, tried)
    # A family that did not converge is refit as a whole at the retry limit.
    for family, spec in FAMILIES.items():
        members = [c for c in configurations if c["family"] == family]
        warned = [
            c
            for c in members
            if c["id"] in results and not results[c["id"]]["converged"]
        ]
        if not warned or not spec["retry_max_iter"]:
            continue
        for entry in members:
            cid = entry["id"]
            if cid in results:
                attempts[cid].append(summarize_attempt(results.pop(cid)))
            else:  # the first attempt raised; keep it, then retry with the family
                attempts[cid].append(
                    {
                        "max_iter": tried[cid],
                        "converged": False,
                        "warnings": [],
                        "error": errors.pop(cid),
                    }
                )
            try_fit(
                entry,
                train,
                validation,
                spec["retry_max_iter"],
                results,
                errors,
                tried,
            )

    outcomes, all_metrics, all_confusion, all_warnings, timing = [], {}, {}, {}, {}
    resolved, lines = {}, []
    y_true = [r["label"] for r in validation]
    for entry in configurations:
        cid = entry["id"]
        result = results.get(cid)
        if result is None:
            status = "failed"
            attempts[cid].append(
                {
                    "max_iter": tried[cid],
                    "converged": False,
                    "warnings": [],
                    "error": errors[cid],
                }
            )
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
                "latency": measure_latency(
                    result["pipeline"], [r["text"] for r in validation]
                ),
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
        {"run_id": run_id, **provenance(config, manifest, started, train + validation)},
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
        "error": None,
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


def comparable_config(run):
    config = run["config.json"]
    kept = {k: v for k, v in config["config"].items() if k not in PATH_KEYS}
    return {**config, "config": kept}


def compare(left_dir, right_dir):
    left, problems = load_run(left_dir)
    right, more = load_run(right_dir)
    problems += more
    if problems:
        return problems
    diffs = []
    if Path(left_dir).resolve() == Path(right_dir).resolve():
        diffs.append("left and right are the same directory")
    if left["provenance.json"]["run_id"] == right["provenance.json"]["run_id"]:
        diffs.append("left and right share a run_id")
    for side, run in (("left", left), ("right", right)):
        bad = [o["id"] for o in run["outcomes.json"] if o["status"] != "ok"]
        if bad:
            diffs.append(f"{side} has configurations that are not ok: {', '.join(bad)}")
        ids = {o["id"] for o in run["outcomes.json"]}
        if not run["predictions.jsonl"]:
            diffs.append(f"{side} has no predictions")
        if {r["configuration"] for r in run["predictions.jsonl"]} != ids:
            diffs.append(f"{side} predictions do not cover its configurations")
        if not all(
            math.isfinite(v) for r in run["predictions.jsonl"] for v in r["scores"]
        ):
            diffs.append(f"{side} has non-finite scores")
    for name in ("outcomes.json", "metrics.json", "confusion.json"):
        if left[name] != right[name]:
            diffs.append(f"{name} differs")
    # Paths may differ (a restored archive); input hashes establish identity.
    left_config, right_config = comparable_config(left), comparable_config(right)
    if left_config != right_config:
        diffs.append("config.json differs")
    for key in (
        "manifest_dataset_sha256",
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


SELECTION_TOLERANCE = 0.01
SIMPLICITY_ORDER = ("B0", "B1", "L1", "L2", "S1", "L3")
SELECTION_RULES = (
    "Per family: candidates are configurations with status ok. The tie set is every "
    "candidate whose validation macro-F1 is within 0.01 (inclusive) of the family best; choose "
    "the smallest C (a family without C has one member). Overall: among family "
    "winners within 0.01 (inclusive) of the best winner, prefer B0, B1, L1, L2, S1, L3 in that "
    "order, then lower median prediction latency, then configuration ID. Any "
    "configuration that is not ok, or a run that is not exactly the 14 required "
    "configurations, makes the selection invalid and nothing is chosen. With one winner "
    "per family the latency and ID keys cannot decide an overall tie; the protocol "
    "declares them anyway."
)


def within_tolerance(score, best):
    # Rounding keeps a gap of exactly 0.01 inside despite float representation.
    return round(score, 12) >= round(best - SELECTION_TOLERANCE, 12)


def select(run_dir):
    """Frozen per-family and overall selection from one run's validation metrics."""
    run, problems = load_run(run_dir)
    if problems:
        raise ValueError("; ".join(problems))
    entries = run["config.json"]["configurations"]
    status = {o["id"]: o["status"] for o in run["outcomes.json"]}
    scores_by_id = {
        e["id"]: run["metrics.json"][e["id"]]["macro_f1"]
        for e in entries
        if status.get(e["id"]) == "ok"
    }
    blocking = [e["id"] for e in entries if e["id"] not in scores_by_id]
    resolved_ids = [e["id"] for e in entries]
    missing = [cid for cid in REQUIRED_IDS if cid not in resolved_ids]
    unexpected = [cid for cid in resolved_ids if cid not in REQUIRED_IDS]
    complete_matrix = not missing and not unexpected
    valid = complete_matrix and not blocking
    c_of = {e["id"]: e["C"] for e in entries}
    latency = {
        cid: t["latency"]["median_seconds"]
        for cid, t in run["timing.json"]["configurations"].items()
    }

    families, winners = {}, {}
    for family in SIMPLICITY_ORDER:
        scores = {
            e["id"]: scores_by_id[e["id"]]
            for e in entries
            if e["family"] == family and e["id"] in scores_by_id
        }
        if not any(e["family"] == family for e in entries):
            continue
        best = max(scores.values(), default=None)
        tie_set = sorted(
            (cid for cid, f in scores.items() if within_tolerance(f, best)),
            key=lambda cid: (c_of[cid] if c_of[cid] is not None else 0, cid),
        )
        chosen = tie_set[0] if valid else None
        if chosen:
            winners[family] = chosen
        families[family] = {"scores": scores, "tie_set": tie_set, "chosen": chosen}

    overall_ties = []
    if winners:
        top = max(scores_by_id[cid] for cid in winners.values())
        overall_ties = sorted(
            (
                cid
                for cid in winners.values()
                if within_tolerance(scores_by_id[cid], top)
            ),
            key=lambda cid: (
                SIMPLICITY_ORDER.index(next(f for f, w in winners.items() if w == cid)),
                latency.get(cid, math.inf),
                cid,
            ),
        )
    provenance_ = run["provenance.json"]
    return {
        "valid": valid,
        "blocking": blocking,
        "complete_matrix": complete_matrix,
        "missing": missing,
        "unexpected": unexpected,
        "rules": {
            "text": SELECTION_RULES,
            "tolerance": SELECTION_TOLERANCE,
            "simplicity_order": list(SIMPLICITY_ORDER),
        },
        "run_id": provenance_["run_id"],
        "run": str(run_dir),
        "hashes": {
            key: provenance_[key]
            for key in (
                "manifest_dataset_sha256",
                "split_manifest_sha256",
                "train_sha256",
                "validation_sha256",
            )
        },
        "configurations": {
            e["id"]: {
                "family": e["family"],
                "C": e["C"],
                "status": status.get(e["id"]),
                "macro_f1": scores_by_id.get(e["id"]),
            }
            for e in entries
        },
        "families": families,
        "overall": {
            "tie_set": overall_ties,
            "chosen": overall_ties[0] if valid and overall_ties else None,
        },
    }


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + " --- |" * len(headers)]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def class_length_tables(rows, name, digest, run_id):
    body = []
    for label in LABELS:
        words = [len(r["text"].split()) for r in rows if r["label"] == label]
        body.append(
            [label, len(words)]
            + [f"{f(words):g}" if words else "-" for f in (min, statistics.median, max)]
        )
    head = (
        f"### {name}\n\nSource: `{name}.jsonl` (sha256 `{digest}`, equal to run "
        f"`{run_id}` provenance). Words are whitespace-separated tokens.\n\n"
    )
    return head + table(["Class", "Queries", "Words min", "median", "max"], body)


def fraction(value):
    return "-" if value is None else f"{value:.4f}"


def report(run_dir, selection_path, train_path, validation_path):
    """Write comparison.md and errors.jsonl from saved files; nothing is fitted."""
    run, problems = load_run(run_dir)
    if problems:
        raise ValueError("; ".join(problems))
    prov = run["provenance.json"]
    run_id = prov["run_id"]
    for path, key in (
        (train_path, "train_sha256"),
        (validation_path, "validation_sha256"),
    ):
        if file_sha256(path) != prov[key]:
            raise ValueError(f"{path} does not match run {run_id} {key}")
    selection = json.loads(Path(selection_path).read_text(encoding="utf-8"))
    expected = select(run_dir)
    if {**selection, "run": None} != {**expected, "run": None}:
        raise ValueError(
            f"{selection_path} does not match the selection of run {run_id}"
        )
    train = load_rows(train_path, "train")
    validation = load_rows(validation_path, "validation")
    texts = {r["query_id"]: r["text"] for r in validation}
    # A sibling of the run directory: results/ is untracked and errors.jsonl holds text.
    out = Path(run_dir).parent / f"{run_id}-report"
    out.mkdir()

    metrics_ = run["metrics.json"]
    timing = run["timing.json"]["configurations"]
    configs = selection["configurations"]
    cite = f"Source: run `{run_id}`"
    flag = "INVALID selection: " if not selection["valid"] else ""
    heading = f"# {flag}Validation comparison for run `{run_id}`\n"
    md = [
        heading,
        (
            f"Validation only. Selection valid: `{selection['valid']}`. "
            f"Dataset sha256 `{prov['manifest_dataset_sha256']}`, split manifest "
            f"sha256 `{prov['split_manifest_sha256']}`.\n"
        ),
    ]
    if selection["blocking"]:
        md.append("Blocking configurations: " + ", ".join(selection["blocking"]) + "\n")
    if selection["missing"] or selection["unexpected"]:
        md.append(
            "Missing configurations: "
            + (", ".join(selection["missing"]) or "none")
            + ". Unexpected: "
            + (", ".join(selection["unexpected"]) or "none")
            + ".\n"
        )

    rows = []
    for cid, info in configs.items():
        m = metrics_.get(cid)
        latency = timing.get(cid, {}).get("latency", {}).get("median_seconds")
        rows.append(
            [
                cid,
                info["status"],
                fraction(m and m["accuracy"]),
                fraction(m and m["macro_f1"]),
                "-" if latency is None else f"{latency:.6f}",
            ]
        )
    md += [
        "## Validation table\n",
        (
            f"{cite}, `outcomes.json`, `metrics.json`, `timing.json`. Latency is "
            "the median seconds to predict the whole validation batch.\n"
        ),
        table(
            ["Configuration", "Status", "Accuracy", "Macro-F1", "Median latency (s)"],
            rows,
        ),
    ]

    md += [
        "## Matched-C comparisons\n",
        f"{cite}, `metrics.json`. Difference is the second family minus the first.\n",
    ]
    for first, second, purpose in (
        ("L1", "L2", "term weighting (counts vs TF-IDF)"),
        ("L2", "S1", "classifier (logistic regression vs linear SVM)"),
        ("L2", "L3", "phrase features (unigrams vs unigrams and bigrams)"),
    ):
        pairs = []
        for cid, info in configs.items():
            if info["family"] != first or info["C"] is None:
                continue
            other = next(
                (
                    o
                    for o, oi in configs.items()
                    if oi["family"] == second and oi["C"] == info["C"]
                ),
                None,
            )
            if other:
                a, b = info["macro_f1"], configs[other]["macro_f1"]
                delta = None if a is None or b is None else b - a
                pairs.append(
                    [
                        f"{info['C']:g}",
                        fraction(a),
                        fraction(b),
                        "-" if delta is None else f"{delta:+.4f}",
                    ]
                )
        md += [
            f"### {first} vs {second}: {purpose}\n",
            table(
                ["C", f"{first} macro-F1", f"{second} macro-F1", "Difference"], pairs
            ),
        ]
    chosen_rows = [
        [fam, f["chosen"] or "-", ", ".join(f["tie_set"]) or "-"]
        for fam, f in selection["families"].items()
    ]
    md += [
        "### Selected configuration per family\n",
        f"{cite}, `selection.json`. Tie set: within 0.01 of the family best.\n",
        table(["Family", "Chosen", "Tie set"], chosen_rows),
        (
            f"Overall choice: `{selection['overall']['chosen']}`; tie set "
            f"{', '.join(selection['overall']['tie_set'])}.\n"
        ),
    ]

    md += [
        "## Class balance and query length\n",
        class_length_tables(train, "train", prov["train_sha256"], run_id),
        class_length_tables(
            validation, "validation", prov["validation_sha256"], run_id
        ),
    ]

    chosen = [f["chosen"] for f in selection["families"].values() if f["chosen"]]
    md.append("## Confusion matrices of selected configurations\n")
    errors, counts = [], {}
    predictions = run["predictions.jsonl"]
    for cid in chosen:
        confusion_ = run["confusion.json"][cid]
        md += [
            f"### {cid}\n",
            f"{cite}, `confusion.json`. Rows are true classes, columns predicted; raw counts.\n",
            table(
                ["true \\ predicted"] + confusion_["labels"],
                [
                    [label] + row
                    for label, row in zip(confusion_["labels"], confusion_["counts"])
                ],
            ),
        ]
        wrong = [
            p
            for p in predictions
            if p["configuration"] == cid and p["label"] != p["prediction"]
        ]
        counts[cid] = len(wrong)
        errors += [
            {
                "configuration": cid,
                "query_id": p["query_id"],
                "label": p["label"],
                "prediction": p["prediction"],
                "text": texts[p["query_id"]],
            }
            for p in wrong
        ]
    errors.sort(key=lambda e: (e["query_id"], e["configuration"]))
    (out / "comparison.md").write_text("\n".join(md), encoding="utf-8")
    (out / "errors.jsonl").write_text(
        "".join(json.dumps(e) + "\n" for e in errors), encoding="utf-8"
    )
    return out, counts, selection
