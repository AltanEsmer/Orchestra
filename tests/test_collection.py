import contextlib
import hashlib
import io
import json
import random
import tempfile
import unittest
from pathlib import Path

from orchestra.__main__ import main
from orchestra.collection import (
    cap_hold,
    check_release,
    import_row,
    interleave,
    passage_attachment,
    seeded_order,
    split_passage,
    table_attachment,
)
from orchestra.data import FIELDS, LABELS


class SeededOrderTest(unittest.TestCase):
    def test_saved_sample_comes_first_then_seeded_shuffle_of_the_rest(self):
        keys = [5, 1, 4, 2, 3, 6]
        order = seeded_order(keys, seed=42, first=[4, 2])
        rest = [1, 3, 5, 6]
        random.Random(42).shuffle(rest)
        self.assertEqual(order, [4, 2] + rest)

    def test_input_order_does_not_change_the_order(self):
        self.assertEqual(seeded_order([3, 1, 2]), seeded_order([2, 3, 1]))

    def test_sample_key_outside_the_pool_is_refused(self):
        with self.assertRaises(ValueError):
            seeded_order([1, 2], first=[9])

    def test_duplicate_keys_are_refused(self):
        with self.assertRaises(ValueError):
            seeded_order([1, 1, 2])


class InterleaveTest(unittest.TestCase):
    def test_weights_set_the_long_run_ratio(self):
        drawn = list(
            interleave({"a": iter(range(30)), "b": iter(range(10))}, {"a": 3, "b": 1})
        )
        self.assertEqual([name for name, _ in drawn[:8]], list("aaba" * 2))
        self.assertEqual(sum(name == "a" for name, _ in drawn), 30)

    def test_each_stream_keeps_its_own_order(self):
        drawn = list(interleave({"a": iter("xyz"), "b": iter("pq")}, {"a": 1, "b": 1}))
        self.assertEqual([v for n, v in drawn if n == "a"], list("xyz"))
        self.assertEqual([v for n, v in drawn if n == "b"], list("pq"))

    def test_exhausted_stream_lets_the_others_continue(self):
        drawn = list(
            interleave({"a": iter([1]), "b": iter([1, 2, 3])}, {"a": 5, "b": 1})
        )
        self.assertEqual([n for n, _ in drawn], ["a", "b", "b", "b"])

    def test_weights_must_be_positive_and_match_the_streams(self):
        with self.assertRaises(ValueError):
            list(interleave({"a": iter([1])}, {"a": 0}))
        with self.assertRaises(ValueError):
            list(interleave({"a": iter([1])}, {"b": 1}))


class ImportAdapterTest(unittest.TestCase):
    def test_row_has_the_nine_fields_and_guide_v3(self):
        row = import_row(
            "q0500", "g0500", "  Keep  me.", "calculation", "gsm8k", "Because.", False
        )
        self.assertEqual(set(row), set(FIELDS))
        self.assertEqual(row["text"], "  Keep  me.")
        self.assertEqual(row["status"], "accepted")
        self.assertEqual(row["annotation_version"], "guide-v3")
        self.assertEqual(row["annotator_ids"], ["ai-screen"])

    def test_adjudicated_row_names_altan_as_annotator(self):
        row = import_row("q1", "g1", "t", "calculation", "gsm8k", "r", True)
        self.assertEqual(row["annotator_ids"], ["ai-screen", "A1"])

    def test_unknown_label_is_refused(self):
        with self.assertRaises(ValueError):
            import_row("q1", "g1", "t", "lookup", "gsm8k", "r", False)

    def test_passage_split_keeps_both_parts_exactly(self):
        prompt = "Summarize this text:\n\nThe  river rose.\n"
        query, passage = split_passage(prompt, "Summarize this text:")
        self.assertEqual(query, "Summarize this text:")
        self.assertEqual(passage, "\n\nThe  river rose.\n")

    def test_passage_split_refuses_missing_repeated_or_empty_parts(self):
        for prompt, instruction in [
            ("Read the poem.", "Summarize"),
            ("Again. Again.", "Again."),
            ("Only an instruction.", "Only an instruction."),
            ("text", "  "),
        ]:
            with self.subTest(instruction=instruction), self.assertRaises(ValueError):
                split_passage(prompt, instruction)

    def test_passage_attachment_checks_the_recorded_hash(self):
        digest = hashlib.sha256(b"Body.").hexdigest()
        record = passage_attachment("q1", "Body.", expected_sha256=digest)
        self.assertEqual(record["sha256"], digest)
        with self.assertRaises(ValueError):
            passage_attachment("q1", "Changed.", expected_sha256=digest)

    def test_table_attachment_is_a_pinned_reference_not_a_copy(self):
        record = table_attachment(
            "q1", "data/001_Forbes/all.parquet", "e75d53a", "b" * 64
        )
        self.assertEqual(record["kind"], "table")
        self.assertNotIn("text", record)
        with self.assertRaises(ValueError):
            table_attachment("q1", "data/x/all.parquet", "e75d53a", "not-a-hash")


