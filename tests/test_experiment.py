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
        self.assertEqual([a["max_iter"] for a in bad["attempts"]], [100, 1000])

    def test_whole_family_reruns_when_one_member_warns(self):
        family = {
            **experiment.FAMILIES["L2"],
            "build": lambda C, n: experiment.build_l2(C, n or (1 if C == 10 else 100)),
        }
        entries = [{"family": "L2", "C": 0.1}, {"family": "L2", "C": 10}]
        self.config_path.write_text(
            json.dumps({**self.config(), "configurations": entries})
        )
        with mock.patch.dict(experiment.FAMILIES, {"L2": family}):
            self.assertEqual(self.run_id("a")[0], 0)
        calm, warned = self.result("a", "outcomes.json")
        self.assertEqual([a["max_iter"] for a in calm["attempts"]], [100, 1000])
        self.assertEqual([a["converged"] for a in calm["attempts"]], [True, True])
        self.assertEqual([a["max_iter"] for a in warned["attempts"]], [1, 1000])
        self.assertEqual((calm["status"], warned["status"]), ("ok", "ok"))

    def test_retry_limits_are_1000_for_logistic_and_10000_for_svm(self):
        for family_id, expected in (("L1", 1000), ("L3", 1000), ("S1", 10000)):
            real = experiment.FAMILIES[family_id]
            family = {**real, "build": lambda C, n, b=real["build"]: b(C, n or 1)}
            entries = [{"family": family_id, "C": 1}]
            self.config_path.write_text(
                json.dumps({**self.config(), "configurations": entries})
            )
            with mock.patch.dict(experiment.FAMILIES, {family_id: family}):
                code, _ = self.run_id(family_id)
            self.assertEqual(code, 0, family_id)
            (outcome,) = self.result(family_id, "outcomes.json")
            self.assertEqual(
                [a["max_iter"] for a in outcome["attempts"]], [1, expected]
            )
            self.assertEqual(
                outcome["attempts"][0]["warnings"][0]["category"],
                "ConvergenceWarning",
            )
        params = self.result("S1", "config.json")["resolved_params"]["S1-C1"]
        self.assertEqual(params["classifier"]["dual"], "auto")
        self.assertEqual(params["classifier"]["max_iter"], 10000)


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


M3_IDS = [
    "B0",
    "B1",
    "L1-C0.1",
    "L1-C1",
    "L1-C10",
    "L2-C0.1",
    "L2-C1",
    "L2-C10",
    "S1-C0.1",
    "S1-C1",
    "S1-C10",
    "L3-C0.1",
    "L3-C1",
    "L3-C10",
]


class FamilyTest(RunTestCase):
    def run_config(self, configurations):
        config = {**self.config(), "configurations": configurations}
        self.config_path.write_text(json.dumps(config))
        self.assertEqual(self.run_id("a")[0], 0)
        lines = (self.root / "results/a/predictions.jsonl").read_text().splitlines()
        return [json.loads(line) for line in lines]

    def test_m3_config_expands_to_the_14_literal_ids(self):
        path = Path(__file__).resolve().parents[1] / "configs" / "m3.json"
        entries = json.loads(path.read_text())["configurations"]
        resolved = experiment.resolve_configurations(entries)
        self.assertEqual([c["id"] for c in resolved], M3_IDS)

    def test_s1_margins_follow_labels_order_and_are_labeled_margin(self):
        rows = self.run_config([{"family": "S1", "C": 1}])
        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertEqual(row["score_type"], "margin")
            self.assertEqual(len(row["scores"]), 4)
            best = row["scores"].index(max(row["scores"]))
            self.assertEqual(LABELS[best], row["prediction"])
        clf = self.result("a", "config.json")["resolved_params"]["S1-C1"]["classifier"]
        self.assertEqual(
            (clf["penalty"], clf["loss"], clf["dual"], clf["max_iter"]),
            ("l2", "squared_hinge", "auto", 1000),
        )
        self.assertEqual((clf["multi_class"], clf["random_state"]), ("ovr", 42))

    def test_b1_probabilities_sum_to_one_on_counts(self):
        rows = self.run_config([{"family": "B1"}])
        for row in rows:
            self.assertEqual(row["score_type"], "probability")
            self.assertAlmostEqual(sum(row["scores"]), 1.0)
            self.assertEqual(
                LABELS[row["scores"].index(max(row["scores"]))], row["prediction"]
            )
        params = self.result("a", "config.json")["resolved_params"]["B1"]
        self.assertEqual(params["vectorizer"]["ngram_range"], [1, 1])
        self.assertEqual(
            (params["classifier"]["alpha"], params["classifier"]["fit_prior"]),
            (1.0, True),
        )

    def test_l3_uses_bigrams_and_l1_uses_counts(self):
        self.run_config([{"family": "L3", "C": 1}, {"family": "L1", "C": 1}])
        params = self.result("a", "config.json")["resolved_params"]
        self.assertEqual(params["L3-C1"]["vectorizer"]["ngram_range"], [1, 2])
        self.assertIn("lowercase", params["L1-C1"]["vectorizer"])
        self.assertNotIn("use_idf", params["L1-C1"]["vectorizer"])

    def test_latency_is_recorded_with_batch_and_repetitions(self):
        self.run_config([{"family": "B0"}])
        latency = self.result("a", "timing.json")["configurations"]["B0"]["latency"]
        self.assertEqual((latency["batch_size"], latency["repetitions"]), (10, 30))
        self.assertGreater(latency["p95_seconds"], 0)
        self.assertLessEqual(latency["median_seconds"], latency["p95_seconds"])


