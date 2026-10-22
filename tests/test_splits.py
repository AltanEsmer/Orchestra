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
from orchestra.data import LABELS, file_sha256
from orchestra.splits import (
    check_extension,
    check_split,
    extend_split,
    make_split,
    row_hash,
)

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

    def test_literal_validation_and_test_membership(self):
        partitions = self.manifest["partitions"]
        self.assertEqual(
            partitions["validation"],
            ["cal-g5-0", "cal-g5-1", "dir-g5-0", "dir-g5-1", "doc-g0-0",
             "doc-g0-1", "doc-g2-0", "doc-g2-1", "kno-g4-0", "kno-g4-1"],
        )  # fmt: skip
        self.assertEqual(
            partitions["test"],
            ["cal-g2-0", "cal-g2-1", "dir-g3-0", "dir-g3-1", "doc-g5-0",
             "doc-g5-1", "kno-g1-0", "kno-g1-1"],
        )  # fmt: skip
        self.assertEqual(len(partitions["train"]), 30)

    def test_row_hashes_are_canonical_content_hashes(self):
        row = {"text": "é?", "label": "calculation", "group_id": "g", "x": 1}
        self.assertEqual(
            row_hash(row),
            "3bf3b31dd4d350afdc5740ae692ceee2ddc7b043329b0f70f7fa200566284a9e",
        )
        self.assertEqual(row_hash(dict(row, x=2)), row_hash(row))
        self.assertNotEqual(row_hash(dict(row, text="e?")), row_hash(row))
        m = self.manifest
        self.assertEqual(m["row_sha256"]["doc-g0-0"], row_hash(self.rows[0]))
        self.assertEqual(len(m["row_sha256"]), 48)

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

    def test_refuses_partition_missing_a_class(self):
        # Mixed-label groups 2-0 and 2-3 leave validation without calculation.
        spec = [
            ("0-2-2", "document_retrieval"),
            ("0-3-2", "document_retrieval"),
            ("1-0-2", "knowledge_lookup"),
            ("1-3-2", "knowledge_lookup"),
            ("1-4-1", "knowledge_lookup"),
            ("1-5-1", "knowledge_lookup"),
            ("2-0-0", "calculation"),
            ("2-0-1", "document_retrieval"),
            ("2-0-2", "direct_answer"),
            ("2-1-0", "calculation"),
            ("2-2-3", "calculation"),
            ("2-3-0", "document_retrieval"),
            ("2-3-1", "knowledge_lookup"),
            ("2-3-2", "calculation"),
            ("2-4-0", "calculation"),
            ("3-0-0", "document_retrieval"),
            ("3-1-0", "direct_answer"),
            ("3-2-1", "direct_answer"),
            ("3-3-0", "direct_answer"),
            ("3-4-1", "direct_answer"),
        ]
        rows = [
            {"query_id": q, "group_id": q[:3], "label": label, "status": "accepted"}
            for q, label in spec
        ]
        with self.assertRaisesRegex(
            ValueError,
            "partition validation has no rows for class calculation; "
            "collect more groups instead of searching seeds",
        ):
            make_split(rows, DIGEST)