def release_rows():
    """2 parent and 6 new rows per class, over two sources and four types."""
    rows, types = [], {}
    for c, label in enumerate(LABELS):
        for i in range(2):
            qid = f"p{c}{i}"
            rows.append(
                _row(qid, f"pg{c}{i}", f"parent {label} words {qid}", label, "s1")
            )
            types[qid] = "t0"
        for i in range(6):
            qid = f"n{c}{i}"
            source = "s1" if i % 2 else "s2"
            text = f"{label} distinct item {i} " + " ".join(
                f"w{c}{i}{k}" for k in range(6)
            )
            rows.append(_row(qid, f"ng{c}{i}", text, label, source))
            types[qid] = f"t{i % 3 + 1}"
    return rows, types


def _row(qid, group, text, label, source):
    return {
        "query_id": qid,
        "group_id": group,
        "text": text,
        "label": label,
        "source_id": source,
    }


PARENT = {f"p{c}{i}" for c in range(4) for i in range(2)}


class ReleaseCheckTest(unittest.TestCase):
    def errors(self, rows, types, pairs=()):
        return check_release(rows, PARENT, types, pairs)["errors"]

    def test_balanced_release_passes_and_reports_counts(self):
        rows, types = release_rows()
        report = check_release(rows, PARENT, types, ())
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["by_class"]["calculation"]["rows"], 8)
        self.assertEqual(report["by_class"]["calculation"]["new_groups"], 6)

    def test_exact_duplicate_after_normalizing_fails(self):
        rows, types = release_rows()
        rows[3]["text"] = "  " + rows[2]["text"].upper()
        self.assertTrue(any("same text" in e for e in self.errors(rows, types)))

    def test_fifth_row_in_a_group_fails(self):
        rows, types = release_rows()
        for row in rows[2:7]:
            row["group_id"] = "ng00"
        self.assertTrue(any("5 rows" in e for e in self.errors(rows, types)))

    def test_source_above_75_percent_of_a_class_fails(self):
        rows, types = release_rows()
        for row in rows[:8]:
            row["source_id"] = "s1"
        self.assertTrue(any("source s1" in e for e in self.errors(rows, types)))

    def test_one_source_class_fails(self):
        rows, types = release_rows()
        for row in rows:
            row["source_id"] = "s1"
        self.assertTrue(any("2 sources" in e for e in self.errors(rows, types)))

    def test_type_above_40_percent_of_a_class_fails(self):
        rows, types = release_rows()
        for qid in ("n01", "n02"):
            types[qid] = "t1"
        self.assertTrue(any("type t1" in e for e in self.errors(rows, types)))

    def test_missing_type_fails(self):
        rows, types = release_rows()
        del types["n00"]
        self.assertTrue(any("no request type" in e for e in self.errors(rows, types)))

    def test_fewer_than_five_new_groups_fails(self):
        rows, types = release_rows()
        for row in rows[2:6]:
            row["group_id"] = "ng-shared"
        self.assertTrue(any("new groups" in e for e in self.errors(rows, types)))

    def test_new_row_in_a_parent_group_fails(self):
        rows, types = release_rows()
        rows[2]["group_id"] = "pg00"
        self.assertTrue(any("parent group" in e for e in self.errors(rows, types)))

    def test_new_row_overlapping_a_parent_row_fails_without_printing_it(self):
        rows, types = release_rows()
        rows[2]["text"] = rows[0]["text"] + " extra"
        errors = self.errors(rows, types)
        self.assertTrue(any("p00" in e for e in errors))
        self.assertFalse(any(rows[0]["text"] in e for e in errors))

    def test_close_pair_needs_a_recorded_hand_check(self):
        rows, types = release_rows()
        rows[3]["text"] = rows[2]["text"] + " more"
        self.assertTrue(any("hand check" in e for e in self.errors(rows, types)))
        decided = [{"pair": ["n00", "n01"], "same_group": False, "reason": "frame"}]
        self.assertEqual(self.errors(rows, types, decided), [])
        joined = [{"pair": ["n00", "n01"], "same_group": True, "reason": "swap"}]
        self.assertTrue(
            any("share a group" in e for e in self.errors(rows, types, joined))
        )


