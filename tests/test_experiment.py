import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_splits import DIGEST, fixture_rows

from orchestra import experiment
from orchestra.__main__ import main
from orchestra.data import LABELS, file_sha256
from orchestra.splits import make_split, materialize

CONFIGURATIONS = [{"family": "B0"}, {"family": "L2", "C": 1}]


class RunTestCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.rows = fixture_rows()
        self.manifest = make_split(self.rows, DIGEST)
        validation = set(self.manifest["partitions"]["validation"])
        for row in self.rows:
            if row["query_id"] in validation:
                row["text"] += " zzheldoutzz"
        materialize(
            self.manifest,
            self.rows,
            self.root / "train.jsonl",
            self.root / "validation.jsonl",
            self.root / "sealed" / "test.jsonl",
        )
        (self.root / "split.json").write_text(json.dumps(self.manifest))
        self.config_path = self.root / "config.json"
        self.config_path.write_text(json.dumps(self.config()))

    def config(self):
        return {
            "seed": 42,
            "split_manifest": str(self.root / "split.json"),
            "train": str(self.root / "train.jsonl"),
            "validation": str(self.root / "validation.jsonl"),
            "sealed_test": str(self.root / "sealed" / "test.jsonl"),
            "results_dir": str(self.root / "results"),
            "configurations": CONFIGURATIONS,
        }

    def cli(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(list(argv))
        return code, output.getvalue()

    def run_id(self, run_id):
        return self.cli("run", "--config", str(self.config_path), "--run-id", run_id)

    def result(self, run_id, name):
        return json.loads((self.root / "results" / run_id / name).read_text())


class BaselineBehaviorTest(RunTestCase):
    def test_b0_predicts_training_majority_for_every_validation_row(self):
        self.assertEqual(self.run_id("a")[0], 0)
        lines = (self.root / "results/a/predictions.jsonl").read_text().splitlines()
        rows = [json.loads(line) for line in lines]
        b0 = [r for r in rows if r["configuration"] == "B0"]
        self.assertEqual(len(b0), 10)
        self.assertEqual({r["prediction"] for r in b0}, {"direct_answer"})
        self.assertEqual(self.result("a", "metrics.json")["B0"]["accuracy"], 0.3)
        self.assertEqual(
            self.result("a", "metrics.json")["B0"]["never_predicted"],
            ["document_retrieval", "knowledge_lookup", "calculation"],
        )

    def test_validation_only_token_is_not_in_fitted_vocabulary(self):
        train = experiment.load_rows(self.root / "train.jsonl", "train")
        validation = experiment.load_rows(self.root / "validation.jsonl", "validation")
        entry = experiment.resolve_configurations(CONFIGURATIONS)[1]
        pipeline = experiment.fit_predict(entry, train, validation)["pipeline"]
        vocabulary = pipeline.named_steps["vec"].vocabulary_
        self.assertTrue(all("zzheldoutzz" in r["text"] for r in validation))
        self.assertNotIn("zzheldoutzz", vocabulary)
        self.assertIn("artificial", vocabulary)

    def test_scores_follow_labels_order_not_alphabetical(self):
        self.assertEqual(self.run_id("a")[0], 0)
        self.assertNotEqual(list(LABELS), sorted(LABELS))
        lines = (self.root / "results/a/predictions.jsonl").read_text().splitlines()
        l2 = [json.loads(x) for x in lines if '"L2-C1"' in x]
        self.assertEqual(len(l2), 10)
        for row in l2:
            self.assertEqual(row["score_type"], "probability")
            self.assertEqual(len(row["scores"]), 4)
            best = row["scores"].index(max(row["scores"]))
            self.assertEqual(LABELS[best], row["prediction"])
            self.assertAlmostEqual(sum(row["scores"]), 1.0)

    def test_resolved_l2_params_and_no_deprecated_penalty_argument(self):
        self.assertEqual(self.run_id("a")[0], 0)
        params = self.result("a", "config.json")["resolved_params"]["L2-C1"]
        clf = params["classifier"]
        self.assertEqual(
            (clf["C"], clf["solver"], clf["l1_ratio"], clf["max_iter"]),
            (1, "lbfgs", 0.0, 100),
        )
        self.assertEqual((clf["tol"], clf["random_state"]), (1e-4, 42))
        self.assertEqual(params["vectorizer"]["token_pattern"], r"(?u)\b\w+\b")
        self.assertEqual(params["vectorizer"]["max_features"], 10000)

    def test_outcomes_record_status_and_one_attempt(self):
        self.run_id("a")
        outcomes = self.result("a", "outcomes.json")
        self.assertEqual([o["id"] for o in outcomes], ["B0", "L2-C1"])
        self.assertEqual([o["status"] for o in outcomes], ["ok", "ok"])
        self.assertEqual([len(o["attempts"]) for o in outcomes], [1, 1])


class MetricsTest(unittest.TestCase):
    def test_literal_counts_f1_and_zero_predicted_class(self):
        true = ["document_retrieval"] * 2 + ["knowledge_lookup", "calculation"]
        true += ["direct_answer"] * 2
        pred = ["document_retrieval", "knowledge_lookup", "knowledge_lookup"]
        pred += ["direct_answer"] * 3
        m = experiment.metrics(true, pred)
        c = experiment.confusion(true, pred)
        self.assertEqual(
            c["counts"], [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2]]
        )
        self.assertEqual(c["normalized"][0], [0.5, 0.5, 0.0, 0.0])
        self.assertAlmostEqual(m["accuracy"], 4 / 6)
        self.assertAlmostEqual(m["macro_f1"], (2 / 3 + 2 / 3 + 0 + 0.8) / 4)
        self.assertEqual(m["never_predicted"], ["calculation"])
        self.assertEqual(m["per_class"]["calculation"]["precision"], 0.0)
        self.assertEqual(m["per_class"]["calculation"]["support"], 1)
        self.assertAlmostEqual(m["per_class"]["document_retrieval"]["recall"], 0.5)

    def test_class_with_no_support_gives_zero_row(self):
        c = experiment.confusion(["direct_answer"], ["direct_answer"])
        self.assertEqual(c["counts"][0], [0, 0, 0, 0])
        self.assertEqual(c["normalized"][0], [0.0, 0.0, 0.0, 0.0])
        self.assertEqual(c["normalized"][3], [0.0, 0.0, 0.0, 1.0])


