import json
import math
import unittest

from orchestra.confidence import probability_metrics, threshold_table
from orchestra.data import LABELS


class ProbabilityTest(unittest.TestCase):
    def test_literal_scores_and_last_bin(self):
        result = probability_metrics(
            [LABELS[0], LABELS[1]], [[1, 0, 0, 0], [0.5, 0.5, 0, 0]]
        )
        self.assertAlmostEqual(result["brier"], 0.25)
        self.assertAlmostEqual(result["log_loss"], -math.log(0.5) / 2)
        self.assertEqual(result["bins"][-1]["count"], 1)
        self.assertEqual(result["bins"][0]["accuracy"], None)

    def test_invalid_probability_arrays(self):
        for values in (
            [[float("nan"), 0, 0, 0]],
            [[1, 1, 0, 0]],
            [[1, 0, 0]],
            [[-1, 1, 1, 0]],
        ):
            with self.subTest(values=values), self.assertRaises(ValueError):
                probability_metrics([LABELS[0]], values)

    def test_sum_tolerance_matches_the_jev_parser_bound(self):
        for drift in (1e-7, 9e-4):
            row = [[0.7 + drift, 0.1, 0.1, 0.1]]
            self.assertIn("brier", probability_metrics([LABELS[0]], row))
        with self.assertRaises(ValueError):
            probability_metrics([LABELS[0]], [[0.7 + 1.1e-3, 0.1, 0.1, 0.1]])

    def test_thresholds_undefined_and_no_qualifier(self):
        result = threshold_table([LABELS[1]], [LABELS[0]], [[0.7, 0.1, 0.1, 0.1]])
        self.assertEqual(result["status"], "no_qualifying_threshold")
        self.assertIsNone(result["chosen"])
        self.assertIsNone(result["rows"][-1]["selective_accuracy"])


