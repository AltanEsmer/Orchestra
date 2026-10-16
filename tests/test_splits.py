import contextlib
import copy
import io
import json
import random
import tempfile
import unittest
from pathlib import Path

import sklearn

from orchestra.__main__ import main
from orchestra.data import LABELS
from orchestra.splits import FOLD_PARTITION, check_split, make_split

SOURCES = {"fixture": {"author": "test", "license": None, "created": "2026-10-01"}}
DIGEST = "a" * 64


def fixture_rows():
    """4 classes x 6 groups x 2 rows; groups 0 of two classes are mixed-label."""
    rows = []
    for label in LABELS:
        for group in range(6):
            for copy_ in range(2):
                row_label = label
                if group == 0 and copy_ == 1 and label in LABELS[:2]:
                    row_label = LABELS[3]  # mixed-label group
                query_id = f"{label[:3]}-g{group}-{copy_}"
                rows.append(
                    {
                        "query_id": query_id,
                        "group_id": f"{label[:3]}-g{group}",
                        "text": f"artificial fixture text {query_id}",
                        "label": row_label,
                        "status": "accepted",
                        "source_id": "fixture",
                        "rationale": "fixture",
                        "annotator_ids": ["fixture"],
                        "annotation_version": "v0",
                    }
                )
    return rows


def partition_of(manifest):
    return {q: name for name, ids in manifest["partitions"].items() for q in ids}


class MakeSplitTest(unittest.TestCase):
    def setUp(self):
        self.rows = fixture_rows()
        self.manifest = make_split(self.rows, DIGEST)

    def test_manifest_fields_and_counts(self):
        m = self.manifest
        self.assertEqual(m["manifest_version"], 1)
        self.assertEqual(m["dataset_sha256"], DIGEST)
        self.assertEqual((m["seed"], m["n_splits"]), (42, 5))
        self.assertEqual(m["algorithm"], "StratifiedGroupKFold")
        self.assertEqual(m["sklearn_version"], sklearn.__version__)
        self.assertEqual(m["class_order"], list(LABELS))
        self.assertEqual(
            m["fold_partition"],
            {"0": "train", "1": "train", "2": "train", "3": "validation", "4": "test"},
        )
        self.assertEqual(sum(len(ids) for ids in m["partitions"].values()), 48)
        for name, ids in m["partitions"].items():
            self.assertEqual(ids, sorted(ids))
            self.assertEqual(sum(m["counts"][name].values()), len(ids))
            self.assertEqual(m["proportions"][name], round(len(ids) / 48, 4))
        self.assertEqual(check_split(m, self.rows, DIGEST), [])

    def test_groups_stay_whole_including_mixed_labels(self):
        where = partition_of(self.manifest)
        by_group = {}
        for row in self.rows:
            by_group.setdefault(row["group_id"], set()).add(where[row["query_id"]])
        self.assertTrue(all(len(names) == 1 for names in by_group.values()))
        mixed = {"doc-g0", "kno-g0"}
        for group in mixed:
            labels = {r["label"] for r in self.rows if r["group_id"] == group}
            self.assertEqual(len(labels), 2)

    def test_fold_three_is_validation_and_fold_four_is_test(self):
        # Re-derive folds with the library and check literal assignment.
        from sklearn.model_selection import StratifiedGroupKFold

        rows = sorted(self.rows, key=lambda r: r["query_id"])
        y = [r["label"] for r in rows]
        g = [r["group_id"] for r in rows]
        folds = list(
            StratifiedGroupKFold(5, shuffle=True, random_state=42).split(y, y, g)
        )
        where = partition_of(self.manifest)
        for index in folds[3][1]:
            self.assertEqual(where[rows[index]["query_id"]], "validation")
        for index in folds[4][1]:
            self.assertEqual(where[rows[index]["query_id"]], "test")
        for fold in (0, 1, 2):
            for index in folds[fold][1]:
                self.assertEqual(where[rows[index]["query_id"]], "train")
        self.assertEqual(FOLD_PARTITION[3], "validation")

    def test_input_order_does_not_change_manifest(self):
        shuffled = copy.deepcopy(self.rows)
        random.Random(1).shuffle(shuffled)
        self.assertEqual(make_split(shuffled, DIGEST), self.manifest)

    def test_non_accepted_rows_are_left_out(self):
        extra = copy.deepcopy(self.rows[0])
        extra.update(query_id="zzz-excluded", status="excluded", label=None)
        manifest = make_split(self.rows + [extra], DIGEST)
        self.assertNotIn("zzz-excluded", partition_of(manifest))

    def test_refuses_needs_review(self):
        rows = fixture_rows()
        rows[3]["status"] = "needs_review"
        with self.assertRaisesRegex(ValueError, "needs_review rows: "):
            make_split(rows, DIGEST)

    def test_refuses_class_with_too_few_groups(self):
        rows = [r for r in self.rows if r["group_id"] != "cal-g5"]
        self.assertEqual(
            len({r["group_id"] for r in rows if r["label"] == "calculation"}), 5
        )
        make_split(rows, DIGEST)  # exactly five groups is allowed
        rows = [r for r in rows if r["group_id"] != "cal-g4"]
        with self.assertRaisesRegex(
            ValueError, "class calculation has 4 groups; need at least 5 for 5 folds"
        ):
            make_split(rows, DIGEST)