class GuardTest(RunTestCase):
    def test_refuses_existing_run_directory(self):
        self.assertEqual(self.run_id("a")[0], 0)
        before = file_sha256(self.root / "results/a/manifest.json")
        code, output = self.run_id("a")
        self.assertEqual(code, 1)
        self.assertEqual(
            output,
            f"ERROR: run directory {self.root}/results/a already exists; "
            "pick a new run id\n",
        )
        self.assertEqual(file_sha256(self.root / "results/a/manifest.json"), before)

    def test_refuses_train_ids_that_disagree_with_manifest(self):
        path = self.root / "train.jsonl"
        lines = path.read_text().splitlines(keepends=True)
        path.write_text("".join(lines[1:]))
        code, output = self.run_id("a")
        self.assertEqual(code, 1)
        self.assertIn("train query_ids differ from the split manifest", output)
        self.assertFalse((self.root / "results" / "a").exists())

    def test_never_opens_dataset_or_sealed_files(self):
        dataset = self.root / "data.jsonl"
        dataset.write_text("{}\n")
        sealed = self.root / "sealed" / "test.jsonl"
        self.assertTrue(sealed.exists())
        self.config_path.write_text(
            json.dumps({**self.config(), "dataset": str(dataset)})
        )
        opened = []
        real_open = open

        def recording_open(file, *args, **kwargs):
            opened.append(os.fspath(file) if not isinstance(file, int) else file)
            return real_open(file, *args, **kwargs)

        with (
            mock.patch("builtins.open", recording_open),
            mock.patch("io.open", recording_open),
        ):
            self.assertEqual(self.run_id("a")[0], 0)
        self.assertIn(str(self.root / "train.jsonl"), opened)
        forbidden = {str(dataset), str(sealed)}
        self.assertEqual(forbidden & {str(p) for p in opened}, set())

    def test_refuses_empty_configuration_list(self):
        config = {**self.config(), "configurations": []}
        self.config_path.write_text(json.dumps(config))
        code, output = self.run_id("a")
        self.assertEqual(code, 1)
        self.assertIn("non-empty list", output)

    def test_provenance_records_library_and_annotation_versions(self):
        self.run_id("a")
        p = self.result("a", "provenance.json")
        self.assertEqual(p["annotation_versions"], ["v0"])
        self.assertEqual(p["manifest_dataset_sha256"], DIGEST)
        for key in ("numpy", "scipy", "sklearn"):
            self.assertRegex(p[key], r"^\d+\.\d+")

    def test_succeeds_without_the_sealed_test_file(self):
        (self.root / "sealed" / "test.jsonl").unlink()
        self.assertEqual(self.run_id("a")[0], 0)

    def test_reports_missing_config_key(self):
        config = self.config()
        del config["configurations"]
        self.config_path.write_text(json.dumps(config))
        code, output = self.run_id("a")
        self.assertEqual(
            (code, output), (1, "ERROR: config is missing 'configurations'\n")
        )

    def test_failed_configuration_is_recorded_and_run_continues(self):
        config = self.config()
        config["configurations"] = [{"family": "L2", "C": -1}, {"family": "B0"}]
        self.config_path.write_text(json.dumps(config))
        code, _ = self.run_id("a")
        self.assertEqual(code, 1)
        outcomes = self.result("a", "outcomes.json")
        self.assertEqual([o["status"] for o in outcomes], ["failed", "ok"])
        self.assertIn("InvalidParameterError", outcomes[0]["error"])
        self.assertTrue((self.root / "results/a/manifest.json").is_file())

    def test_unknown_family_is_refused(self):
        config = self.config()
        config["configurations"] = [{"family": "ZZ"}]
        self.config_path.write_text(json.dumps(config))
        self.assertEqual(self.run_id("a")[0], 1)


