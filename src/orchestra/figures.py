"""Publication figures derived only from verified saved experiment artifacts."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from orchestra import experiment
from orchestra.data import LABELS, file_sha256

RECIPE_VERSION = 1


def _artifact(directory, scope):
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    if manifest.get("complete") is not True or not manifest.get("files"):
        raise ValueError(f"{directory}: incomplete artifact")
    required = {
        "config.json",
        "provenance.json",
        "metrics.json",
        "reliability.json",
        "thresholds.json",
        "predictions.jsonl",
        "error-review.jsonl",
    }
    required |= (
        {"outcomes.json", "calibration-folds.json"}
        if scope == "confidence"
        else {"confusion.json", "warnings.json"}
    )
    if not required.issubset(manifest["files"]):
        raise ValueError(f"{directory}: incomplete {scope} artifact file set")
    for name, digest in manifest["files"].items():
        path = directory / name
        if Path(name).name != name or not path.is_file() or file_sha256(path) != digest:
            raise ValueError(f"{directory}: artifact hash mismatch: {name}")
    return {
        name: json.loads((directory / name).read_text())
        for name in manifest["files"]
        if name.endswith(".json")
    }


def render(
    run_dir,
    selection_path,
    train_path,
    validation_path,
    out_dir,
    confidence_dir=None,
    final_dir=None,
    fixture=False,
):
    """Export SVG/PNG figures, exact numeric inputs and source hash sidecars."""
    out = Path(out_dir)
    if out.exists():
        raise FileExistsError(out)
    run, problems = experiment.load_run(run_dir)
    if problems:
        raise ValueError("; ".join(problems))
    selection = json.loads(Path(selection_path).read_text())
    expected = experiment.select(run_dir)
    if {**selection, "run": None} != {**expected, "run": None} or not selection[
        "valid"
    ]:
        raise ValueError("selection does not match a valid complete comparison run")
    prov = run["provenance.json"]
    for path, key in (
        (train_path, "train_sha256"),
        (validation_path, "validation_sha256"),
    ):
        if file_sha256(path) != prov[key]:
            raise ValueError(f"{path} differs from {key}")
    train = experiment.load_rows(train_path, "train")
    validation = experiment.load_rows(validation_path, "validation")
    data = {
        "class_order": list(LABELS),
        "class_balance": {
            name: [sum(r["label"] == label for r in rows) for label in LABELS]
            for name, rows in (("train", train), ("validation", validation))
        },
        "word_lengths": {
            name: [len(r["text"].split()) for r in rows]
            for name, rows in (("train", train), ("validation", validation))
        },
        "macro_f1": {
            cid: metric["macro_f1"] for cid, metric in run["metrics.json"].items()
        },
        "selected_confusion": {
            info["chosen"]: run["confusion.json"][info["chosen"]]
            for info in selection["families"].values()
        },
        "matched_c": {},
    }
    for first, second in (("L1", "L2"), ("L2", "S1"), ("L2", "L3")):
        data["matched_c"][f"{first}-{second}"] = {
            family: [data["macro_f1"][f"{family}-C{c:g}"] for c in (0.1, 1, 10)]
            for family in (first, second)
        }
    sources = {
        "run/manifest.json": file_sha256(Path(run_dir) / "manifest.json"),
        "selection.json": file_sha256(selection_path),
        "train.jsonl": file_sha256(train_path),
        "validation.jsonl": file_sha256(validation_path),
    }
    for name, directory in (("confidence", confidence_dir), ("final", final_dir)):
        if directory is not None:
            artifact = _artifact(directory, name)
            config = artifact.get("config.json", {})
            artifact_fixture = config.get("fixture") is True
            if name == "final":
                config = config.get("config", {})
                artifact_fixture |= config.get("fixture") is True
            hashes = config.get("hashes", {})
            if (
                hashes.get(str(Path(run_dir).resolve() / "manifest.json"))
                != sources["run/manifest.json"]
            ):
                raise ValueError(f"{name} artifacts do not belong to this run")
            if (
                hashes.get(str(Path(selection_path).resolve()))
                != sources["selection.json"]
            ):
                raise ValueError(f"{name} artifacts do not belong to this selection")
            fixture = bool(fixture or artifact_fixture)
            data[name] = {
                key: artifact[key]
                for key in (
                    "metrics.json",
                    "confusion.json",
                    "reliability.json",
                    "thresholds.json",
                )
                if key in artifact
            }
            sources[f"{name}/manifest.json"] = file_sha256(
                Path(directory) / "manifest.json"
            )
    if not fixture:
        from orchestra.confidence import _research_evidence

        config = run["config.json"]["config"]
        split_path = config["split_manifest"]
        if file_sha256(split_path) != prov["split_manifest_sha256"]:
            raise ValueError("split manifest differs from source run")
        manifest = json.loads(Path(split_path).read_text())
        evidence_hashes = _research_evidence(config, manifest)
        sources.update(
            {
                f"study-evidence/{path}": digest
                for path, digest in evidence_hashes.items()
            }
        )
    provenance = {
        "recipe_version": RECIPE_VERSION,
        "fixture": fixture,
        "run_id": prov["run_id"],
        "configuration_ids": list(data["macro_f1"]),
        "split_manifest_sha256": prov["split_manifest_sha256"],
        "sources": sources,
        "matplotlib_version": matplotlib.__version__,
    }
    out.mkdir(parents=True)
    suffix = " — ARTIFICIAL FIXTURE" if fixture else ""
    with matplotlib.rc_context(
        {"svg.hashsalt": "orchestra-figures-v1", "font.size": 10}
    ):

        def save(fig, name, title):
            fig.suptitle(title + suffix, fontsize=12)
            fig.tight_layout(rect=(0, 0, 1, 0.94))
            fig.savefig(out / f"{name}.svg", metadata={"Date": None})
            fig.savefig(
                out / f"{name}.png", dpi=160, metadata={"Software": "Orchestra"}
            )
            plt.close(fig)
            experiment.write_json(out / f"{name}.source.json", provenance)

        labels = [label.replace("_", "\n") for label in LABELS]
        fig, ax = plt.subplots(figsize=(7, 4))
        x = np.arange(len(LABELS))
        for offset, (name, counts) in zip((-0.2, 0.2), data["class_balance"].items()):
            ax.bar(x + offset, counts, 0.4, label=name)
        ax.set(xticks=x, xticklabels=labels, ylabel="Queries")
        ax.legend()
        save(fig, "class-balance", "Visible partition class balance")

        fig, ax = plt.subplots(figsize=(7, 4))
        lengths = data["word_lengths"]
        longest = max(v for values in lengths.values() for v in values)
        bins = np.arange(0, longest + 2)
        for name, values in lengths.items():
            ax.hist(values, bins=bins, histtype="step", linewidth=2, label=name)
        ax.set(xlabel="Whitespace-separated words per query", ylabel="Queries")
        ax.legend()
        save(fig, "word-lengths", "Visible partition query lengths")

        fig, ax = plt.subplots(figsize=(9, 5))
        ids = list(data["macro_f1"])
        ax.barh(ids, [data["macro_f1"][cid] for cid in ids])
        ax.set(xlabel="Validation macro-F1", xlim=(0, 1))
        ax.invert_yaxis()
        save(fig, "validation-comparison", "Fourteen configuration comparison")

        for cid, confusion in data["selected_confusion"].items():
            for kind in ("counts", "normalized"):
                fig, ax = plt.subplots(figsize=(6, 5))
                matrix = confusion[kind]
                im = ax.imshow(
                    matrix,
                    cmap="Blues",
                    vmin=0,
                    vmax=1 if kind == "normalized" else None,
                )
                ax.set(
                    xticks=x,
                    yticks=x,
                    xticklabels=labels,
                    yticklabels=labels,
                    xlabel="Predicted action",
                    ylabel="True action",
                )
                for i in range(4):
                    for j in range(4):
                        ax.text(
                            j,
                            i,
                            f"{matrix[i][j]:.2f}"
                            if kind == "normalized"
                            else str(matrix[i][j]),
                            ha="center",
                            va="center",
                            color="black",
                            bbox={
                                "facecolor": "white",
                                "alpha": 0.65,
                                "edgecolor": "none",
                            },
                        )
                fig.colorbar(
                    im,
                    ax=ax,
                    label="Fraction of true class"
                    if kind == "normalized"
                    else "Queries",
                )
                save(
                    fig,
                    f"confusion-{cid}-{kind}",
                    f"Validation {cid}: confusion {kind}",
                )

        fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
        for ax, (pair, values) in zip(axes, data["matched_c"].items()):
            for family, scores in values.items():
                ax.plot((0.1, 1, 10), scores, marker="o", label=family)
            ax.set(xscale="log", xlabel="C", ylim=(0, 1), title=pair)
            ax.legend()
        axes[0].set_ylabel("Validation macro-F1")
        save(fig, "matched-c", "Matched regularization comparisons")
        if "final" in data:
            final_metrics = data["final"].get("metrics.json", {})
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(
                list(final_metrics), [m["macro_f1"] for m in final_metrics.values()]
            )
            ax.set(xlabel="Final test macro-F1 (frozen systems)", xlim=(0, 1))
            save(
                fig, "final-comparison", "Final test: frozen systems, no new selection"
            )
            for cid, matrix in data["final"].get("confusion.json", {}).items():
                fig, ax = plt.subplots(figsize=(6, 5))
                im = ax.imshow(matrix["counts"], cmap="Blues", vmin=0)
                ax.set(
                    xticks=x,
                    yticks=x,
                    xticklabels=labels,
                    yticklabels=labels,
                    xlabel="Predicted action",
                    ylabel="True action",
                )
                for i in range(4):
                    for j in range(4):
                        ax.text(
                            j,
                            i,
                            str(matrix["counts"][i][j]),
                            ha="center",
                            va="center",
                            bbox={
                                "facecolor": "white",
                                "alpha": 0.65,
                                "edgecolor": "none",
                            },
                        )
                fig.colorbar(im, ax=ax, label="Queries")
                save(
                    fig, f"final-confusion-{cid}", f"Final test {cid}: confusion counts"
                )
        _confidence_figures(data, save)
    experiment.write_json(out / "plot-data.json", data)
    experiment.write_json(out / "provenance.json", provenance)
    experiment.write_json(
        out / "manifest.json",
        {
            "complete": True,
            "files": {
                path.name: file_sha256(path)
                for path in sorted(out.iterdir())
                if path.is_file()
            },
        },
    )
    return out


def _confidence_figures(data, save):
    for scope in ("confidence", "final"):
        if scope not in data:
            continue
        artifact = data[scope]
        reliability = artifact.get("reliability.json", {})
        if reliability:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.plot((0, 1), (0, 1), "--", color="gray", label="Perfect calibration")
            for name, bins in reliability.items():
                if isinstance(bins, dict):
                    bins = bins.get("bins", [])
                nonempty = [b for b in bins if b.get("count", 0)]
                ax.plot(
                    [b["mean_confidence"] for b in nonempty],
                    [b["accuracy"] for b in nonempty],
                    marker="o",
                    label=name,
                )
                for b in nonempty:
                    ax.annotate(str(b["count"]), (b["mean_confidence"], b["accuracy"]))
            ax.set(
                xlabel="Mean top-label confidence",
                ylabel="Top-label accuracy",
                xlim=(0, 1),
                ylim=(0, 1),
            )
            ax.legend()
            save(
                fig,
                f"{scope}-reliability",
                f"{scope.title()} reliability (labels are bin counts)",
            )
        thresholds = artifact.get("thresholds.json", {}).get("rows", [])
        if thresholds:
            fig, ax = plt.subplots(figsize=(6, 4))
            rows = [r for r in thresholds if r["selective_accuracy"] is not None]
            ax.plot(
                [r["coverage"] for r in rows],
                [r["selective_accuracy"] for r in rows],
                marker="o",
            )
            coincident = {}
            for row in rows:
                point = (row["coverage"], row["selective_accuracy"])
                coincident.setdefault(point, []).append(row)
            for (coverage, accuracy), members in coincident.items():
                thresholds_text = ", ".join(f"{row['threshold']:g}" for row in members)
                accepted = ", ".join(
                    str(n) for n in sorted({row["accepted"] for row in members})
                )
                ax.annotate(
                    f"t={thresholds_text}\nn={accepted}",
                    (coverage, accuracy),
                    xytext=(-6 if coverage > 0.5 else 6, -8 if accuracy > 0.8 else 8),
                    textcoords="offset points",
                    ha="right" if coverage > 0.5 else "left",
                    va="top" if accuracy > 0.8 else "bottom",
                    fontsize=8,
                    bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
                )
            ax.set(
                xlabel="Accepted queries / all queries (coverage)",
                ylabel="Correct / accepted queries",
                xlim=(0, 1),
                ylim=(0, 1.05),
            )
            save(
                fig,
                f"{scope}-coverage",
                f"{scope.title()} selective accuracy and coverage",
            )
