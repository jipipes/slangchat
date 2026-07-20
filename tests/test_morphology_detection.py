import unittest

from slangchat.data.loader import load_entries
from slangchat.detection import HybridSlangDetector, KiwiSlangDetector, MatchType


class MorphologyDetectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        entries = load_entries("data/slang.json")
        cls.morphology = KiwiSlangDetector(entries)
        cls.hybrid = HybridSlangDetector(entries)

    def test_detects_unregistered_present_inflection(self) -> None:
        results = self.morphology.detect("그 상황은 진짜 킹받는다")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].surface, "킹받는다")
        self.assertEqual(results[0].term, "킹받다")
        self.assertEqual(results[0].match_type, MatchType.MORPHOLOGY_LEMMA)
        self.assertEqual(results[0].confidence, 0.92)

    def test_detects_past_inflection_with_prefix(self) -> None:
        results = self.morphology.detect("나 그거 개킹받았어")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].surface, "개킹받았어")
        self.assertEqual(results[0].prefix, "개")
        self.assertEqual(results[0].term, "킹받다")

    def test_hybrid_prefers_registered_dictionary_variant(self) -> None:
        results = self.hybrid.detect("이거 개킹받네")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].match_type, MatchType.DICTIONARY_VARIANT)
        self.assertEqual(results[0].matched_surface, "킹받네")

    def test_does_not_apply_korean_morphology_to_nouns(self) -> None:
        self.assertEqual(self.morphology.detect("이번 달부터 갓생 산다"), [])


if __name__ == "__main__":
    unittest.main()

