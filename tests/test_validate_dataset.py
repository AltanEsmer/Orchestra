import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import (
    agreement,
    main,
    read_jsonl,
    readiness,
    summarize,
    validate,
    validate_reviews,
)

SOURCES = {"s1": {"author": "altan", "license": "CC-BY-4.0", "created": "2026-10-01"}}
VALID_ROWS = [
    {
        "query_id": "q0001",
        "group_id": "g01",
        "text": "What is 17% of 240?",
        "label": "calculation",
        "status": "accepted",
        "source_id": "s1",
        "rationale": "Needs arithmetic.",
        "annotator_ids": ["a1"],
        "annotation_version": "v1",
    },
    {
        "query_id": "q0002",
        "group_id": "g02",
        "text": "Summarize section 3 of the attached contract.",
        "label": "document_retrieval",
        "status": "accepted",
        "source_id": "s1",
        "rationale": "Needs the user's document.",
        "annotator_ids": ["a1", "a2"],
        "annotation_version": "v1",
    },
]


def rows():
    return copy.deepcopy(VALID_ROWS)


def row(query_id, group_id, label, status="accepted", text="a b", source_id="s1"):
    return {
        "query_id": query_id,
        "group_id": group_id,
        "label": label,
        "status": status,
        "text": text,
        "source_id": source_id,
        "rationale": f"why {query_id}",
    }


def review(query_id, original, reviewed=None, resolved=None, kind="second_human"):
    return {
        "query_id": query_id,
        "original_label": original,
        "review_label": reviewed or original,
        "reviewer_id": "r1",
        "review_date": "2026-10-20",
        "review_kind": kind,
        "resolved_label": resolved or original,
    }


class ValidateTest(unittest.TestCase):
    def test_valid_rows_have_no_errors(self):
        self.assertEqual(validate(rows(), SOURCES), [])

    def test_missing_field(self):
        data = rows()
        del data[0]["rationale"]
        self.assertEqual(validate(data, SOURCES), ["q0001: missing fields rationale"])

    def test_duplicate_query_id(self):
        data = rows()
        data[1]["query_id"] = "q0001"
        self.assertEqual(validate(data, SOURCES), ["q0001: duplicate query_id"])

    def test_empty_text(self):
        data = rows()
        data[0]["text"] = "   "
        self.assertEqual(validate(data, SOURCES), ["q0001: empty text"])

    def test_accepted_row_needs_label(self):
        data = rows()
        data[0]["label"] = None
        self.assertEqual(validate(data, SOURCES), ["q0001: accepted row has no label"])

    def test_unknown_label(self):
        data = rows()
        data[0]["label"] = "web_search"
        self.assertEqual(validate(data, SOURCES), ["q0001: unknown label web_search"])

    def test_unresolved_row_may_have_null_label(self):
        data = rows()
        data[0]["label"] = None
        data[0]["status"] = "needs_review"
        self.assertEqual(validate(data, SOURCES), [])

    def test_duplicate_text_after_normalization(self):
        data = rows()
        data[1]["text"] = "  what is 17%   OF 240? "
        self.assertEqual(validate(data, SOURCES), ["q0002: same text as q0001"])

    def test_group_larger_than_limit(self):
        data = []
        for number in range(1, 6):
            extra = copy.deepcopy(VALID_ROWS[0])
            extra["query_id"] = f"q{number}"
            extra["text"] = f"What is {number}% of 240?"
            data.append(extra)
        self.assertEqual(validate(data, SOURCES), ["group g01: 5 rows exceeds 4"])

    def test_draft_source_without_license_is_structurally_valid(self):
        sources = copy.deepcopy(SOURCES)
        sources["s1"]["license"] = None
        self.assertEqual(validate(rows(), sources), [])

    def test_source_without_author(self):
        sources = copy.deepcopy(SOURCES)
        sources["s1"]["author"] = None
        self.assertEqual(validate(rows(), sources), ["source s1: missing author"])


