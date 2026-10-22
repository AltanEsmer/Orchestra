import json
import unittest
from unittest import mock

from test_experiment import RunTestCase

from orchestra import experiment, figures
from orchestra.data import LABELS, file_sha256


class FigureTest(RunTestCase):
    def setUp(self):
        super().setUp()
        config = self.config()
        config["configurations"] = [
            {"family": "B0"},
            {"family": "B1"},
            *(
                {"family": family, "C": c}
                for family in ("L1", "L2", "S1", "L3")
                for c in (0.1, 1, 10)
            ),
        ]
        self.run, _ = experiment.run(config, "figures")
        self.selection = self.root / "selection.json"
        self.selection.write_text(json.dumps(experiment.select(self.run)))

    def render(self, **kwargs):
        return figures.render(
            self.run,
            self.selection,
            self.config()["train"],
            self.config()["validation"],
            self.root / "plots",
            **kwargs,
        )

    def test_exports_traceable_fixture_values_without_opening_sealed_rows(self):
        (self.root / "sealed/test.jsonl").unlink()
        with mock.patch.object(
            experiment, "fit_predict", side_effect=AssertionError("must not fit")
        ):
            out = self.render(fixture=True)
        data = json.loads((out / "plot-data.json").read_text())
        self.assertEqual(
            sum(data["class_balance"]["train"]),
            len(self.manifest["partitions"]["train"]),
        )
        self.assertEqual(data["class_order"], list(LABELS))
        self.assertEqual(len(data["macro_f1"]), 14)
        provenance = json.loads((out / "provenance.json").read_text())
        self.assertTrue(provenance["fixture"])
        self.assertEqual(
            provenance["sources"]["selection.json"], file_sha256(self.selection)
        )
        for path in out.glob("*.svg"):
            self.assertIn("ARTIFICIAL FIXTURE", path.read_text())
        self.assertGreater(len(list(out.glob("*.png"))), 5)
        with self.assertRaises(FileExistsError):
            self.render(fixture=True)

    def test_confidence_lineage_and_reliability_values_are_preserved(self):
        directory = self.root / "confidence"
        directory.mkdir()
        payloads = {
            "config.json": {
                "fixture": True,
                "hashes": {
                    str(self.run.resolve() / "manifest.json"): file_sha256(
                        self.run / "manifest.json"
                    ),
                    str(self.selection.resolve()): file_sha256(self.selection),
                },
            },
            "reliability.json": {
                "raw": [
                    {
                        "lower": 0.8,
                        "upper": 1.0,
                        "count": 4,
                        "mean_confidence": 0.9,
                        "accuracy": 0.75,
                    },
                ]
            },
            "thresholds.json": {
                "rows": [
                    {
                        "threshold": 0.5,
                        "accepted": 4,
                        "coverage": 0.5,
                        "selective_accuracy": 0.75,
                    },
                    {
                        "threshold": 0.9,
                        "accepted": 0,
                        "coverage": 0.0,
                        "selective_accuracy": None,
                    },
                ]
            },
        }
        payloads.update(
            {
                "provenance.json": {},
                "metrics.json": {},
                "outcomes.json": {},
                "calibration-folds.json": [],
            }
        )
        for name, value in payloads.items():
            (directory / name).write_text(json.dumps(value))
        for name in ("predictions.jsonl", "error-review.jsonl"):
            (directory / name).write_text("")
            payloads[name] = None
        (directory / "manifest.json").write_text(
            json.dumps(
                {
                    "complete": True,
                    "files": {name: file_sha256(directory / name) for name in payloads},
                }
            )
        )
        out = self.render(confidence_dir=directory)
        self.assertTrue(json.loads((out / "provenance.json").read_text())["fixture"])
        for path in out.glob("*.svg"):
            self.assertIn("ARTIFICIAL FIXTURE", path.read_text())
        self.assertTrue((out / "confidence-reliability.svg").is_file())
        data = json.loads((out / "plot-data.json").read_text())
        self.assertEqual(
            data["confidence"]["reliability.json"], payloads["reliability.json"]
        )
        (directory / "reliability.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            figures.render(
                self.run,
                self.selection,
                self.config()["train"],
                self.config()["validation"],
                self.root / "tampered-plots",
                confidence_dir=directory,
                fixture=True,
            )
        self.assertFalse((self.root / "tampered-plots").exists())

    def test_unprepared_m3_run_requires_explicit_fixture_designation(self):
        with self.assertRaisesRegex(ValueError, "prepared study evidence"):
            self.render()
        self.assertFalse((self.root / "plots").exists())

    def test_prepared_research_evidence_is_verified_without_opening_dataset(self):
        saved = json.loads((self.run / "config.json").read_text())
        config = saved["config"]
        payloads = {
            "sources": {"fixture": {"license": "artificial test permission"}},
            "review": [],
            "collection_brief": "Artificial evidence-contract test only.",
        }
        evidence = {"ready": True, "dataset_sha256": self.manifest["dataset_sha256"]}
        for key, value in payloads.items():
            path = self.root / (key + ".json")
            path.write_text(json.dumps(value))
            config[key] = str(path)
            evidence[key + "_sha256"] = file_sha256(path)
        config["study_evidence"] = evidence
        config["dataset"] = str(self.root / "does-not-exist.jsonl")
        (self.run / "config.json").write_text(json.dumps(saved))
        manifest = json.loads((self.run / "manifest.json").read_text())
        manifest["files"]["config.json"] = file_sha256(self.run / "config.json")
        (self.run / "manifest.json").write_text(json.dumps(manifest))
        (self.root / "sealed/test.jsonl").unlink()
        out = self.render()
        provenance = json.loads((out / "provenance.json").read_text())
        self.assertFalse(provenance["fixture"])
        self.assertTrue(
            any(key.startswith("study-evidence/") for key in provenance["sources"])
        )
        (self.root / "review.json").write_text("changed evidence")
        with self.assertRaisesRegex(ValueError, "frozen input changed"):
            figures.render(
                self.run,
                self.selection,
                self.config()["train"],
                self.config()["validation"],
                self.root / "changed-evidence-plots",
            )
        self.assertFalse((self.root / "changed-evidence-plots").exists())

    def test_final_fixture_cannot_be_downgraded_by_omitted_flag(self):
        directory = self.root / "final"
        directory.mkdir()
        payloads = {
            "config.json": {
                "fixture": True,
                "config": {
                    "fixture": True,
                    "hashes": {
                        str(self.run.resolve() / "manifest.json"): file_sha256(
                            self.run / "manifest.json"
                        ),
                        str(self.selection.resolve()): file_sha256(self.selection),
                    },
                },
            },
            "provenance.json": {},
            "metrics.json": {},
            "reliability.json": {},
            "thresholds.json": {},
            "confusion.json": {},
            "warnings.json": [],
        }
        for name, value in payloads.items():
            (directory / name).write_text(json.dumps(value))
        for name in ("predictions.jsonl", "error-review.jsonl"):
            (directory / name).write_text("")
            payloads[name] = None
        (directory / "manifest.json").write_text(
            json.dumps(
                {
                    "complete": True,
                    "files": {name: file_sha256(directory / name) for name in payloads},
                }
            )
        )
        out = self.render(final_dir=directory)
        self.assertTrue(json.loads((out / "provenance.json").read_text())["fixture"])
        for path in out.glob("*.svg"):
            self.assertIn("ARTIFICIAL FIXTURE", path.read_text())

    def test_coincident_coverage_labels_are_grouped_inside_axes(self):
        data = {
            "confidence": {
                "thresholds.json": {
                    "rows": [
                        {
                            "threshold": threshold,
                            "accepted": 20,
                            "coverage": 1.0,
                            "selective_accuracy": 1.0,
                        }
                        for threshold in (0.0, 0.5, 0.6, 0.7, 0.8, 0.9)
                    ]
                }
            }
        }
        observed = []

        def capture(fig, name, title):
            annotations = fig.axes[0].texts
            self.assertEqual(len(annotations), 1)
            self.assertEqual(
                annotations[0].get_text(), "t=0, 0.5, 0.6, 0.7, 0.8, 0.9\nn=20"
            )
            self.assertEqual(annotations[0].get_ha(), "right")
            self.assertEqual(annotations[0].get_va(), "top")
            observed.append(name)
            figures.plt.close(fig)

        figures._confidence_figures(data, capture)
        self.assertEqual(observed, ["confidence-coverage"])

    def test_export_is_byte_reproducible(self):
        out = self.render(fixture=True)
        other = figures.render(
            self.run,
            self.selection,
            self.config()["train"],
            self.config()["validation"],
            self.root / "plots-again",
            fixture=True,
        )
        self.assertEqual(
            {p.name: file_sha256(p) for p in out.iterdir()},
            {p.name: file_sha256(p) for p in other.iterdir()},
        )

    def test_tampered_source_and_selection_are_refused_before_output(self):
        selection = json.loads(self.selection.read_text())
        selection["overall"]["chosen"] = "B0"
        selection["valid"] = False
        self.selection.write_text(json.dumps(selection))
        with self.assertRaisesRegex(ValueError, "selection"):
            self.render()
        self.assertFalse((self.root / "plots").exists())

    def test_tampered_run_artifact_is_refused(self):
        (self.run / "metrics.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "manifest hash"):
            self.render()

    def test_changed_validation_input_is_refused(self):
        with open(self.config()["validation"], "a") as file:
            file.write("\n")
        with self.assertRaisesRegex(ValueError, "validation_sha256"):
            self.render()


if __name__ == "__main__":
    unittest.main()
