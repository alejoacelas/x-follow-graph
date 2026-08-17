import importlib.util
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("analyze", Path(__file__).parents[1] / "scripts" / "analyze.py")
analyze = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyze)


class AnalyzeTests(unittest.TestCase):
    def test_tokens_normalize_and_remove_stopwords(self):
        self.assertEqual(analyze.tokens("AI safety and alignment research"), ["ai-safety", "ai-safety"])

    def test_cosine(self):
        self.assertAlmostEqual(analyze.cosine({"a": 1}, {"a": 0.5, "b": 0.5}), 0.5)

    def test_mutual_count_english_or_spanish(self):
        self.assertEqual(analyze.parse_mutual_count("A, B and 74 others you follow"), 76)
        self.assertEqual(analyze.parse_mutual_count("A, B y 6 más de las cuentas que sigues"), 8)

    def test_kmeans_is_deterministic(self):
        vectors = {"a": {"x": 1}, "b": {"x": .9, "y": .1}, "c": {"z": 1}, "d": {"z": .9, "y": .1}}
        self.assertEqual(analyze.kmeans(vectors, 2), analyze.kmeans(vectors, 2))


if __name__ == "__main__":
    unittest.main()