def write_run(directory, spec, run_id="fx", blocked=None):
    """Write a literal run: spec maps id -> (family, C, status, macro_f1, latency)."""
    directory.mkdir(parents=True)
    entries = [
        {"id": cid, "family": family, "C": c}
        for cid, (family, c, *_rest) in spec.items()
    ]
    contents = {
        "config.json": {"configurations": entries},
        "provenance.json": {
            "run_id": run_id,
            "manifest_dataset_sha256": "d" * 64,
            "split_manifest_sha256": "s" * 64,
            "train_sha256": "t" * 64,
            "validation_sha256": "v" * 64,
        },
        "outcomes.json": [
            {"id": cid, "status": status} for cid, (_, _, status, *_r) in spec.items()
        ],
        "metrics.json": {
            cid: {"macro_f1": f1, "accuracy": f1}
            for cid, (_, _, status, f1, _l) in spec.items()
            if status != "failed"
        },
        "timing.json": {
            "configurations": {
                cid: {"latency": {"median_seconds": lat}}
                for cid, (*_h, lat) in spec.items()
            }
        },
        "confusion.json": {},
        "warnings.json": {},
        "predictions.jsonl": None,
    }
    files = {}
    for name in experiment.RUN_FILES:
        text = "" if name == "predictions.jsonl" else json.dumps(contents[name])
        (directory / name).write_text(text)
        files[name] = file_sha256(directory / name)
    (directory / "manifest.json").write_text(
        json.dumps({"run_id": run_id, "complete": True, "files": files})
    )


def full_spec(**overrides):
    """All 14 required configurations ok at macro-F1 0.5 unless overridden."""
    spec = {}
    for cid in experiment.REQUIRED_IDS:
        family, _, c = cid.partition("-C")
        spec[cid] = (family, float(c) if c else None, "ok", 0.5, 0.1)
    for key, value in overrides.items():
        spec[key.replace("_C", "-C")] = value
    return spec


class SelectionTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def select(self, spec):
        write_run(self.root / "run", spec)
        return experiment.select(self.root / "run")

    def test_tie_within_tolerance_picks_smallest_c(self):
        # 0.80 - 0.79 is exactly the inclusive tolerance.
        selection = self.select(
            {
                **full_spec(),
                "L2-C0.1": ("L2", 0.1, "ok", 0.795, 0.1),
                "L2-C1": ("L2", 1, "ok", 0.80, 0.1),
                "L2-C10": ("L2", 10, "ok", 0.79, 0.1),
            }
        )
        family = selection["families"]["L2"]
        self.assertEqual(family["tie_set"], ["L2-C0.1", "L2-C1", "L2-C10"])
        self.assertEqual(family["chosen"], "L2-C0.1")
        self.assertIs(selection["valid"], True)
        self.assertIs(selection["complete_matrix"], True)

    def test_gap_of_0_011_is_not_a_tie(self):
        selection = self.select(
            {
                **full_spec(),
                "L2-C0.1": ("L2", 0.1, "ok", 0.789, 0.1),
                "L2-C1": ("L2", 1, "ok", 0.80, 0.1),
            }
        )
        family = selection["families"]["L2"]
        self.assertEqual(family["tie_set"], ["L2-C1"])
        self.assertEqual(family["chosen"], "L2-C1")

    def test_failed_configuration_invalidates_and_stays_listed(self):
        selection = self.select(
            {
                **full_spec(),
                "L2-C1": ("L2", 1, "unresolved_warning", 0.9, 0.1),
                "L2-C10": ("L2", 10, "failed", None, 0.1),
            }
        )
        self.assertIs(selection["valid"], False)
        self.assertEqual(selection["blocking"], ["L2-C1", "L2-C10"])
        self.assertEqual(selection["configurations"]["L2-C10"]["status"], "failed")
        self.assertIsNone(selection["families"]["B0"]["chosen"])
        self.assertIsNone(selection["overall"]["chosen"])

    def test_incomplete_matrix_is_invalid_and_lists_missing(self):
        selection = self.select(
            {
                "B0": ("B0", None, "ok", 0.1, 0.1),
                "L2-C1": ("L2", 1, "ok", 0.8, 0.1),
            }
        )
        self.assertIs(selection["valid"], False)
        self.assertIs(selection["complete_matrix"], False)
        self.assertEqual(selection["blocking"], [])
        self.assertEqual(len(selection["missing"]), 12)
        self.assertIn("S1-C0.1", selection["missing"])
        self.assertNotIn("L2-C1", selection["missing"])
        self.assertIsNone(selection["overall"]["chosen"])

    def test_extra_configuration_is_invalid(self):
        spec = {**full_spec(), "L2-C100": ("L2", 100, "ok", 0.5, 0.1)}
        selection = self.select(spec)
        self.assertIs(selection["valid"], False)
        self.assertEqual(selection["unexpected"], ["L2-C100"])

    def test_overall_tie_prefers_the_simpler_family_over_latency(self):
        selection = self.select(
            {
                **full_spec(),
                "L3-C1": ("L3", 1, "ok", 0.80, 0.001),
                "S1-C1": ("S1", 1, "ok", 0.795, 0.002),
                "L2-C1": ("L2", 1, "ok", 0.79, 0.9),
            }
        )
        self.assertEqual(selection["overall"]["tie_set"], ["L2-C1", "S1-C1", "L3-C1"])
        self.assertEqual(selection["overall"]["chosen"], "L2-C1")
        self.assertEqual(selection["families"]["B0"]["chosen"], "B0")

    def test_overall_gap_beyond_tolerance_keeps_only_the_best_winner(self):
        selection = self.select(
            {
                **full_spec(),
                "L1-C1": ("L1", 1, "ok", 0.70, 0.1),
                "L3-C1": ("L3", 1, "ok", 0.80, 0.1),
            }
        )
        self.assertEqual(selection["overall"]["chosen"], "L3-C1")

    def test_cli_writes_invalid_selection_and_exits_1_and_refuses_overwrite(self):
        write_run(
            self.root / "run",
            {**full_spec(), "B0": ("B0", None, "failed", None, 0.1)},
        )
        out = self.root / "selection.json"
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(["select", "--run", str(self.root / "run"), "--out", str(out)])
        self.assertEqual(code, 1)
        self.assertIn("FAIL: selection is not valid; blocked by B0", output.getvalue())
        saved = json.loads(out.read_text())
        self.assertEqual((saved["valid"], saved["run_id"]), (False, "fx"))
        self.assertEqual(saved["hashes"]["validation_sha256"], "v" * 64)
        out.write_text("{}")
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(["select", "--run", str(self.root / "run"), "--out", str(out)])
        self.assertEqual(code, 1)
        self.assertIn("exists and differs; selections are immutable", output.getvalue())
        self.assertEqual(out.read_text(), "{}")


