import unittest

from slangchat.data.loader import load_entries
from slangchat.detection import DictionarySlangDetector, MatchType
from slangchat.detection.normalizer import normalize_text


class DictionaryDetectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.detector = DictionarySlangDetector(load_entries("data/slang.json"))

    def test_normalizes_unicode_and_whitespace(self) -> None:
        self.assertEqual(normalize_text("  no\t\ncap  "), "no cap")

    def test_detects_korean_variant_with_attached_prefix(self) -> None:
        results = self.detector.detect("이거 개킹받네")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].surface, "개킹받네")
        self.assertEqual(results[0].matched_surface, "킹받네")
        self.assertEqual(results[0].term, "킹받다")
        self.assertEqual(results[0].prefix, "개")
        self.assertEqual(results[0].match_type, MatchType.DICTIONARY_VARIANT)
        self.assertEqual(results[0].confidence, 0.96)

    def test_detects_spaced_prefix(self) -> None:
        results = self.detector.detect("완전 갓생 산다")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].prefix, "완전")
        self.assertEqual(results[0].term, "갓생")
        self.assertEqual(results[0].matched_surface, "갓생 산다")

    def test_detects_english_case_insensitively(self) -> None:
        results = self.detector.detect("That explanation is SUS!")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].term, "sus")
        self.assertEqual(results[0].match_type, MatchType.DICTIONARY_EXACT)

    def test_prefers_longest_phrase_and_avoids_overlap(self) -> None:
        results = self.detector.detect("No cap, that presentation slayed.")

        self.assertEqual([result.term for result in results], ["no cap", "slay"])

    def test_does_not_split_prefix_without_dictionary_match(self) -> None:
        self.assertEqual(self.detector.detect("개인 일정이 완전히 바뀌었다"), [])

    def test_does_not_treat_unproductive_syllables_as_prefixes(self) -> None:
        self.assertEqual(self.detector.detect("존킹받네"), [])
        self.assertEqual(self.detector.detect("씨킹받네"), [])


if __name__ == "__main__":
    unittest.main()