class ConvergenceRetryTest(RunTestCase):
    def run_with_limit(self, retry_max_iter):
        # A one-iteration first attempt cannot converge, so lbfgs warns.
        family = {
            **experiment.FAMILIES["L2"],
            "build": lambda C, n: experiment.build_l2(C, n or 1),
            "retry_max_iter": retry_max_iter,
        }
        config = {**self.config(), "configurations": [{"family": "L2", "C": 1}]}
        self.config_path.write_text(json.dumps(config))
        with mock.patch.dict(experiment.FAMILIES, {"L2": family}):
            return self.run_id("a")

    def test_retry_at_larger_limit_records_failed_attempt(self):
        self.assertEqual(self.run_with_limit(1000)[0], 0)
        (outcome,) = self.result("a", "outcomes.json")
        self.assertEqual(outcome["status"], "ok")
        self.assertEqual(
            [(a["max_iter"], a["converged"]) for a in outcome["attempts"]],
            [(1, False), (1000, True)],
        )
        self.assertEqual(
            outcome["attempts"][0]["warnings"][0]["category"], "ConvergenceWarning"
        )
        params = self.result("a", "config.json")["resolved_params"]["L2-C1"]
        self.assertEqual(params["classifier"]["max_iter"], 1000)

    def test_unresolved_warning_after_retry(self):
        self.assertEqual(self.run_with_limit(1)[0], 1)
        (outcome,) = self.result("a", "outcomes.json")
        self.assertEqual(outcome["status"], "unresolved_warning")
        self.assertEqual(len(outcome["attempts"]), 2)

    def test_member_that_raised_is_retried_with_its_family(self):
        family = {
            **experiment.FAMILIES["L2"],
            "build": lambda C, n: experiment.build_l2(C, n or 1),
        }
        config = {
            **self.config(),
            "configurations": [{"family": "L2", "C": 1}, {"family": "L2", "C": -1}],
        }
        self.config_path.write_text(json.dumps(config))
        with mock.patch.dict(experiment.FAMILIES, {"L2": family}):
            self.assertEqual(self.run_id("a")[0], 1)
        good, bad = self.result("a", "outcomes.json")
        self.assertEqual(good["status"], "ok")
        self.assertEqual(len(bad["attempts"]), 2)
        self.assertIn("InvalidParameterError", bad["attempts"][0]["error"])
        self.assertEqual(bad["status"], "failed")