class LifecycleTest(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path

        from test_splits import DIGEST, fixture_rows

        from orchestra import experiment
        from orchestra.splits import make_split, materialize

        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        rows = fixture_rows()
        manifest = make_split(rows, DIGEST)
        experiment.write_json(self.root / "split.json", manifest)
        materialize(
            manifest,
            rows,
            self.root / "train.jsonl",
            self.root / "validation.jsonl",
            self.root / "test.jsonl",
        )
        self.config = {
            "seed": 42,
            "split_manifest": str(self.root / "split.json"),
            "train": str(self.root / "train.jsonl"),
            "validation": str(self.root / "validation.jsonl"),
            "sealed_test": str(self.root / "test.jsonl"),
            "results_dir": str(self.root / "results"),
            "configurations": [{"family": "B0"}, {"family": "B1"}]
            + [
                {"family": f, "C": c}
                for f in ("L1", "L2", "S1", "L3")
                for c in (0.1, 1, 10)
            ],
        }
        self.run, _ = experiment.run(self.config, "fixture")
        self.selection = self.root / "selection.json"
        experiment.write_json(self.selection, experiment.select(self.run))

    def test_full_lifecycle_never_reads_test_before_freeze(self):
        from orchestra import confidence

        test_path = self.root / "test.jsonl"
        original = test_path.read_bytes()
        test_path.unlink()
        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        test_path.write_bytes(original)
        result = confidence.final_test(frozen, self.root / "final")
        self.assertEqual(result, confidence.final_test(frozen, self.root / "final"))
        with self.assertRaisesRegex(ValueError, "already reserved"):
            confidence.final_test(frozen, self.root / "another-final")
        self.assertIn("calibrated", confidence.load_artifacts(result)["metrics.json"])

    def test_forged_selection_and_input_change_refused(self):
        import json

        from orchestra import confidence

        selected = json.loads(self.selection.read_text())
        selected["overall"]["chosen"] = "B0"
        selected["valid"] = False
        self.selection.write_text(json.dumps(selected))
        with self.assertRaisesRegex(ValueError, "selection"):
            confidence.analyze(
                self.run, self.selection, self.root / "confidence", fixture=True
            )

    def test_changed_test_content_leaves_failed_receipt(self):
        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        path = self.root / "test.jsonl"
        path.write_text(path.read_text().replace('text": "', 'text": "changed ', 1))
        with self.assertRaisesRegex(ValueError, "content hash"):
            confidence.final_test(frozen, self.root / "final")
        with self.assertRaisesRegex(ValueError, "incomplete"):
            confidence.final_test(frozen, self.root / "final")

    def test_tampered_freeze_refused_before_test_read(self):
        import json

        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        value = confidence.freeze(out, frozen)
        value["fallback"]["chosen"] = 0.999
        frozen.write_text(json.dumps(value))
        (self.root / "test.jsonl").unlink()
        with self.assertRaisesRegex(ValueError, "freeze decisions"):
            confidence.final_test(frozen, self.root / "final")

    def test_calibration_fold_pipelines_only_fit_training_vocabulary(self):
        from orchestra import confidence

        _, _, train, validation, _, _, entry = confidence._context(
            self.run, self.selection
        )
        for row in validation:
            row["text"] += " zzvalidationonlyzz"
        folds = confidence.calibration_folds(train)
        model = confidence._calibrate(entry, train, validation, folds)["pipeline"]
        for classifier in model.calibrated_classifiers_:
            self.assertNotIn(
                "zzvalidationonlyzz",
                classifier.estimator.named_steps["vec"].vocabulary_,
            )
        short = [r for r in train if r["label"] != LABELS[0]]
        with self.assertRaisesRegex(ValueError, "shortage"):
            confidence.calibration_folds(short)

    def test_existing_final_output_does_not_reserve_or_read_test(self):
        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        (self.root / "final").mkdir()
        (self.root / "test.jsonl").unlink()
        with self.assertRaisesRegex(ValueError, "output already exists"):
            confidence.final_test(frozen, self.root / "final")
        self.assertFalse(list((self.root / "fixture-test-receipts").glob("*.json")))

    def test_research_analyze_requires_prepared_evidence(self):
        from orchestra import confidence

        with self.assertRaisesRegex(ValueError, "study evidence"):
            confidence.analyze(self.run, self.selection, self.root / "confidence")

    def test_failed_exact_request_can_resume_with_preserved_history(self):
        from unittest.mock import patch

        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        with (
            patch.object(
                confidence, "_fit", side_effect=RuntimeError("interrupted fixture")
            ),
            self.assertRaisesRegex(RuntimeError, "interrupted"),
        ):
            confidence.final_test(frozen, self.root / "final")
        result = confidence.final_test(frozen, self.root / "final", resume=True)
        self.assertTrue(result.is_dir())

    def test_reliability_respects_estimator_tie_prediction(self):
        from orchestra import confidence, experiment

        train = [
            {"text": "identical phrase", "label": label}
            for label in LABELS
            for _ in range(3)
        ]
        model = experiment.build_l2({"C": 1}, 100).fit(
            [r["text"] for r in train], [r["label"] for r in train]
        )
        predictions = list(model.predict(["unknownword"]))
        probabilities = experiment.score(model, ["unknownword"], "probability")
        result = probability_metrics(predictions, probabilities, predictions)
        self.assertEqual(result["bins"][1]["accuracy"], 1.0)
        self.assertEqual(result["bins"][1]["count"], 1)
        self.assertEqual(
            confidence.ex.metrics(predictions, predictions)["accuracy"], 1.0
        )

    def test_error_interpretation_contract(self):
        import json

        from orchestra import confidence, experiment

        run, _ = experiment.load_run(self.run)
        systems = confidence._context(self.run, self.selection)[5]
        with self.assertRaisesRegex(ValueError, "interpretations"):
            confidence._error_interpretations(None, run, systems)
        path = self.root / "interpretations.jsonl"
        chosen = {entry["id"] for entry in systems}
        facts = [p for p in run["predictions.jsonl"] if p["configuration"] in chosen]
        rows = [
            {
                "configuration": p["configuration"],
                "query_id": p["query_id"],
                "category": "vocabulary_mismatch",
                "hypothesis": "Fixture hypothesis for contract verification.",
            }
            for p in facts
        ]
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        self.assertTrue(confidence._error_interpretations(path, run, systems))
        path.write_text("")
        with self.assertRaisesRegex(ValueError, "interpret at least"):
            confidence._error_interpretations(path, run, systems)

    def test_research_evidence_checks_permissions_and_never_opens_dataset(self):
        import json

        from test_splits import DIGEST

        from orchestra import confidence
        from orchestra.data import file_sha256

        sources = self.root / "sources.json"
        sources.write_text(json.dumps({"fixture": {"license": "fixture-only"}}))
        review = self.root / "review.jsonl"
        review.write_text("{}\n")
        brief = self.root / "brief.md"
        brief.write_text("Fixed collection brief for fixture test.")
        config = {
            "dataset": str(self.root / "missing-dataset"),
            "sources": str(sources),
            "review": str(review),
            "collection_brief": str(brief),
            "study_evidence": {
                "ready": True,
                "dataset_sha256": DIGEST,
                "sources_sha256": file_sha256(sources),
                "review_sha256": file_sha256(review),
                "collection_brief_sha256": file_sha256(brief),
            },
        }
        self.assertEqual(
            len(confidence._research_evidence(config, {"dataset_sha256": DIGEST})), 3
        )
        review.write_text("changed")
        with self.assertRaisesRegex(ValueError, "input changed"):
            confidence._research_evidence(config, {"dataset_sha256": DIGEST})

    def test_environment_mismatch_is_rejected(self):
        import json

        from orchestra import confidence, experiment
        from orchestra.data import file_sha256

        path = self.run / "provenance.json"
        provenance = json.loads(path.read_text())
        provenance["sklearn"] = "incompatible-fixture-version"
        experiment.write_json(path, provenance)
        manifest = json.loads((self.run / "manifest.json").read_text())
        manifest["files"]["provenance.json"] = file_sha256(path)
        experiment.write_json(self.run / "manifest.json", manifest)
        with self.assertRaisesRegex(ValueError, "environment mismatch"):
            confidence.analyze(
                self.run, self.selection, self.root / "confidence", fixture=True
            )

    def test_blocked_parent_fails_before_receipt_or_test_access(self):
        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        parent = self.root / "blocked-parent"
        parent.write_text("ordinary file")
        (self.root / "test.jsonl").unlink()
        with self.assertRaises(FileExistsError):
            confidence.final_test(frozen, parent / "final")
        self.assertFalse(list((self.root / "fixture-test-receipts").glob("*.json")))

    def test_keyboard_interrupt_is_recorded_and_exact_resume_succeeds(self):
        import json
        from unittest.mock import patch

        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        with (
            patch.object(confidence, "_fit", side_effect=KeyboardInterrupt),
            self.assertRaises(KeyboardInterrupt),
        ):
            confidence.final_test(frozen, self.root / "final")
        receipt_path = next((self.root / "fixture-test-receipts").glob("*.json"))
        receipt = json.loads(receipt_path.read_text())
        self.assertEqual(receipt["status"], "failed_after_reservation")
        self.assertIn("KeyboardInterrupt", receipt["attempts"][0]["error"])
        confidence.final_test(frozen, self.root / "final", resume=True)
        self.assertEqual(len(json.loads(receipt_path.read_text())["attempts"]), 2)

    def test_active_final_run_excludes_second_request(self):
        import fcntl

        from orchestra import confidence
        from orchestra.data import file_sha256

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        store = self.root / "fixture-test-receipts"
        store.mkdir()
        lock = store / (file_sha256(self.root / "split.json") + ".lock")
        with lock.open("a") as held:
            fcntl.flock(held.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(ValueError, "active final evaluation"):
                confidence.final_test(frozen, self.root / "final", resume=True)
        self.assertFalse((self.root / "final").exists())

    def test_stale_opened_receipt_resumes_only_after_lock_release(self):
        import json
        from unittest.mock import patch

        from orchestra import confidence, experiment

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen)
        with (
            patch.object(confidence, "_fit", side_effect=RuntimeError("fixture stop")),
            self.assertRaises(RuntimeError),
        ):
            confidence.final_test(frozen, self.root / "final")
        receipt_path = next((self.root / "fixture-test-receipts").glob("*.json"))
        receipt = json.loads(receipt_path.read_text())
        receipt["status"] = "opened"
        receipt["attempts"][0].pop("failed_utc")
        receipt["attempts"][0].pop("error")
        experiment.write_json(receipt_path, receipt)
        confidence.final_test(frozen, self.root / "final", resume=True)
        updated = json.loads(receipt_path.read_text())
        self.assertEqual(updated["status"], "complete")
        self.assertEqual(updated["attempts"][0], receipt["attempts"][0])
        self.assertEqual(len(updated["attempts"]), 2)


def jev_answer(body, choice="calculation"):
    """A valid fake Jev reply for one request body."""
    probabilities = {label: 0.1 for label in LABELS}
    probabilities[choice] = 0.7
    answer = {"type": "choice", "choice": choice, "confidence": 0.5}
    answer["probabilities"] = probabilities
    return 200, {"model": "jev-1.14.0", "answers": {"first_action": answer}}


class M35LifecycleTest(unittest.TestCase):
    """The m3.5 decision set, Jev included, through confidence, freeze and test."""

    def setUp(self):
        import tempfile
        from pathlib import Path

        from test_splits import DIGEST, fixture_rows

        from orchestra import experiment, jev
        from orchestra.data import file_sha256
        from orchestra.splits import make_split, materialize

        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        rows = fixture_rows()
        manifest = make_split(rows, DIGEST)
        experiment.write_json(self.root / "split.json", manifest)
        materialize(
            manifest,
            rows,
            self.root / "train.jsonl",
            self.root / "validation.jsonl",
            self.root / "test.jsonl",
        )
        validation = experiment.load_rows(self.root / "validation.jsonl", "validation")
        log = self.root / "jev-validation.jsonl"
        jev.collect(validation, log, len(validation), jev_answer)
        # The tracked M3.5 template lists the 26 local configurations.
        template = Path(__file__).resolve().parents[1] / "configs" / "m3-5.json"
        local = json.loads(template.read_text())["configurations"]
        self.config = {
            "matrix": "m3.5",
            "seed": 42,
            "split_manifest": str(self.root / "split.json"),
            "train": str(self.root / "train.jsonl"),
            "validation": str(self.root / "validation.jsonl"),
            "sealed_test": str(self.root / "test.jsonl"),
            "results_dir": str(self.root / "results"),
            "configurations": local
            + [
                {
                    "family": "Jev",
                    "responses": str(log),
                    "responses_sha256": file_sha256(log),
                }
            ],
        }
        self.run, _ = experiment.run(self.config, "fixture")
        self.selection = self.root / "selection.json"
        experiment.write_json(self.selection, experiment.select(self.run))
        self.store = self.root / "fixture-test-receipts"
        self.test_log = self.root / "jev-test.jsonl"

    def frozen(self):
        """Analyze and freeze without the test file, then restore it."""
        from orchestra import confidence

        test_path = self.root / "test.jsonl"
        original = test_path.read_bytes()
        test_path.unlink()
        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        confidence.freeze(out, frozen, jev_test_log=self.test_log)
        test_path.write_bytes(original)
        return out, frozen

    def receipts(self):
        return list(self.store.glob("*.json"))

    def test_jev_is_never_calibrated_and_every_system_is_declared(self):
        from orchestra import confidence

        out, _ = self.frozen()
        systems = confidence.load_artifacts(out)["systems.json"]
        selection = json_file(self.selection)
        chosen = {info["chosen"] for info in selection["families"].values()}
        self.assertEqual(set(systems), chosen)
        self.assertEqual(systems["Jev"]["calibration"], "none")
        self.assertEqual(systems["Jev"]["score_type"], "probability")
        self.assertIn("brier", systems["Jev"]["metrics"])
        calibrated = [s for s in systems.values() if s["calibration"] != "none"]
        self.assertEqual(len(calibrated), 1)
        self.assertIn(calibrated[0]["family"], ("L1", "L2", "L3"))
        margins = [s for s in systems.values() if s["score_type"] == "margin"]
        self.assertTrue(margins)
        self.assertTrue(all("brier" not in s["metrics"] for s in margins))

    def test_freeze_requires_an_untracked_unused_jev_test_log(self):
        from pathlib import Path

        from orchestra import confidence

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        with self.assertRaisesRegex(ValueError, "Jev test log"):
            confidence.freeze(out, frozen)
        tracked = Path(confidence.__file__).resolve().parents[2] / "docs" / "x.jsonl"
        with self.assertRaisesRegex(ValueError, "ignored by Git"):
            confidence.freeze(out, frozen, jev_test_log=tracked)
        with self.assertRaisesRegex(ValueError, "no folder"):
            confidence.freeze(out, frozen, jev_test_log=self.root / "no" / "x.jsonl")
        self.test_log.write_text("")
        with self.assertRaisesRegex(ValueError, "already exists"):
            confidence.freeze(out, frozen, jev_test_log=self.test_log)
        self.assertFalse(frozen.exists())

    def test_jev_test_answers_are_collected_inside_the_reservation(self):
        from orchestra import confidence
        from orchestra.data import file_sha256

        _, frozen = self.frozen()
        final = self.root / "final"
        with self.assertRaisesRegex(ValueError, "send-jev-test"):
            confidence.final_test(frozen, final)
        self.assertFalse(self.receipts())
        self.assertFalse(self.test_log.exists())

        sent = []

        def flaky(body):
            sent.append(body["state"]["query"])
            return (503, "unavailable") if len(sent) <= 3 else jev_answer(body)

        with self.assertRaisesRegex(ValueError, "no valid Jev answer; rerun"):
            confidence.final_test(frozen, final, jev_send=flaky)
        (receipt,) = self.receipts()
        self.assertEqual(json_file(receipt)["status"], "failed_after_reservation")
        with self.assertRaisesRegex(ValueError, "send-jev-test"):
            confidence.final_test(frozen, final, resume=True)

        resent = []

        def steady(body):
            resent.append(body["state"]["query"])
            return jev_answer(body)

        result = confidence.final_test(frozen, final, resume=True, jev_send=steady)
        self.assertEqual(resent, sent[:3])
        artifacts = confidence.load_artifacts(result)
        self.assertIn("brier", artifacts["metrics.json"]["Jev"])
        self.assertIn("calibrated", artifacts["metrics.json"])
        jev_rows = [
            json.loads(line)
            for line in (result / "predictions.jsonl").read_text().splitlines()
            if json.loads(line)["configuration"] == "Jev"
        ]
        test = (self.root / "test.jsonl").read_text().splitlines()
        self.assertEqual(len(jev_rows), len(test))
        self.assertEqual({r["prediction"] for r in jev_rows}, {"calculation"})
        self.assertEqual(jev_rows[0]["scores"], [0.1, 0.1, 0.7, 0.1])
        provenance = artifacts["provenance.json"]
        self.assertEqual(provenance["jev_test_log_sha256"], file_sha256(self.test_log))
        self.assertEqual(provenance["jev_test_requests"], len(sent) + len(resent))
        self.assertEqual(len(sent) - 3 + len(resent), len(test))

        def forbidden(body):
            raise AssertionError("a completed final test sent a request")

        self.assertEqual(
            confidence.final_test(frozen, final, jev_send=forbidden), result
        )
        before = frozen.read_text()
        confidence.freeze(self.root / "confidence", frozen, jev_test_log=self.test_log)
        self.assertEqual(frozen.read_text(), before)

    def test_jev_test_log_edited_between_attempts_blocks_resume(self):
        from orchestra import confidence

        _, frozen = self.frozen()
        final = self.root / "final"

        def down(body):
            return 503, "unavailable"

        with self.assertRaisesRegex(ValueError, "no valid Jev answer"):
            confidence.final_test(frozen, final, jev_send=down)
        with self.test_log.open("a", encoding="utf-8") as log:
            log.write("{}\n")
        with self.assertRaisesRegex(ValueError, "changed since the last attempt"):
            confidence.final_test(frozen, final, resume=True, jev_send=jev_answer)

    def test_send_function_without_jev_is_refused_before_reservation(self):
        from orchestra import confidence, experiment

        self.config["matrix"] = "m3"
        self.config["configurations"] = [
            c for c in self.config["configurations"] if c["family"] in M3_FAMILIES
        ]
        run, _ = experiment.run(self.config, "m3")
        selection = self.root / "m3-selection.json"
        experiment.write_json(selection, experiment.select(run))
        out = confidence.analyze(run, selection, self.root / "m3-conf", fixture=True)
        frozen = self.root / "m3-freeze.json"
        confidence.freeze(out, frozen)
        with self.assertRaisesRegex(ValueError, "no Jev system"):
            confidence.final_test(frozen, self.root / "f", jev_send=jev_answer)
        self.assertFalse(list((self.root / "fixture-test-receipts").glob("*.json")))

    def test_xgboost_version_mismatch_is_rejected(self):
        from orchestra import confidence, experiment
        from orchestra.data import file_sha256

        path = self.run / "provenance.json"
        original = path.read_text()
        for version in ("incompatible-fixture-version", None):
            with self.subTest(version=version):
                provenance = json.loads(original)
                provenance["xgboost"] = version
                if version is None:
                    del provenance["xgboost"]  # an m3.5 run must record it
                experiment.write_json(path, provenance)
                manifest = json_file(self.run / "manifest.json")
                manifest["files"]["provenance.json"] = file_sha256(path)
                experiment.write_json(self.run / "manifest.json", manifest)
                with self.assertRaisesRegex(ValueError, "mismatch: xgboost"):
                    confidence.analyze(
                        self.run, self.selection, self.root / "c", fixture=True
                    )

    def test_jev_test_log_written_before_reservation_is_refused(self):
        from orchestra import confidence

        _, frozen = self.frozen()
        self.test_log.write_text("")
        with self.assertRaisesRegex(ValueError, "before the test was reserved"):
            confidence.final_test(frozen, self.root / "final", jev_send=jev_answer)
        self.assertFalse(self.receipts())

    def test_cli_freezes_the_log_path_and_refuses_a_missing_key(self):
        import contextlib
        import io
        import os
        from unittest import mock

        from orchestra import confidence, jev
        from orchestra.__main__ import main

        def cli(*argv):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(list(argv))
            return code, output.getvalue()

        out = confidence.analyze(
            self.run, self.selection, self.root / "confidence", fixture=True
        )
        frozen = self.root / "freeze.json"
        code, _ = cli(
            "freeze",
            "--confidence",
            str(out),
            "--out",
            str(frozen),
            "--jev-test-log",
            str(self.test_log),
        )
        self.assertEqual(code, 0)
        self.assertEqual(
            json_file(frozen)["jev_test_log"], str(self.test_log.resolve())
        )
        environment = {k: v for k, v in os.environ.items() if k != jev.KEY_VARIABLE}
        final = ("final-test", "--freeze", str(frozen), "--out", str(self.root / "f"))
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(jev, "post", side_effect=AssertionError("network")),
        ):
            code, output = cli(*final, "--send-jev-test")
            self.assertEqual(
                (code, output.strip()), (1, "ERROR: TYPESAFE_API_KEY is not set")
            )
            code, output = cli(*final)
            self.assertEqual(code, 1)
            self.assertIn("--send-jev-test", output)
        self.assertFalse(self.receipts())

    def test_set_without_jev_refuses_a_jev_test_log(self):
        from orchestra import confidence, experiment

        self.config["matrix"] = "m3"
        self.config["configurations"] = [
            c for c in self.config["configurations"] if c["family"] in M3_FAMILIES
        ]
        run, _ = experiment.run(self.config, "m3")
        selection = self.root / "m3-selection.json"
        experiment.write_json(selection, experiment.select(run))
        out = confidence.analyze(run, selection, self.root / "m3-conf", fixture=True)
        with self.assertRaisesRegex(ValueError, "no Jev system"):
            confidence.freeze(
                out, self.root / "m3-freeze.json", jev_test_log=self.test_log
            )


M3_FAMILIES = ("B0", "B1", "L1", "L2", "S1", "L3")


def json_file(path):
    return json.loads(path.read_text())
