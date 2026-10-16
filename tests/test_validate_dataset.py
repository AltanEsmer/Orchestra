import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import main, read_jsonl, summarize, validate

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


def row(query_id, group_id, label, status="accepted"):
    return {
        "query_id": query_id,
        "group_id": group_id,
        "label": label,
        "status": status,
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

    def test_source_with_null_license(self):
        sources = copy.deepcopy(SOURCES)
        sources["s1"]["license"] = None
        self.assertEqual(validate(rows(), sources), ["source s1: missing license"])


class SummarizeTest(unittest.TestCase):
    def test_counts_and_mixed_groups(self):
        data = [
            row("q1", "g1", "calculation"),
            row("q2", "g1", "direct_answer"),
            row("q3", "g2", "calculation"),
            row("q4", "g3", None, status="needs_review"),
            row("q5", "g3", "knowledge_lookup", status="excluded"),
        ]
        self.assertEqual(
            summarize(data),
            {
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
            },
        )


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

    def run_main(self, dataset):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main([dataset, "--sources", str(self.sources)])
        return code, output.getvalue()

    def test_read_jsonl_reports_bad_lines(self):
        path = self.write("data.jsonl", ['{"a": 1}', "", "not json", "[1, 2]"])
        self.assertEqual(
            read_jsonl(path),
            ([{"a": 1}], ["line 3: not a JSON object", "line 4: not a JSON object"]),
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
        self.assertEqual(output, "ERROR: line 2: not a JSON object\nFAIL: 1 errors\n")

    def test_main_reports_missing_file(self):
        code, output = self.run_main(str(self.folder / "absent.jsonl"))
        self.assertEqual(code, 1)
        self.assertTrue(output.startswith("ERROR: cannot read"))


if __name__ == "__main__":
    unittest.main()