class ArtifactTest(RunTestCase):
    def test_manifest_hashes_match_file_contents(self):
        self.run_id("a")
        out = self.root / "results/a"
        manifest = self.result("a", "manifest.json")
        self.assertIs(manifest["complete"], True)
        self.assertEqual(set(manifest["files"]), set(experiment.RUN_FILES))
        for name, digest in manifest["files"].items():
            self.assertEqual(file_sha256(out / name), digest)
        self.assertNotIn(
            "artificial fixture text", (out / "predictions.jsonl").read_text()
        )

    def test_tampered_file_fails_compare(self):
        self.run_id("a")
        self.run_id("b")
        path = self.root / "results/b/metrics.json"
        path.write_text(path.read_text().replace("0.3", "0.4", 1))
        code, output = self.cli(
            "compare",
            "--left",
            str(self.root / "results/a"),
            "--right",
            str(self.root / "results/b"),
        )
        self.assertEqual(code, 1)
        self.assertIn("metrics.json does not match its manifest hash", output)
        self.assertTrue(output.endswith("FAIL: runs differ\n"))

    def test_partial_run_without_manifest_fails_compare(self):
        self.run_id("a")
        self.run_id("b")
        (self.root / "results/b/manifest.json").unlink()
        diffs = experiment.compare(self.root / "results/a", self.root / "results/b")
        self.assertEqual(len(diffs), 1)
        self.assertIn("partial run", diffs[0])