class SummarizeTest(unittest.TestCase):
    def test_counts_and_mixed_groups(self):
        data = [
            row("q1", "g1", "calculation", text="one"),
            row("q2", "g1", "direct_answer", text="one two three"),
            row("q3", "g2", "calculation", text="one two", source_id="s2"),
            row("q4", "g3", None, status="needs_review"),
            row("q5", "g3", "knowledge_lookup", status="excluded"),
        ]
        self.assertEqual(
            summarize(data, "abc"),
            {
                "sha256": "abc",
                "rows": 5,
                "status": {"accepted": 3, "needs_review": 1, "excluded": 1},
                "accepted_by_label": {
                    "document_retrieval": 0,
                    "knowledge_lookup": 0,
                    "calculation": 2,
                    "direct_answer": 1,
                },
                "groups_by_label": {
                    "document_retrieval": 0,
                    "knowledge_lookup": 0,
                    "calculation": 2,
                    "direct_answer": 1,
                },
                "mixed_label_groups": ["g1"],
                "words": {"min": 1, "median": 2, "max": 3},
                "source_mix": {"s1": 2, "s2": 1},
                "group_sizes": {1: 1, 2: 1},
                "excluded": [{"query_id": "q5", "rationale": "why q5"}],
            },
        )

    def test_no_accepted_rows_has_no_length_stats(self):
        summary = summarize([row("q1", "g1", None, status="needs_review")], "abc")
        self.assertEqual(summary["words"], {"min": None, "median": None, "max": None})


L = ("document_retrieval", "knowledge_lookup", "calculation", "direct_answer")
# One accepted row and group per class, every row reviewed.
READY_ROWS = [row(f"q{i}", f"g{i}", label) for i, label in enumerate(L)]
READY_REVIEWS = [review(f"q{i}", label) for i, label in enumerate(L)]
SMALL = {"accepted": 4, "per_class": 1, "groups_per_class": 1, "review_fraction": 0.5}
LICENSED = {"s1": {"author": "a", "license": "MIT", "created": "2026-10-01"}}


class ReadinessTest(unittest.TestCase):
    def check(self, data=None, sources=None, reviews=None, requirements=SMALL):
        return readiness(
            copy.deepcopy(READY_ROWS if data is None else data),
            copy.deepcopy(LICENSED if sources is None else sources),
            copy.deepcopy(READY_REVIEWS if reviews is None else reviews),
            requirements,
        )

    def test_ready_fixture_passes(self):
        self.assertEqual(self.check(), [])

    def test_empty_dataset(self):
        self.assertEqual(
            self.check(data=[], reviews=[]),
            ["no accepted rows: the training dataset is empty"],
        )

    def test_too_few_accepted_rows(self):
        errors = self.check(requirements={**SMALL, "accepted": 5})
        self.assertEqual(errors, ["4 accepted rows, need 5"])

    def test_missing_class(self):
        errors = self.check(data=READY_ROWS[:3], reviews=READY_REVIEWS[:3])
        self.assertIn("direct_answer: 0 accepted rows, need 1", errors)
        self.assertIn("direct_answer: 0 groups, need 1", errors)

    def test_too_few_groups_in_class(self):
        data = READY_ROWS + [row("q9", "g0", "document_retrieval", text="x y")]
        errors = self.check(data=data, requirements={**SMALL, "groups_per_class": 2})
        self.assertEqual(
            errors,
            [f"{label}: 1 groups, need 2" for label in L],
        )

    def test_unresolved_row_remains(self):
        data = READY_ROWS + [row("q9", "g9", None, status="needs_review")]
        self.assertEqual(self.check(data=data), ["1 rows still need review"])

    def test_missing_permission(self):
        sources = {"s1": {"author": "a", "license": None, "created": "2026-10-01"}}
        self.assertEqual(
            self.check(sources=sources), ["source s1: no license, permission missing"]
        )

    def test_review_fraction_rounds_up_per_class(self):
        data = READY_ROWS + [row("q9", "g9", "calculation", text="x y")]
        reviews = READY_REVIEWS  # 1 of 2 calculation rows reviewed
        errors = self.check(
            data=data, reviews=reviews, requirements={**SMALL, "review_fraction": 0.6}
        )
        self.assertEqual(errors, ["calculation: 1 reviewed rows, need 2"])

    def test_missing_review_evidence(self):
        errors = self.check(reviews=[])
        self.assertEqual(
            errors,
            [f"{label}: 0 reviewed rows, need 1" for label in L]
            + ["no review evidence"],
        )

    def test_ledger_must_agree_with_dataset_label(self):
        reviews = copy.deepcopy(READY_REVIEWS)
        reviews[2]["resolved_label"] = "direct_answer"
        self.assertEqual(
            self.check(reviews=reviews),
            [
                "q2: ledger resolved direct_answer but dataset accepted row expects calculation"
            ],
        )

    def test_excluded_row_must_resolve_to_null(self):
        data = READY_ROWS + [row("q9", "g9", None, status="excluded")]
        good = READY_REVIEWS + [review("q9", "calculation", resolved=None)]
        good[-1]["resolved_label"] = None
        self.assertEqual(self.check(data=data, reviews=good), [])
        bad = READY_REVIEWS + [review("q9", "calculation")]
        self.assertEqual(
            self.check(data=data, reviews=bad),
            ["q9: ledger resolved calculation but dataset excluded row expects None"],
        )

    def test_mixed_label_group_needs_review_of_every_row(self):
        data = [
            row("q0", "g0", "document_retrieval"),
            row("q1", "g0", "knowledge_lookup"),
            row("q2", "g2", "calculation"),
            row("q3", "g3", "direct_answer"),
        ]
        reviews = [review(f"q{i}", data[i]["label"]) for i in (0, 2, 3)]
        self.assertEqual(
            self.check(
                data=data,
                reviews=reviews,
                requirements={**SMALL, "review_fraction": 0},
            ),
            ["group g0: mixed labels need review of q1"],
        )


