import hashlib
import random
import unittest

from orchestra.collection import (
    import_row,
    interleave,
    passage_attachment,
    seeded_order,
    split_passage,
    table_attachment,
)
from orchestra.data import FIELDS


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


if __name__ == "__main__":
    unittest.main()