class CompareGuardTest(RunTestCase):
    def setUp(self):
        super().setUp()
        self.run_id("a")
        self.run_id("b")
        self.a, self.b = self.root / "results/a", self.root / "results/b"

    def rewrite(self, directory, name, edit):
        path = directory / name
        path.write_text(edit(path.read_text()))
        manifest = json.loads((directory / "manifest.json").read_text())
        manifest["files"][name] = file_sha256(path)
        (directory / "manifest.json").write_text(json.dumps(manifest))

    def shift_first_l2_score(self, delta):
        def edit(text):
            lines = text.splitlines()
            i = next(n for n, x in enumerate(lines) if '"L2-C1"' in x)
            row = json.loads(lines[i])
            row["scores"][0] += delta
            lines[i] = json.dumps(row)
            return "\n".join(lines) + "\n"

        self.rewrite(self.b, "predictions.jsonl", edit)

    def test_identical_runs_pass(self):
        self.assertEqual(experiment.compare(self.a, self.b), [])

    def test_same_directory_is_refused(self):
        diffs = experiment.compare(self.a, self.a)
        self.assertIn("left and right are the same directory", diffs)
        self.assertIn("left and right share a run_id", diffs)

    def test_shared_run_id_is_refused(self):
        self.rewrite(
            self.b,
            "provenance.json",
            lambda t: t.replace('"run_id": "b"', '"run_id": "a"'),
        )
        self.assertEqual(
            experiment.compare(self.a, self.b), ["left and right share a run_id"]
        )

    def test_run_with_a_non_ok_outcome_is_refused(self):
        for directory in (self.a, self.b):
            self.rewrite(
                directory,
                "outcomes.json",
                lambda t: t.replace('"status": "ok"', '"status": "failed"', 1),
            )
        diffs = experiment.compare(self.a, self.b)
        self.assertEqual(
            diffs[:2],
            [
                "left has configurations that are not ok: B0",
                "right has configurations that are not ok: B0",
            ],
        )

    def test_empty_predictions_on_both_sides_are_refused(self):
        for directory in (self.a, self.b):
            self.rewrite(directory, "predictions.jsonl", lambda t: "")
        diffs = experiment.compare(self.a, self.b)
        self.assertIn("left has no predictions", diffs)
        self.assertIn("right has no predictions", diffs)

    def test_missing_configuration_in_predictions_is_refused(self):
        def drop_b0(text):
            return "".join(x for x in text.splitlines(True) if '"B0"' not in x)

        self.rewrite(self.b, "predictions.jsonl", drop_b0)
        diffs = experiment.compare(self.a, self.b)
        self.assertIn("right predictions do not cover its configurations", diffs)

    def test_non_finite_score_is_refused(self):
        self.shift_first_l2_score(float("nan"))
        self.assertIn("right has non-finite scores", experiment.compare(self.a, self.b))

    def test_score_tolerance_boundary(self):
        self.shift_first_l2_score(5e-11)
        self.assertEqual(experiment.compare(self.a, self.b), [])
        self.rewrite(self.b, "predictions.jsonl", lambda t: t)  # keep manifest valid
        self.shift_first_l2_score(5e-10)
        self.assertEqual(
            experiment.compare(self.a, self.b),
            ["predictions.jsonl row 11: scores differ beyond 1e-10"],
        )

    def test_runs_from_copied_inputs_in_another_directory_compare_equal(self):
        copy = self.root / "restored"
        shutil.copytree(self.root, copy, ignore=shutil.ignore_patterns("results"))
        config = json.loads(self.config_path.read_text())
        for key in ("split_manifest", "train", "validation", "sealed_test"):
            config[key] = config[key].replace(str(self.root), str(copy))
        config["results_dir"] = str(copy / "results")
        (copy / "config.json").write_text(json.dumps(config))
        code, _ = self.cli(
            "run", "--config", str(copy / "config.json"), "--run-id", "c"
        )
        self.assertEqual(code, 0)
        self.assertEqual(experiment.compare(self.a, copy / "results/c"), [])


class ReproductionTest(RunTestCase):
    def process(self, *argv):
        env = {
            **os.environ,
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
        }
        return subprocess.run(
            [sys.executable, "-m", "orchestra", *argv],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_two_processes_reproduce_and_altered_prediction_fails(self):
        for run_id in ("a", "b"):
            done = self.process(
                "run", "--config", str(self.config_path), "--run-id", run_id
            )
            self.assertEqual(done.returncode, 0)
            self.assertIn("PASS: run written to", done.stdout)
        left, right = self.root / "results/a", self.root / "results/b"
        done = self.process("compare", "--left", str(left), "--right", str(right))
        self.assertEqual((done.returncode, done.stdout), (0, "PASS: runs reproduce\n"))
        self.assertEqual(
            self.result("b", "provenance.json")["thread_env"]["OMP_NUM_THREADS"], "1"
        )

        lines = (right / "predictions.jsonl").read_text().splitlines()
        first = json.loads(lines[0])
        first["prediction"] = (
            "calculation" if first["prediction"] != "calculation" else "direct_answer"
        )
        lines[0] = json.dumps(first)
        (right / "predictions.jsonl").write_text("\n".join(lines) + "\n")
        manifest = json.loads((right / "manifest.json").read_text())
        manifest["files"]["predictions.jsonl"] = file_sha256(
            right / "predictions.jsonl"
        )
        (right / "manifest.json").write_text(json.dumps(manifest))
        done = self.process("compare", "--left", str(left), "--right", str(right))
        self.assertEqual(done.returncode, 1)
        self.assertIn("predictions.jsonl row 1", done.stdout)
        self.assertTrue(done.stdout.endswith("FAIL: runs differ\n"))


if __name__ == "__main__":
    unittest.main()
