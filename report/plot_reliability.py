"""Render the report's reliability panels from the retained numeric sidecar."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    directory = Path(__file__).resolve().parent / "figures"
    source = directory / "test-reliability.source.json"
    provenance = json.loads(source.read_text())
    fig, axes = plt.subplots(1, 3, figsize=(9.1, 2.9), sharex=True, sharey=True)
    names = ("L3-C10", "calibrated", "Jev")
    titles = ("L3-C10 raw", "L3-C10 calibrated", "Jev")
    for ax, name, title in zip(axes, names, titles, strict=True):
        bins = [row for row in provenance["bins"][name] if row["count"]]
        ax.plot([0, 1], [0, 1], "--", color="0.6", linewidth=1)
        ax.plot(
            [row["mean_confidence"] for row in bins],
            [row["accuracy"] for row in bins],
            "o-",
            color="#235d82",
        )
        for row in bins:
            ax.annotate(
                str(row["count"]),
                (row["mean_confidence"], row["accuracy"]),
                xytext=(0, -14 if row["accuracy"] > 0.9 else 7),
                textcoords="offset points",
                ha="center",
                fontsize=9,
            )
        ax.set(
            title=title,
            xlabel="Mean top-label probability",
            xlim=(0, 1),
            ylim=(0, 1.08),
        )
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
    axes[0].set_ylabel("Observed accuracy")
    fig.tight_layout(pad=0.7)
    output = directory / "test-reliability.png"
    fig.savefig(output, dpi=220, metadata={"Software": "Orchestra"})
    plt.close(fig)
    provenance["figure_sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    provenance["renderer_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    provenance["matplotlib_version"] = matplotlib.__version__
    source.write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"PASS: rendered {output.name} from saved reliability bins")


if __name__ == "__main__":
    main()
