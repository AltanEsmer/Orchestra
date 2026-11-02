import contextlib
import http.client
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_splits import DIGEST, fixture_rows

from orchestra import jev
from orchestra.__main__ import main
from orchestra.data import LABELS, file_sha256
from orchestra.splits import make_split, materialize


def answer(choice="calculation", probabilities=(0.1, 0.2, 0.6, 0.1)):
    return {
        "model": "jev-1.14.0",
        "answers": {
            "first_action": {
                "type": "choice",
                "choice": choice,
                "confidence": max(probabilities),
                "probabilities": dict(zip(LABELS, probabilities)),
            }
        },
        "usage": {"input_tokens": 10, "output_tokens": 1},
    }


def ok_send(body):
    return 200, answer()


class RunTestCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        rows = fixture_rows()
        manifest = make_split(rows, DIGEST)
        materialize(
            manifest,
            rows,
            self.root / "train.jsonl",
            self.root / "validation.jsonl",
            self.root / "sealed" / "test.jsonl",
        )
        (self.root / "split.json").write_text(json.dumps(manifest))
        self.config_path = self.root / "config.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "split_manifest": str(self.root / "split.json"),
                    "train": str(self.root / "train.jsonl"),
                    "validation": str(self.root / "validation.jsonl"),
                    "sealed_test": str(self.root / "sealed" / "test.jsonl"),
                }
            )
        )

    def cli(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(list(argv))
        return code, output.getvalue()


class RequestBodyTest(unittest.TestCase):
    def test_body_holds_only_the_frozen_prompt_and_the_query(self):
        body = jev.request_body("What is 2 + 2?")
        self.assertEqual(body["model"], "jev-1.14.0")
        self.assertEqual(body["state"], {"query": "What is 2 + 2?"})
        question = body["questions"]["first_action"]
        self.assertEqual(question["type"], "choice")
        self.assertEqual(list(question["criteria"]), list(LABELS))
        self.assertEqual(set(body), {"model", "state", "questions"})


class ParseTest(unittest.TestCase):
    def test_probabilities_follow_label_order_whatever_the_key_order(self):
        payload = answer()
        shuffled = payload["answers"]["first_action"]["probabilities"]
        payload["answers"]["first_action"]["probabilities"] = dict(
            reversed(list(shuffled.items()))
        )
        parsed = jev.parse(payload)
        self.assertEqual(parsed["probabilities"], [0.1, 0.2, 0.6, 0.1])
        self.assertEqual(parsed["choice"], "calculation")
        self.assertEqual(parsed["usage"], {"input_tokens": 10, "output_tokens": 1})

    def test_invalid_answers_raise(self):
        def edit(change):
            payload = answer()
            change(payload["answers"]["first_action"], payload)
            return payload

        cases = {
            "missing": edit(lambda a, p: p["answers"].clear()),
            "not a choice": edit(lambda a, p: a.update(type="text")),
            "unknown label": edit(lambda a, p: a.update(choice="search")),
            "extra key": edit(lambda a, p: a["probabilities"].update(extra=0.0)),
            "negative": edit(
                lambda a, p: a["probabilities"].update(
                    document_retrieval=-0.1, calculation=0.8
                )
            ),
            "above one": edit(lambda a, p: a["probabilities"].update(calculation=1.5)),
            "nan": edit(
                lambda a, p: a["probabilities"].update(calculation=float("nan"))
            ),
            "bad sum": edit(lambda a, p: a["probabilities"].update(calculation=0.5)),
        }
        for name, payload in cases.items():
            with self.subTest(name), self.assertRaises(ValueError):
                jev.parse(payload)


class CollectTestCase(RunTestCase):
    def setUp(self):
        super().setUp()
        self.log = self.root / "jev.jsonl"
        self.validation = [
            json.loads(line)
            for line in (self.root / "validation.jsonl").read_text().splitlines()
        ]
        self.validation.sort(key=lambda r: r["query_id"])

    def lines(self):
        return [json.loads(x) for x in self.log.read_text().splitlines()]


class CollectTest(CollectTestCase):
    def test_cap_limits_requests_and_rerun_asks_only_for_missing_rows(self):
        sent = []

        def send(body):
            sent.append(body["state"]["query"])
            return 200, answer()

        total = len(self.validation)
        first = jev.collect(self.validation, self.log, 2, send)
        self.assertEqual(first["requests"], 2)
        self.assertEqual(first["answered"], 2)
        self.assertEqual(len(first["missing"]), total - 2)
        self.assertEqual(first["input_tokens"], 20)
        second = jev.collect(self.validation, self.log, 1000, send)
        self.assertEqual(second["requests"], total - 2)
        self.assertEqual(second["missing"], [])
        self.assertEqual(len(sent), total)
        self.assertEqual(len(set(sent)), total)

    def test_rejected_key_stops_after_one_request(self):
        for status in (401, 403):
            with self.subTest(status=status):
                self.log.unlink(missing_ok=True)
                sent = []

                def send(body, status=status, sent=sent):
                    sent.append(body)
                    return status, {"error": "invalid key"}

                summary = jev.collect(self.validation, self.log, 1000, send)
                self.assertEqual((summary["requests"], len(sent)), (1, 1))
                self.assertEqual(len(summary["missing"]), len(self.validation))
                self.assertEqual(self.lines()[0]["error"], f"HTTP status {status}")

    def test_invalid_response_is_logged_with_error_and_requested_again(self):
        rows = self.validation[:1]
        bad = jev.collect(rows, self.log, 5, lambda body: (200, {"answers": {}}))
        self.assertEqual(bad["missing"], [rows[0]["query_id"]])
        self.assertEqual(self.lines()[0]["error"], "no first_action answer")
        failed = jev.collect(rows, self.log, 5, lambda body: (500, "boom"))
        self.assertEqual(failed["requests"], 1)
        self.assertEqual(self.lines()[1]["error"], "HTTP status 500")
        good = jev.collect(rows, self.log, 5, ok_send)
        self.assertEqual(good["requests"], 1)
        self.assertEqual(good["missing"], [])
        self.assertIsNone(self.lines()[2]["error"])
        again = jev.collect(rows, self.log, 5, ok_send)
        self.assertEqual(again["requests"], 0)

    def test_log_lines_never_carry_the_label(self):
        jev.collect(self.validation, self.log, 3, ok_send)
        keys = {
            "query_id",
            "text_sha256",
            "requested_utc",
            "latency_seconds",
            "request",
            "status",
            "response",
            "error",
        }
        for line, row in zip(self.lines(), self.validation):
            self.assertEqual(set(line), keys)
            self.assertEqual(line["request"], jev.request_body(row["text"]))

    def test_answer_from_another_model_is_logged_and_requested_again(self):
        rows = self.validation[:1]
        stale = answer()
        stale["model"] = "jev-1.15.0"
        first = jev.collect(rows, self.log, 5, lambda body: (200, stale))
        self.assertEqual(first["missing"], [rows[0]["query_id"]])
        self.assertEqual(
            self.lines()[0]["error"], "answered by model jev-1.15.0, not jev-1.14.0"
        )
        again = jev.collect(rows, self.log, 5, ok_send)
        self.assertEqual(again["requests"], 1)
        self.assertEqual(again["missing"], [])

    def test_line_written_under_another_prompt_is_not_an_answer(self):
        rows = self.validation[:1]
        jev.collect(rows, self.log, 5, ok_send)
        line = self.lines()[0]
        line["request"]["questions"]["first_action"]["instructions"] = "older"
        self.log.write_text(json.dumps(line) + "\n")
        model = jev.Replay(str(self.log), file_sha256(self.log)).fit([])
        self.assertEqual(model.answers_, {})
        with self.assertRaisesRegex(ValueError, "1 queries have no valid"):
            model.predict([rows[0]["text"]])
        again = jev.collect(rows, self.log, 5, ok_send)
        self.assertEqual(again["requests"], 1)

    def test_line_for_changed_text_counts_as_missing(self):
        rows = [dict(self.validation[0])]
        jev.collect(rows, self.log, 5, ok_send)
        rows[0]["text"] += " edited"
        summary = jev.collect(rows, self.log, 0, ok_send)
        self.assertEqual(summary["missing"], [rows[0]["query_id"]])
        self.assertEqual(summary["answered"], 0)


class PostTest(unittest.TestCase):
    def test_incomplete_read_returns_no_status(self):
        error = http.client.IncompleteRead(b"par", 10)
        with mock.patch("urllib.request.urlopen", side_effect=error):
            status, reason = jev.post(jev.request_body("q"), "k")
        self.assertIsNone(status)
        self.assertIn("IncompleteRead", reason)


class ReplayTest(CollectTestCase):
    def replay(self, **changes):
        arguments = {
            "responses": str(self.log),
            "responses_sha256": file_sha256(self.log),
        }
        return jev.Replay(**{**arguments, **changes})

    def test_replay_returns_saved_answers_for_known_texts(self):
        rows = self.validation[:2]
        answers = iter([answer("direct_answer", (0, 0, 0.25, 0.75)), answer()])
        jev.collect(rows, self.log, 2, lambda body: (200, next(answers)))
        model = self.replay().fit([r["text"] for r in rows])
        texts = [rows[1]["text"], rows[0]["text"]]
        self.assertEqual(list(model.predict(texts)), ["calculation", "direct_answer"])
        self.assertEqual(
            model.predict_proba(texts).tolist(),
            [[0.1, 0.2, 0.6, 0.1], [0, 0, 0.25, 0.75]],
        )
        self.assertEqual(list(model.classes_), list(LABELS))

    def test_tampered_log_fails_to_fit(self):
        jev.collect(self.validation[:1], self.log, 1, ok_send)
        wrong = self.replay(responses_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "Jev responses changed"):
            wrong.fit([])

    def test_unknown_text_fails_without_a_fallback_label(self):
        jev.collect(self.validation[:1], self.log, 1, ok_send)
        model = self.replay().fit([])
        with self.assertRaisesRegex(ValueError, "1 queries have no valid"):
            model.predict(["never asked"])


class CliTest(RunTestCase):
    def jev_cli(self, *extra):
        return self.cli(
            "jev",
            "--config",
            str(self.config_path),
            "--log",
            str(self.root / "jev.jsonl"),
            "--max-requests",
            "3",
            *extra,
        )

    def test_missing_key_refuses_and_sends_nothing(self):
        environment = {k: v for k, v in os.environ.items() if k != jev.KEY_VARIABLE}
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(jev, "post", side_effect=AssertionError("network")),
        ):
            code, output = self.jev_cli()
        self.assertEqual(code, 1)
        self.assertIn("ERROR: TYPESAFE_API_KEY is not set", output)

    def test_dry_run_needs_no_key_and_prints_the_plan(self):
        environment = {k: v for k, v in os.environ.items() if k != jev.KEY_VARIABLE}
        with (
            mock.patch.dict(os.environ, environment, clear=True),
            mock.patch.object(jev, "post", side_effect=AssertionError("network")),
        ):
            code, output = self.jev_cli("--dry-run")
        self.assertEqual(code, 0)
        plan = json.loads(output)
        validation = (self.root / "validation.jsonl").read_text().splitlines()
        self.assertEqual(plan["validation_rows"], len(validation))
        self.assertEqual(plan["pending"], len(validation))
        self.assertEqual(plan["example_request"]["state"], {"query": "<query text>"})

    def test_log_inside_the_repository_and_not_ignored_is_refused(self):
        log = (
            Path(jev.__file__).resolve().parents[2] / "tests" / "zz_jev_unignored.jsonl"
        )
        self.addCleanup(lambda: log.unlink(missing_ok=True))
        for extra in ((), ("--dry-run",)):
            with mock.patch.object(jev, "post", side_effect=AssertionError("network")):
                code, output = self.cli(
                    "jev",
                    "--config",
                    str(self.config_path),
                    "--log",
                    str(log),
                    "--max-requests",
                    "3",
                    *extra,
                )
            self.assertEqual(code, 1)
            self.assertIn("ERROR:", output)
            self.assertFalse(log.exists())

    def test_real_mode_sends_up_to_the_cap_with_the_key(self):
        sends = []

        def fake_post(body, key):
            sends.append(key)
            return 200, answer()

        with (
            mock.patch.dict(os.environ, {jev.KEY_VARIABLE: "sk-test-SENTINEL-7f3a"}),
            mock.patch.object(jev, "post", fake_post),
        ):
            code, output = self.jev_cli()
        self.assertEqual(code, 1)  # cap 3 leaves rows missing
        self.assertEqual(sends, ["sk-test-SENTINEL-7f3a"] * 3)
        self.assertIn("log sha256:", output)
        self.assertNotIn("SENTINEL", output)
        self.assertNotIn("SENTINEL", (self.root / "jev.jsonl").read_text())


if __name__ == "__main__":
    unittest.main()