class ReviewLedgerTest(unittest.TestCase):
    def test_valid_ledger(self):
        self.assertEqual(validate_reviews(READY_REVIEWS, READY_ROWS), [])

    def test_bad_entries(self):
        bad = [
            {**review("q0", "calculation"), "review_kind": "friend"},
            {**review("q1", "calculation"), "review_date": "20/10/2026"},
            {**review("q2", "calculation"), "review_label": "web_search"},
            {**review("q3", "calculation"), "reviewer_id": " "},
            review("q404", "calculation"),
            review("q0", "calculation"),
            {**review("q1", "calculation"), "extra": 1},
        ]
        del bad[6]["reviewer_id"]
        self.assertEqual(
            validate_reviews(bad, READY_ROWS),
            [
                "q0: unknown review_kind 'friend'",
                "q1: review_date must be YYYY-MM-DD",
                "q2: review review_label 'web_search' is not a label",
                "q3: review empty reviewer_id",
                "q404: review for unknown query_id",
                "q0: duplicate review",
                "q1: review missing fields reviewer_id",
                "q1: review unknown fields extra",
            ],
        )

    def test_null_resolved_label_only(self):
        ok = {**review("q0", "calculation"), "resolved_label": None}
        self.assertEqual(validate_reviews([ok], READY_ROWS), [])
        bad = {**review("q1", "calculation"), "original_label": None}
        self.assertEqual(
            validate_reviews([bad], READY_ROWS),
            ["q1: review original_label None is not a label"],
        )

    def test_second_human_must_not_be_an_annotator(self):
        data = copy.deepcopy(READY_ROWS)
        data[0]["annotator_ids"] = ["r1"]
        self.assertEqual(
            validate_reviews(READY_REVIEWS[:1], data),
            ["q0: second_human reviewer is an annotator"],
        )
        delayed = [review("q0", "document_retrieval", kind="delayed_self")]
        self.assertEqual(validate_reviews(delayed, data), [])

    def test_unhashable_query_ids_do_not_crash(self):
        data = copy.deepcopy(READY_ROWS)
        data[0]["query_id"] = ["q0"]
        bad = {**review("q1", "calculation"), "query_id": ["q1"]}
        self.assertEqual(
            validate_reviews([bad], data),
            ["['q1']: review empty query_id"],
        )


class AgreementTest(unittest.TestCase):
    def test_three_of_four_match(self):
        reviews = [
            review("q1", "calculation"),
            review("q2", "calculation"),
            review("q3", "calculation", kind="delayed_self"),
            review("q4", "calculation", reviewed="direct_answer"),
        ]
        self.assertEqual(
            agreement(reviews),
            {
                "matching": 3,
                "reviewed": 4,
                "rate": 0.75,
                "by_kind": {
                    "second_human": {"matching": 2, "reviewed": 3},
                    "delayed_self": {"matching": 1, "reviewed": 1},
                },
            },
        )

    def test_empty_ledger_has_no_rate(self):
        self.assertIsNone(agreement([])["rate"])


class FileTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.folder = Path(directory.name)
        self.sources = self.folder / "sources.json"
        self.sources.write_text(json.dumps(SOURCES), encoding="utf-8")

    def write(self, name, lines):
        path = self.folder / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(path)

    def run_main(self, dataset, *extra):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main([dataset, "--sources", str(self.sources), *extra])
        return code, output.getvalue()

    def test_read_jsonl_reports_bad_lines(self):
        path = self.write("data.jsonl", ['{"a": 1}', "", "not json", "[1, 2]"])
        self.assertEqual(
            read_jsonl(path),
            (
                [{"a": 1}],
                [
                    f"{path} line 3: not a JSON object",
                    f"{path} line 4: not a JSON object",
                ],
            ),
        )

    def test_main_passes_valid_file(self):
        path = self.write("data.jsonl", [json.dumps(r) for r in VALID_ROWS])
        code, output = self.run_main(path)
        self.assertEqual(code, 0)
        self.assertTrue(output.endswith("PASS: 2 rows valid\n"))

    def test_main_fails_invalid_file(self):
        path = self.write("data.jsonl", [json.dumps(VALID_ROWS[0]), "oops"])
        code, output = self.run_main(path)
        self.assertEqual(code, 1)
        self.assertEqual(
            output, f"ERROR: {path} line 2: not a JSON object\nFAIL: 1 errors\n"
        )

    def test_ready_requires_review(self):
        path = self.write("data.jsonl", [json.dumps(r) for r in VALID_ROWS])
        with (
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit) as raised,
        ):
            self.run_main(path, "--ready")
        self.assertEqual(raised.exception.code, 2)

    def test_review_prints_agreement(self):
        path = self.write("data.jsonl", [json.dumps(r) for r in VALID_ROWS])
        ledger = self.write(
            "ledger.jsonl", [json.dumps(review("q0001", "calculation"))]
        )
        code, output = self.run_main(path, "--review", ledger)
        self.assertEqual(code, 0)
        self.assertIn('"matching": 1', output)
        self.assertIn('"rate": 1.0', output)
        self.assertTrue(output.endswith("PASS: 2 rows valid\n"))

    def test_ready_fails_small_dataset(self):
        path = self.write("data.jsonl", [json.dumps(r) for r in VALID_ROWS])
        ledger = self.write(
            "ledger.jsonl", [json.dumps(review("q0001", "calculation"))]
        )
        code, output = self.run_main(path, "--review", ledger, "--ready")
        self.assertEqual(code, 1)
        self.assertIn("ERROR: 2 accepted rows, need 120\n", output)
        self.assertIn("ERROR: knowledge_lookup: 0 accepted rows, need 30\n", output)

    def test_bad_ledger_fails(self):
        path = self.write("data.jsonl", [json.dumps(r) for r in VALID_ROWS])
        ledger = self.write(
            "ledger.jsonl", [json.dumps(review("q9999", "calculation"))]
        )
        code, output = self.run_main(path, "--review", ledger)
        self.assertEqual(code, 1)
        self.assertEqual(
            output, "ERROR: q9999: review for unknown query_id\nFAIL: 1 errors\n"
        )

    def test_malformed_query_ids_fail_cleanly(self):
        rows_ = [{**VALID_ROWS[0], "query_id": ["q1"]}, VALID_ROWS[1]]
        path = self.write("data.jsonl", [json.dumps(r) for r in rows_])
        bad = {**review("q0002", "document_retrieval"), "query_id": ["q0002"]}
        ledger = self.write("ledger.jsonl", [json.dumps(bad)])
        code, output = self.run_main(path, "--review", ledger)
        self.assertEqual(code, 1)
        self.assertIn("ERROR: ['q0002']: review empty query_id\n", output)
        self.assertTrue(output.endswith("errors\n"))

    def test_ready_passes_full_size_fixture(self):
        data, ledger = [], []
        for number, label in enumerate(L * 30, start=1):
            qid = f"q{number:03d}"
            data.append(
                {
                    **VALID_ROWS[0],
                    "query_id": qid,
                    "group_id": f"g{number:03d}",
                    "text": f"distinct text {number}",
                    "label": label,
                }
            )
            if number % 3 == 0:
                ledger.append(review(qid, label))
        path = self.write("data.jsonl", [json.dumps(r) for r in data])
        review_path = self.write("ledger.jsonl", [json.dumps(r) for r in ledger])
        sources = {"s1": {**SOURCES["s1"]}}
        self.sources.write_text(json.dumps(sources), encoding="utf-8")
        code, output = self.run_main(path, "--review", review_path, "--ready")
        self.assertEqual(code, 0, output)
        self.assertTrue(
            output.endswith(
                "PASS: M1 readiness checks passed (120 accepted rows, 40 reviewed)\n"
            )
        )
        self.assertIn('"ledger_sha256"', output)

    def test_main_reports_missing_file(self):
        code, output = self.run_main(str(self.folder / "absent.jsonl"))
        self.assertEqual(code, 1)
        self.assertTrue(output.startswith("ERROR: cannot read"))


if __name__ == "__main__":
    unittest.main()