class CheckSplitTest(unittest.TestCase):
    def setUp(self):
        self.rows = fixture_rows()
        self.manifest = make_split(self.rows, DIGEST)

    def check(self, manifest, rows=None, digest=DIGEST):
        return check_split(manifest, rows or self.rows, digest)

    def test_rejects_stale_hash(self):
        self.assertEqual(
            self.check(self.manifest, digest="b" * 64),
            ["stale dataset hash: manifest does not match the dataset file"],
        )

    def test_rejects_duplicate_membership(self):
        m = copy.deepcopy(self.manifest)
        moved = m["partitions"]["train"][0]
        m["partitions"]["test"].append(moved)
        errors = self.check(m)
        self.assertIn(f"{moved}: appears 2 times across partitions", errors)

    def test_rejects_missing_id(self):
        m = copy.deepcopy(self.manifest)
        dropped = m["partitions"]["train"].pop()
        self.assertIn(f"{dropped}: accepted row missing from partitions", self.check(m))

    def test_rejects_extra_id(self):
        m = copy.deepcopy(self.manifest)
        m["partitions"]["train"].append("ghost")
        self.assertIn("ghost: partition member is not an accepted row", self.check(m))

    def test_rejects_group_overlap(self):
        m = copy.deepcopy(self.manifest)
        row = self.rows[0]
        home = partition_of(m)[row["query_id"]]
        other = "test" if home != "test" else "train"
        m["partitions"][home].remove(row["query_id"])
        m["partitions"][other].append(row["query_id"])
        errors = self.check(m)
        self.assertIn(
            f"group {row['group_id']} spans {home}, {other}"
            if home < other
            else f"group {row['group_id']} spans {other}, {home}",
            errors,
        )

    def test_rejects_malformed_manifest(self):
        m = copy.deepcopy(self.manifest)
        del m["groups"]
        self.assertEqual(self.check(m), ["manifest missing fields: groups"])
        m = copy.deepcopy(self.manifest)
        m["manifest_version"] = 2
        self.assertEqual(self.check(m), ["unsupported manifest_version 2"])
        self.assertEqual(self.check([]), ["manifest is not a JSON object"])

    def test_rejects_missing_class_in_partition(self):
        m = copy.deepcopy(self.manifest)
        keep = [
            q
            for q in m["partitions"]["validation"]
            if next(r for r in self.rows if r["query_id"] == q)["label"]
            != "calculation"
        ]
        removed = set(m["partitions"]["validation"]) - set(keep)
        m["partitions"]["validation"] = keep
        errors = self.check(m)
        self.assertIn("partition validation has no rows for class calculation", errors)
        self.assertEqual(
            len([e for e in errors if "missing from partitions" in e]), len(removed)
        )

    def test_rejects_needs_review_row(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["status"] = "needs_review"
        errors = self.check(self.manifest, rows)
        self.assertIn(f"{rows[0]['query_id']}: needs_review row in dataset", errors)

    def test_rejects_group_mapping_disagreement(self):
        m = copy.deepcopy(self.manifest)
        m["groups"][self.rows[0]["query_id"]] = "other"
        self.assertEqual(
            self.check(m),
            [f"{self.rows[0]['query_id']}: manifest group disagrees with dataset"],
        )


class SplitCliTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.rows = fixture_rows()
        (self.root / "data.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in self.rows), encoding="utf-8"
        )
        (self.root / "sources.json").write_text(json.dumps(SOURCES), encoding="utf-8")
        self.config = self.root / "config.json"
        self.write_config()

    def write_config(self, **changes):
        config = {
            "dataset": str(self.root / "data.jsonl"),
            "sources": str(self.root / "sources.json"),
            "seed": 42,
            "split_manifest": str(self.root / "splits" / "split.json"),
            "train": str(self.root / "out" / "train.jsonl"),
            "validation": str(self.root / "out" / "validation.jsonl"),
            "sealed_test": str(self.root / "sealed" / "test.jsonl"),
            **changes,
        }
        self.config.write_text(json.dumps(config), encoding="utf-8")

    def run_split(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main(["split", "--config", str(self.config)])
        return code, output.getvalue()

    def ids(self, name):
        path = self.root / name
        return [json.loads(line)["query_id"] for line in path.read_text().splitlines()]

    def test_split_writes_manifest_and_three_files(self):
        code, output = self.run_split()
        self.assertEqual(code, 0)
        manifest = json.loads((self.root / "splits" / "split.json").read_text())
        self.assertEqual(self.ids("out/train.jsonl"), manifest["partitions"]["train"])
        self.assertEqual(
            self.ids("out/validation.jsonl"), manifest["partitions"]["validation"]
        )
        self.assertEqual(self.ids("sealed/test.jsonl"), manifest["partitions"]["test"])
        self.assertIn('"proportions"', output)
        self.assertNotIn("artificial fixture text", output)
        self.assertTrue(
            output.endswith(
                "PASS: split written to "
                + str(self.root / "splits" / "split.json")
                + "\n"
            )
        )

    def test_rerun_is_idempotent_but_changed_manifest_is_refused(self):
        self.assertEqual(self.run_split()[0], 0)
        self.assertEqual(self.run_split()[0], 0)
        self.write_config(seed=7)
        code, output = self.run_split()
        self.assertEqual(code, 1)
        self.assertIn("exists and differs; manifests are immutable", output)

    def test_refuses_needs_review_dataset(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["status"] = "needs_review"
        (self.root / "data.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8"
        )
        code, output = self.run_split()
        self.assertEqual(code, 1)
        self.assertIn("ERROR: unresolved needs_review rows: ", output)
        self.assertFalse((self.root / "splits").exists())

    def test_refuses_structurally_invalid_dataset(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["text"] = ""
        (self.root / "data.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8"
        )
        code, output = self.run_split()
        self.assertEqual(code, 1)
        self.assertIn("is not structurally valid", output)


if __name__ == "__main__":
    unittest.main()
