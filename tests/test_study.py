import json
import tempfile
import unittest
from pathlib import Path

from orchestra.data import LABELS
from orchestra.study import prepare_review, status


def rows():
    return [
        {
            "query_id": f"q{n}-{i}",
            "group_id": f"g{n}-{i}",
            "text": f"Query {n} {i}",
            "label": label,
            "status": "accepted",
            "source_id": "s",
            "rationale": "Private rationale",
            "annotator_ids": ["author"],
            "annotation_version": "v1",
        }
        for n, label in enumerate(LABELS)
        for i in range(6)
    ]


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dataset = self.root / "data.jsonl"
        self.sources = self.root / "sources.json"
        self.review = self.root / "review.jsonl"
        self.sources.write_text(
            json.dumps({"s": {"author": "a", "created": "2026-10-22", "license": None}})
        )
        self.write_rows(rows())
        self.review.write_text("")

    def write_rows(self, values):
        self.dataset.write_text("".join(json.dumps(r) + "\n" for r in values))

    def test_status_missing_and_permission_are_actionable(self):
        result = status(self.dataset, self.sources, self.review)
        self.assertFalse(result["ready"])
        self.assertTrue(any("permission" in b for b in result["blockers"]))
        self.assertTrue(result["next_action"])
        self.dataset.unlink()
        self.assertIn(
            "missing",
            " ".join(status(self.dataset, self.sources, self.review)["blockers"]),
        )

    def test_blind_sample_is_deterministic_and_separate(self):
        a = prepare_review(self.dataset, self.sources, self.root / "a")
        b = prepare_review(self.dataset, self.sources, self.root / "b")
        worksheet = (a / "reviewer.jsonl").read_text()
        self.assertEqual(worksheet, (b / "reviewer.jsonl").read_text())
        selected = [json.loads(line) for line in worksheet.splitlines()]
        self.assertEqual(len(selected), 8)
        self.assertTrue(all(set(r) == {"query_id", "text"} for r in selected))
        steward = json.loads((a / "steward.json").read_text())
        self.assertEqual(len(steward["original_labels"]), 8)
        self.assertNotIn("reviewer_id", worksheet)
        with self.assertRaises(FileExistsError):
            prepare_review(self.dataset, self.sources, a)

    def test_mixed_groups_extra_and_unresolved_are_explicit(self):
        values = rows()
        values[0]["group_id"] = values[6]["group_id"] = "mixed"
        values.append(
            {
                **values[1],
                "query_id": "ambiguous",
                "group_id": "amb",
                "text": "Unclear query",
                "label": None,
                "status": "needs_review",
            }
        )
        self.write_rows(values)
        out = prepare_review(
            self.dataset, self.sources, self.root / "out", extra_ids=["ambiguous"]
        )
        sheet = [
            json.loads(line)
            for line in (out / "reviewer.jsonl").read_text().splitlines()
        ]
        self.assertTrue(
            {values[0]["query_id"], values[6]["query_id"], "ambiguous"}
            <= {r["query_id"] for r in sheet}
        )
        self.assertIn("ambiguous", (out / "steward.json").read_text())
        with self.assertRaises(ValueError):
            prepare_review(
                self.dataset, self.sources, self.root / "bad", extra_ids=["missing"]
            )
        self.assertFalse((self.root / "bad").exists())

    def test_status_accepts_real_consistent_readiness_evidence(self):
        values = []
        reviews = []
        for n, label in enumerate(LABELS):
            for i in range(30):
                row = {
                    **rows()[n * 6],
                    "query_id": f"ready{n}-{i}",
                    "group_id": f"independent{n}-{i}",
                    "text": f"Ready query {n} {i}",
                }
                values.append(row)
                if i < 6:
                    reviews.append(
                        {
                            "query_id": row["query_id"],
                            "original_label": label,
                            "review_label": label,
                            "resolved_label": label,
                            "reviewer_id": "reviewer",
                            "review_date": "2026-10-22",
                            "review_kind": "second_human",
                        }
                    )
        self.write_rows(values)
        self.sources.write_text(
            json.dumps(
                {
                    "s": {
                        "author": "a",
                        "created": "2026-10-22",
                        "license": "test fixture permission",
                    }
                }
            )
        )
        self.review.write_text("".join(json.dumps(r) + "\n" for r in reviews))
        self.assertTrue(status(self.dataset, self.sources, self.review)["ready"])
        reviews[0]["reviewer_id"] = "author"
        self.review.write_text("".join(json.dumps(r) + "\n" for r in reviews))
        result = status(self.dataset, self.sources, self.review)
        self.assertFalse(result["ready"])
        self.assertIn("annotator", " ".join(result["blockers"]))

    def ready_fixture(self):
        values, reviews = [], []
        for n, label in enumerate(LABELS):
            for i in range(30):
                row = {
                    **rows()[n * 6],
                    "query_id": f"r{n}-{i}",
                    "group_id": f"rg{n}-{i}",
                    "text": f"ready text {n} {i}",
                }
                values.append(row)
                if i < 6:
                    reviews.append(
                        {
                            "query_id": row["query_id"],
                            "original_label": label,
                            "review_label": label,
                            "resolved_label": label,
                            "reviewer_id": "reviewer",
                            "review_date": "2026-10-22",
                            "review_kind": "second_human",
                        }
                    )
        self.write_rows(values)
        self.sources.write_text(
            json.dumps(
                {"s": {"author": "a", "created": "2026-10-22", "license": "fixture"}}
            )
        )
        self.review.write_text("".join(json.dumps(r) + "\n" for r in reviews))

    def config_fixture(self):
        config = {
            "dataset": str(self.dataset),
            "sources": str(self.sources),
            "seed": 42,
            "split_manifest": str(self.root / "split.json"),
            "train": str(self.root / "train/rows.jsonl"),
            "validation": str(self.root / "validation/rows.jsonl"),
            "sealed_test": str(self.root / "sealed/rows.jsonl"),
            "results_dir": str(self.root / "results"),
            "configurations": [{"family": "B0"}],
        }
        path = self.root / "config.json"
        path.write_text(json.dumps(config))
        brief = self.root / "brief.md"
        brief.write_text(
            "Collect independently written scenarios from the predeclared action boundaries."
        )
        return path, brief, config

    def test_prepare_gates_and_materializes_without_changing_draft(self):
        from orchestra.study import prepare

        config, brief, _ = self.config_fixture()
        original = config.read_bytes()
        out = self.root / "resolved.json"
        with self.assertRaises(ValueError):
            prepare(config, self.review, brief, out)
        self.assertFalse(out.exists())
        self.assertFalse((self.root / "split.json").exists())
        self.ready_fixture()
        prepared = prepare(config, self.review, brief, out)
        resolved = json.loads(prepared.read_text())
        self.assertEqual(config.read_bytes(), original)
        self.assertEqual(len(resolved["collection_brief_sha256"]), 64)
        from orchestra.data import file_sha256

        self.assertEqual(
            resolved["study_evidence"],
            {
                "format_version": 1,
                "ready": True,
                "dataset_sha256": file_sha256(self.dataset),
                "sources_sha256": file_sha256(self.sources),
                "review_sha256": file_sha256(self.review),
                "collection_brief_sha256": file_sha256(brief),
            },
        )
        self.assertTrue((self.root / "sealed/rows.jsonl").is_file())
        self.assertTrue(Path(resolved["dataset"]).is_absolute())
        self.assertEqual(prepare(config, self.review, brief, out), out.resolve())

    def test_prepare_refuses_alias_empty_brief_and_changed_output(self):
        from orchestra.study import prepare

        self.ready_fixture()
        config, brief, values = self.config_fixture()
        with self.assertRaises(ValueError):
            prepare(config, self.review, brief, self.dataset)
        values["train"] = str(self.dataset)
        config.write_text(json.dumps(values))
        with self.assertRaises(ValueError):
            prepare(config, self.review, brief, self.root / "resolved.json")
        self.assertFalse((self.root / "resolved.json").exists())
        config, brief, _ = self.config_fixture()
        brief.write_text(" \n")
        with self.assertRaises(ValueError):
            prepare(config, self.review, brief, self.root / "resolved.json")

    def test_prepare_checks_parent_hash_before_writing(self):
        from orchestra.study import prepare

        self.ready_fixture()
        path, brief, config = self.config_fixture()
        parent = self.root / "parent.json"
        parent.write_text("{}")
        config.update(
            parent_manifest=str(parent),
            parent_dataset=str(self.dataset),
            parent_manifest_sha256="wrong",
        )
        path.write_text(json.dumps(config))
        out = self.root / "resolved.json"
        with self.assertRaisesRegex(ValueError, "parent_manifest_sha256"):
            prepare(path, self.review, brief, out)
        self.assertFalse(out.exists())
        self.assertFalse((self.root / "split.json").exists())

    def test_prepare_resolves_relative_paths_from_working_directory(self):
        import contextlib

        from orchestra.study import prepare

        self.ready_fixture()
        path, brief, config = self.config_fixture()
        for key in (
            "dataset",
            "sources",
            "split_manifest",
            "train",
            "validation",
            "sealed_test",
            "results_dir",
        ):
            config[key] = str(Path(config[key]).relative_to(self.root))
        path.write_text(json.dumps(config))
        with contextlib.chdir(self.root):
            out = prepare("config.json", "review.jsonl", "brief.md", "resolved.json")
        self.assertEqual(
            Path(json.loads(out.read_text())["dataset"]), self.dataset.resolve()
        )
        brief.write_text("Changed collection brief")
        with (
            contextlib.chdir(self.root),
            self.assertRaisesRegex(ValueError, "immutable"),
        ):
            prepare(path, self.review, brief, out)