class CheckSplitTest(unittest.TestCase):
    def setUp(self):
        self.rows = fixture_rows()
        self.manifest = make_split(self.rows, DIGEST)

    def check(self, manifest, rows=None, digest=DIGEST):
        return check_split(manifest, rows if rows is not None else self.rows, digest)

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

    def test_rejects_non_string_ids_without_crashing(self):
        malformed = "manifest partitions or groups are malformed"
        for bad in (["x"], {"x": 1}, 7):
            m = copy.deepcopy(self.manifest)
            m["partitions"]["train"].append(bad)
            self.assertEqual(self.check(m), [malformed])
        m = copy.deepcopy(self.manifest)
        m["groups"]["x"] = 5
        self.assertEqual(self.check(m), [malformed])

    def test_rejects_wrong_counts_and_constants(self):
        m = copy.deepcopy(self.manifest)
        m["counts"]["train"]["calculation"] += 1
        self.assertEqual(
            self.check(m), ["manifest counts differ from the counts of its partitions"]
        )
        m = copy.deepcopy(self.manifest)
        m["n_splits"] = 3
        self.assertEqual(self.check(m), ["manifest n_splits is 3, expected 5"])
        m = copy.deepcopy(self.manifest)
        m["fold_partition"]["3"] = "test"
        self.assertEqual(len(self.check(m)), 1)

    def test_rejects_extra_groups_key(self):
        m = copy.deepcopy(self.manifest)
        m["groups"]["ghost"] = "gx"
        self.assertEqual(
            self.check(m), ["ghost: manifest group for a row that is not accepted"]
        )

    def test_rejects_changed_row_content_hash(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["text"] = "edited"
        self.assertEqual(
            self.check(self.manifest, rows),
            [f"{rows[0]['query_id']}: row content hash disagrees with dataset"],
        )
        m = copy.deepcopy(self.manifest)
        m["row_sha256"]["ghost"] = "0" * 64
        self.assertEqual(
            self.check(m), ["ghost: row hash for a row that is not accepted"]
        )
        del m["row_sha256"]
        self.assertEqual(self.check(m), ["manifest missing fields: row_sha256"])

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

    def test_refuses_output_aliasing_input_before_any_write(self):
        path = self.root / "raw/data.jsonl"
        path.parent.mkdir()
        path.write_bytes((self.root / "data.jsonl").read_bytes())
        before = path.read_bytes()
        self.write_config(dataset=str(path), train=str(path))
        code, output = self.run_split()
        self.assertEqual(code, 1, output)
        self.assertEqual(path.read_bytes(), before)
        self.assertFalse((self.root / "splits").exists())

    def test_refuses_changed_materialized_file_without_rewriting_others(self):
        self.assertEqual(self.run_split()[0], 0)
        path = self.root / "sealed/test.jsonl"
        path.write_text("changed\n")
        code, output = self.run_split()
        self.assertEqual(code, 1, output)
        self.assertEqual(path.read_text(), "changed\n")

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

    def test_refuses_sealed_test_sharing_a_path_or_directory(self):
        for changes in (
            {"sealed_test": str(self.root / "out" / "train.jsonl")},
            {"sealed_test": str(self.root / "out" / "test.jsonl")},
        ):
            self.write_config(**changes)
            code, output = self.run_split()
            self.assertEqual(code, 1)
            self.assertIn("must be distinct files", output)
            self.assertFalse((self.root / "splits").exists())

    def test_reports_bad_config_without_traceback(self):
        config = json.loads(self.config.read_text())
        del config["seed"]
        self.config.write_text(json.dumps(config))
        self.assertEqual(self.run_split(), (1, "ERROR: config is missing 'seed'\n"))
        missing = self.root / "nope.jsonl"
        self.write_config(dataset=str(missing))
        self.assertEqual(
            self.run_split(),
            (1, f"ERROR: cannot read {missing}: No such file or directory\n"),
        )

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


def new_rows():
    """Artificial extension: 4 classes x 6 new independent groups x 2 rows."""
    rows = fixture_rows()
    for row in rows:
        row["query_id"] = "new-" + row["query_id"]
        row["group_id"] = "new-" + row["group_id"]
        row["text"] = row["text"].replace("fixture text", "fixture extension text")
    return rows


PARENT_DIGEST = "c" * 64
CHILD_DIGEST = "d" * 64


class ExtendSplitTest(unittest.TestCase):
    def setUp(self):
        self.parent_rows = fixture_rows()
        self.parent = make_split(self.parent_rows, PARENT_DIGEST)
        self.rows = fixture_rows() + new_rows()
        self.child = self.extend(self.rows)

    def extend(self, rows, parent=None, seed=42):
        return extend_split(
            self.parent if parent is None else parent,
            self.parent_rows,
            rows,
            PARENT_DIGEST,
            "e" * 64,
            CHILD_DIGEST,
            seed,
        )

    def test_parent_literal_memberships_are_frozen(self):
        for name, ids in self.parent["partitions"].items():
            self.assertTrue(set(ids) <= set(self.child["partitions"][name]))
        self.assertEqual(
            [q for q in self.child["partitions"]["validation"] if q[:3] != "new"],
            [
                "cal-g5-0", "cal-g5-1", "dir-g5-0", "dir-g5-1", "doc-g0-0",
                "doc-g0-1", "doc-g2-0", "doc-g2-1", "kno-g4-0", "kno-g4-1",
            ],
        )  # fmt: skip
        # M2 validation can never become M3 test.
        validation = set(self.parent["partitions"]["validation"])
        self.assertFalse(validation & set(self.child["partitions"]["test"]))

    def test_child_records_lineage_and_combined_counts(self):
        c = self.child
        self.assertEqual(c["parent_manifest_sha256"], "e" * 64)
        self.assertEqual(c["parent_dataset_sha256"], PARENT_DIGEST)
        self.assertEqual(c["dataset_sha256"], CHILD_DIGEST)
        self.assertEqual(sum(len(i) for i in c["partitions"].values()), 96)
        self.assertEqual(len(c["row_sha256"]), 96)
        # Mixed-label groups count once under each label they contain.
        self.assertEqual(
            c["new_groups"]["by_class"],
            {
                "document_retrieval": 6,
                "knowledge_lookup": 6,
                "calculation": 6,
                "direct_answer": 8,
            },
        )
        self.assertEqual(sum(c["new_groups"]["by_partition"].values()), 24)
        for name, ids in c["partitions"].items():
            self.assertEqual(c["proportions"][name], round(len(ids) / 96, 4))
        self.assertEqual(
            check_extension(
                c, self.parent, self.parent_rows, self.rows, CHILD_DIGEST, "e" * 64
            ),
            [],
        )
        self.assertEqual(check_split(c, self.rows, CHILD_DIGEST), [])

    def test_new_rows_use_the_p2_allocation(self):
        # New rows alone, split as P2 would, land in the same partitions.
        alone = make_split(new_rows(), CHILD_DIGEST)["partitions"]
        for name, ids in alone.items():
            self.assertTrue(set(ids) <= set(self.child["partitions"][name]))

    def test_new_row_order_does_not_change_child(self):
        shuffled = copy.deepcopy(self.rows)
        random.Random(3).shuffle(shuffled)
        self.assertEqual(self.extend(shuffled), self.child)

    def test_refuses_changed_old_text_label_group_and_missing_row(self):
        for field, value in (("text", "edited"), ("label", LABELS[2])):
            rows = copy.deepcopy(self.rows)
            rows[5][field] = value
            q = rows[5]["query_id"]
            with self.assertRaisesRegex(
                ValueError, f"{q}: text, label or group_id differs.*successor protocol"
            ):
                self.extend(rows)
        rows = copy.deepcopy(self.rows)
        rows[5]["group_id"] = "regrouped"
        with self.assertRaisesRegex(ValueError, "differs from the parent"):
            self.extend(rows)
        rows = [r for r in self.rows if r["query_id"] != "cal-g1-0"]
        with self.assertRaisesRegex(
            ValueError, "cal-g1-0: parent row is missing from the extension"
        ):
            self.extend(rows)

    def test_refuses_new_row_in_an_existing_group(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["group_id"] = "cal-g1"
        with self.assertRaisesRegex(
            ValueError,
            f"{rows[-1]['query_id']}: group cal-g1 already exists.*challenge",
        ):
            self.extend(rows)

    def test_refuses_needs_review_and_too_few_new_groups(self):
        rows = copy.deepcopy(self.rows)
        rows[-1]["status"] = "needs_review"
        with self.assertRaisesRegex(ValueError, "needs_review rows: "):
            self.extend(rows)
        rows = [r for r in self.rows if not r["group_id"].startswith("new-cal-g5")]
        self.extend(rows)  # five new groups per class is enough
        rows = [r for r in rows if not r["group_id"].startswith("new-cal-g4")]
        with self.assertRaisesRegex(
            ValueError, "class calculation has 4 new groups; need at least 5"
        ):
            self.extend(rows)

    def test_refuses_an_invalid_parent_manifest(self):
        parent = copy.deepcopy(self.parent)
        parent["partitions"]["train"].pop()
        with self.assertRaisesRegex(ValueError, "parent manifest is invalid"):
            self.extend(self.rows, parent)


class CheckExtensionTest(unittest.TestCase):
    def setUp(self):
        self.parent_rows = fixture_rows()
        self.parent = make_split(self.parent_rows, PARENT_DIGEST)
        self.rows = fixture_rows() + new_rows()
        self.child = extend_split(
            self.parent,
            self.parent_rows,
            self.rows,
            PARENT_DIGEST,
            "e" * 64,
            CHILD_DIGEST,
            42,
        )

    def check(self, child, rows=None, digest=CHILD_DIGEST, parent=None, pin="e" * 64):
        return check_extension(
            child,
            self.parent if parent is None else parent,
            self.parent_rows,
            rows or self.rows,
            digest,
            pin,
        )

    def move(self, child, query_id, target):
        for ids in child["partitions"].values():
            if query_id in ids:
                ids.remove(query_id)
        child["partitions"][target].append(query_id)

    def move_group(self, child, group, target):
        """Move a whole group and recompute counts, so only extension rules object."""
        rows_by_id = {r["query_id"]: r for r in self.rows}
        for q, g in child["groups"].items():
            if g == group:
                self.move(child, q, target)
        for name, ids in child["partitions"].items():
            ids.sort()
            child["counts"][name] = {
                label: sum(rows_by_id[q]["label"] == label for q in ids)
                for label in LABELS
            }
        self.assertEqual(check_split(child, self.rows, CHILD_DIGEST), [])

    def test_accepts_the_built_child(self):
        self.assertEqual(self.check(self.child), [])

    def test_rejects_moved_original_id(self):
        child = copy.deepcopy(self.child)
        moved = self.parent["partitions"]["validation"][0]
        self.move_group(child, self.parent["groups"][moved], "test")
        errors = self.check(child)
        self.assertIn(f"{moved}: moved from parent validation to test", errors)

    def test_rejects_dropped_original_id(self):
        child = copy.deepcopy(self.child)
        dropped = self.parent["partitions"]["test"][0]
        child["partitions"]["test"].remove(dropped)
        self.assertIn(
            f"{dropped}: accepted row missing from partitions", self.check(child)
        )

    def test_rejects_changed_old_row_content(self):
        rows = copy.deepcopy(self.rows)
        rows[5]["text"] = "edited"
        errors = self.check(self.child, rows)
        self.assertIn(
            f"{rows[5]['query_id']}: row content hash disagrees with dataset", errors
        )

    def test_rejects_stale_hashes(self):
        child = copy.deepcopy(self.child)
        child["parent_dataset_sha256"] = "f" * 64
        self.assertEqual(
            self.check(child),
            ["child differs from the manifest rebuilt from parent and rows"],
        )
        self.assertEqual(
            self.check(self.child, pin="9" * 64),
            ["child differs from the manifest rebuilt from parent and rows"],
        )
        self.assertEqual(
            self.check(self.child, digest="9" * 64),
            ["stale dataset hash: manifest does not match the dataset file"],
        )

    def test_rejects_new_row_joined_to_a_parent_group_in_its_own_partition(self):
        rows = copy.deepcopy(self.rows)
        child = copy.deepcopy(self.child)
        new_id = "new-cal-g0-0"
        row = next(r for r in rows if r["query_id"] == new_id)
        home = next(n for n, ids in child["partitions"].items() if new_id in ids)
        family = next(q for q in self.parent["partitions"][home] if q.startswith("cal"))
        group = self.parent["groups"][family]
        self.move(child, "new-cal-g0-1", home)  # keep the child's own group whole
        row["group_id"] = group
        next(r for r in rows if r["query_id"] == "new-cal-g0-1")["group_id"] = group
        for q in (new_id, "new-cal-g0-1"):
            child["groups"][q] = group
            child["row_sha256"][q] = row_hash(
                next(r for r in rows if r["query_id"] == q)
            )
        errors = self.check(child, rows)
        self.assertTrue(
            any("already exists in the parent" in e for e in errors), errors
        )

    def test_rejects_hand_moved_new_group(self):
        child = copy.deepcopy(self.child)
        new_id = "new-cal-g0-0"
        home = next(n for n, ids in child["partitions"].items() if new_id in ids)
        target = "validation" if home != "validation" else "test"
        self.move_group(child, "new-cal-g0", target)
        self.assertEqual(
            self.check(child),
            ["child differs from the manifest rebuilt from parent and rows"],
        )

    def test_malformed_manifests_return_errors_not_exceptions(self):
        for bad in ([], None, "x"):
            self.assertTrue(self.check(bad))
            if bad is not None:
                self.assertTrue(self.check(self.child, parent=bad))
        child = copy.deepcopy(self.child)
        child["partitions"] = []
        self.assertEqual(
            self.check(child), ["manifest partitions or groups are malformed"]
        )
        child = copy.deepcopy(self.child)
        del child["row_sha256"]
        self.assertEqual(self.check(child), ["manifest missing fields: row_sha256"])
        parent = copy.deepcopy(self.parent)
        del parent["row_sha256"]
        self.assertEqual(
            self.check(self.child, parent=parent),
            ["parent: manifest missing fields: row_sha256"],
        )


class ExtendCliTest(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.parent_rows = fixture_rows()
        self.rows = self.parent_rows + new_rows()
        self.write("parent.jsonl", self.parent_rows)
        self.write("child.jsonl", self.rows)
        (self.root / "sources.json").write_text(json.dumps(SOURCES), encoding="utf-8")
        self.split_config = self.root / "split.json"
        self.split_config.write_text(
            json.dumps(
                {
                    "dataset": str(self.root / "parent.jsonl"),
                    "sources": str(self.root / "sources.json"),
                    "seed": 42,
                    "split_manifest": str(self.root / "splits" / "m2.json"),
                    "train": str(self.root / "m2" / "train.jsonl"),
                    "validation": str(self.root / "m2" / "validation.jsonl"),
                    "sealed_test": str(self.root / "sealed" / "m2-test.jsonl"),
                }
            ),
            encoding="utf-8",
        )
        self.config = self.root / "extend.json"
        self.assertEqual(self.cli("split", self.split_config)[0], 0)
        self.write_config()

    def write(self, name, rows):
        (self.root / name).write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8"
        )

    def write_config(self, **changes):
        config = {
            "parent_dataset": str(self.root / "parent.jsonl"),
            "parent_manifest": str(self.root / "splits" / "m2.json"),
            "parent_manifest_sha256": file_sha256(self.root / "splits" / "m2.json"),
            "dataset": str(self.root / "child.jsonl"),
            "sources": str(self.root / "sources.json"),
            "seed": 42,
            "split_manifest": str(self.root / "splits" / "m3.json"),
            "train": str(self.root / "m3" / "train.jsonl"),
            "validation": str(self.root / "m3" / "validation.jsonl"),
            "sealed_test": str(self.root / "sealed" / "m3-test.jsonl"),
            "results_dir": str(self.root / "results"),
            "configurations": [{"family": "B0"}, {"family": "L2", "C": 1}],
            **changes,
        }
        self.config.write_text(json.dumps(config), encoding="utf-8")

    def cli(self, command, config, *extra):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = main([command, "--config", str(config), *extra])
        return code, output.getvalue()

    def ids(self, name):
        lines = (self.root / name).read_text().splitlines()
        return [json.loads(line)["query_id"] for line in lines]

    def test_extend_end_to_end_then_run(self):
        code, output = self.cli("extend", self.config)
        self.assertEqual(code, 0, output)
        parent = json.loads((self.root / "splits" / "m2.json").read_text())
        child = json.loads((self.root / "splits" / "m3.json").read_text())
        for name, files in (
            ("train", "m3/train.jsonl"),
            ("validation", "m3/validation.jsonl"),
            ("test", "sealed/m3-test.jsonl"),
        ):
            self.assertEqual(self.ids(files), child["partitions"][name])
            self.assertTrue(set(parent["partitions"][name]) <= set(self.ids(files)))
        self.assertEqual(child["new_groups"]["by_class"]["calculation"], 6)
        self.assertEqual(
            child["parent_manifest_sha256"],
            file_sha256(self.root / "splits" / "m2.json"),
        )
        self.assertIn('"new_groups"', output)
        self.assertNotIn("artificial fixture", output)
        self.assertTrue(
            output.endswith(f"PASS: extension written to {self.root}/splits/m3.json\n")
        )
        self.assertEqual(self.cli("extend", self.config)[0], 0)  # idempotent
        code, output = self.cli("run", self.config, "--run-id", "m3-test")
        self.assertEqual(code, 0, output)
        self.assertIn("B0: ok", output)

    def test_refuses_stale_parent_dataset(self):
        edited = copy.deepcopy(self.parent_rows)
        edited[0]["text"] = "edited after the split"
        self.write("parent.jsonl", edited)
        code, output = self.cli("extend", self.config)
        self.assertEqual(
            (code, output),
            (1, "ERROR: parent dataset file does not match the parent manifest hash\n"),
        )
        self.assertFalse((self.root / "splits" / "m3.json").exists())

    def test_refuses_changed_old_row_in_new_dataset(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["text"] = "silently corrected"
        self.write("child.jsonl", rows)
        code, output = self.cli("extend", self.config)
        self.assertEqual(code, 1)
        self.assertIn("record the correction and build a named successor", output)
        self.assertFalse((self.root / "splits" / "m3.json").exists())
        self.assertFalse((self.root / "sealed" / "m3-test.jsonl").exists())

    def test_refuses_unpinned_or_stale_parent_manifest_hash(self):
        message = (
            "ERROR: parent_manifest_sha256 in the config is missing or does not "
            "match the parent manifest file\n"
        )
        for pin in (None, "0" * 64):
            self.write_config(parent_manifest_sha256=pin)
            self.assertEqual(self.cli("extend", self.config), (1, message))
        self.assertFalse((self.root / "splits" / "m3.json").exists())

    def test_refuses_shared_output_paths(self):
        self.write_config(sealed_test=str(self.root / "m3" / "test.jsonl"))
        code, output = self.cli("extend", self.config)
        self.assertEqual(code, 1)
        self.assertIn("must be distinct files", output)

    def test_reports_missing_config_key(self):
        config = json.loads(self.config.read_text())
        del config["parent_manifest"]
        self.config.write_text(json.dumps(config))
        self.assertEqual(
            self.cli("extend", self.config),
            (1, "ERROR: config is missing 'parent_manifest'\n"),
        )


if __name__ == "__main__":
    unittest.main()