class CapHoldTest(unittest.TestCase):
    def test_candidate_over_a_source_or_type_cap_is_held(self):
        rows = [_row(f"q{i}", f"g{i}", "t", "calculation", "big") for i in range(3)]
        rows.append(_row("q3", "g3", "t", "calculation", "small"))
        types = {"q0": "a", "q1": "a", "q2": "b", "q3": "b"}
        new = _row("q4", "g4", "t", "calculation", "big")
        self.assertIn("source big", cap_hold(rows, types, new, "c"))
        other = _row("q5", "g5", "t", "calculation", "small")
        self.assertIsNone(cap_hold(rows, types, other, "c"))
        self.assertIn("type b", cap_hold(rows, types, other, "b"))

    def test_other_classes_do_not_count(self):
        rows = [_row(f"d{i}", f"h{i}", "t", "direct_answer", "big") for i in range(6)]
        rows += [_row("c0", "g0", "t", "calculation", "small")]
        rows += [_row("c1", "g1", "t", "calculation", "mid")]
        types = {r["query_id"]: "a" for r in rows} | {"c1": "b"}
        new = _row("q1", "g2", "t", "calculation", "big")
        self.assertIsNone(cap_hold(rows, types, new, "c"))


class CheckCollectionCommandTest(unittest.TestCase):
    def run_command(self, rows, types, pairs):
        rows = [r | {"status": "accepted"} for r in rows]
        parent_rows = [r for r in rows if r["query_id"] in PARENT]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            files = {
                "dataset": (tmp / "d.jsonl", rows),
                "parent": (tmp / "p.jsonl", parent_rows),
            }
            for path, data in files.values():
                path.write_text("".join(json.dumps(r) + "\n" for r in data))
            (tmp / "t.json").write_text(json.dumps(types))
            (tmp / "pairs.json").write_text(json.dumps(pairs))
            argv = ["check-collection", "--dataset", str(tmp / "d.jsonl")]
            argv += ["--parent", str(tmp / "p.jsonl"), "--types", str(tmp / "t.json")]
            argv += ["--pairs", str(tmp / "pairs.json"), "--out", str(tmp / "r.json")]
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = main(argv)
            report = json.loads((tmp / "r.json").read_text())
        return code, output.getvalue(), report

    def test_passing_release_exits_zero_and_saves_the_report(self):
        rows, types = release_rows()
        code, output, report = self.run_command(rows, types, [])
        self.assertEqual(code, 0)
        self.assertIn("PASS", output)
        self.assertEqual(report["errors"], [])

    def test_failing_release_exits_one_without_printing_text(self):
        rows, types = release_rows()
        rows[2]["text"] = rows[0]["text"] + " extra"
        code, output, report = self.run_command(rows, types, [])
        self.assertEqual(code, 1)
        self.assertIn("overlaps parent row p00", output)
        self.assertNotIn(rows[0]["text"], output)
        self.assertTrue(report["errors"])


if __name__ == "__main__":
    unittest.main()