class ReportTest(RunTestCase):
    def setUp(self):
        super().setUp()
        path = Path(__file__).resolve().parents[1] / "configs" / "m3.json"
        entries = json.loads(path.read_text())["configurations"]
        self.config_path.write_text(
            json.dumps({**self.config(), "configurations": entries})
        )
        self.assertEqual(self.run_id("a")[0], 0)
        self.run_dir = self.root / "results/a"
        self.selection = self.root / "selection.json"
        self.assertEqual(
            self.cli(
                "select", "--run", str(self.run_dir), "--out", str(self.selection)
            )[0],
            0,
        )

    def report(self, validation=None, run_dir=None, selection=None):
        return self.cli(
            "report",
            "--run",
            str(run_dir or self.run_dir),
            "--selection",
            str(selection or self.selection),
            "--train",
            str(self.root / "train.jsonl"),
            "--validation",
            str(validation or self.root / "validation.jsonl"),
        )

    def test_report_is_byte_identical_and_fits_nothing(self):
        out = self.root / "results/a-report"
        with mock.patch(
            "sklearn.pipeline.Pipeline.fit", side_effect=AssertionError("fit called")
        ):
            first = self.report()
            saved = self.root / "first"
            out.rename(saved)
            second = self.report()
        self.assertEqual((first[0], second[0]), (0, 0))
        self.assertTrue(first[1].endswith(f"PASS: report written to {out}\n"))
        for name in ("comparison.md", "errors.jsonl"):
            self.assertEqual((saved / name).read_bytes(), (out / name).read_bytes())
        text = (out / "comparison.md").read_text()
        self.assertIn("# Validation comparison for run `a`", text)
        self.assertIn("| B0 | ok | 0.3000 | ", text)
        self.assertIn("| L3-C10 | ok | ", text)
        self.assertIn("### L2 vs L3: phrase features", text)
        self.assertIn("| document_retrieval | 6 | 4 | 4 | 4 |", text)
        self.assertIn("| document_retrieval | 3 | 5 | 5 | 5 |", text)
        self.assertIn("Source: run `a`, `confusion.json`", text)

    def test_errors_cover_selected_configs_sorted_with_text(self):
        code, output = self.report()
        self.assertEqual(code, 0)
        errors = [
            json.loads(x)
            for x in (self.root / "results/a-report/errors.jsonl")
            .read_text()
            .splitlines()
        ]
        selected = {
            f["chosen"]
            for f in json.loads(self.selection.read_text())["families"].values()
        }
        self.assertEqual({e["configuration"] for e in errors} - selected, set())
        self.assertEqual(
            [e["query_id"] for e in errors], sorted(e["query_id"] for e in errors)
        )
        self.assertTrue(all("zzheldoutzz" in e["text"] for e in errors))
        self.assertTrue(all(e["label"] != e["prediction"] for e in errors))
        self.assertIn("B0: 7 validation errors", output)
        self.assertNotIn("zzheldoutzz", output)

    def test_report_has_no_out_option(self):
        with (
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            self.cli(
                "report",
                "--run",
                "r",
                "--selection",
                "s",
                "--train",
                "t",
                "--validation",
                "v",
                "--out",
                str(self.root / "x"),
            )

    def test_refuses_validation_file_that_differs_from_provenance(self):
        other = self.root / "other.jsonl"
        other.write_text((self.root / "validation.jsonl").read_text() + "\n")
        code, output = self.report(validation=other)
        self.assertEqual(code, 1)
        self.assertIn("does not match run a validation_sha256", output)
        self.assertFalse((self.root / "results/a-report").exists())

    def test_refuses_existing_output_directory(self):
        (self.root / "results/a-report").mkdir()
        code, output = self.report()
        self.assertEqual(code, 1)
        self.assertIn("already exists; report needs a new directory", output)

    def test_refuses_selection_that_does_not_match_the_run(self):
        selection = json.loads(self.selection.read_text())
        selection["overall"]["chosen"] = "B0"
        self.selection.write_text(json.dumps(selection))
        code, output = self.report()
        self.assertEqual(code, 1)
        self.assertIn("does not match the selection of run a", output)

    def test_invalid_selection_still_writes_files_but_exits_1(self):
        config = {**self.config(), "configurations": CONFIGURATIONS}
        self.config_path.write_text(json.dumps(config))
        self.assertEqual(self.run_id("b")[0], 0)
        run_b, selection_b = self.root / "results/b", self.root / "selection-b.json"
        code, _ = self.cli("select", "--run", str(run_b), "--out", str(selection_b))
        self.assertEqual(code, 1)
        code, output = self.report(run_dir=run_b, selection=selection_b)
        self.assertEqual(code, 1)
        self.assertIn("INVALID selection: ", output)
        self.assertIn("S1-C10", output)
        text = (self.root / "results/b-report/comparison.md").read_text()
        self.assertTrue(text.startswith("# INVALID selection: Validation comparison"))
        self.assertTrue((self.root / "results/b-report/errors.jsonl").is_file())


class ThreadWarningTest(RunTestCase):
    def test_run_warns_when_a_thread_variable_is_unset(self):
        env = {k: "1" for k in experiment.THREAD_VARS}
        del env["VECLIB_MAXIMUM_THREADS"]
        with mock.patch.dict(os.environ, env, clear=True):
            code, output = self.run_id("a")
        self.assertEqual(code, 0)
        self.assertIn(
            "WARNING: thread variables not set before start: VECLIB_MAXIMUM_THREADS\n",
            output,
        )
        provenance = self.result("a", "provenance.json")
        self.assertIsNone(provenance["thread_env"]["VECLIB_MAXIMUM_THREADS"])
        self.assertIsInstance(provenance["threadpools"], list)

    def test_no_warning_when_all_set(self):
        env = {k: "1" for k in experiment.THREAD_VARS}
        with mock.patch.dict(os.environ, env, clear=True):
            _, output = self.run_id("a")
        self.assertNotIn("WARNING", output)


if __name__ == "__main__":
    unittest.main()
