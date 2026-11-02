import random
import unittest

from orchestra.collection import interleave, seeded_order


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


if __name__ == "__main__":
    unittest.main()
