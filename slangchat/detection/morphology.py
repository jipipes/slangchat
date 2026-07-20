from __future__ import annotations

from collections.abc import Iterable

from kiwipiepy import Kiwi, Token

from slangchat.data.schema import Language, SlangEntry
from slangchat.detection.dictionary import KOREAN_EMPHASIS_PREFIXES
from slangchat.detection.models import DetectionResult, MatchType
from slangchat.detection.normalizer import normalize_text


ENDING_TAGS = ("EP", "EF", "EC", "ETM", "ETN")


class KiwiSlangDetector:
    """Detect inflected Korean slang predicates using curated dictionary lemmas."""

    def __init__(self, entries: Iterable[SlangEntry]) -> None:
        self._kiwi = Kiwi()
        self._stems: dict[str, SlangEntry] = {}

        for entry in entries:
            if entry.language != Language.KO or not entry.term.endswith("다"):
                continue
            stem = entry.term[:-1]
            if not stem:
                continue
            self._stems[stem] = entry
            self._kiwi.add_user_word(stem, "VV")

    def detect(self, text: str) -> list[DetectionResult]:
        normalized = normalize_text(text)
        tokens = self._kiwi.tokenize(normalized)
        results: list[DetectionResult] = []

        for index, token in enumerate(tokens):
            entry = self._stems.get(token.form)
            if entry is None or not token.tag.startswith("VV"):
                continue

            ending_tokens = self._following_endings(tokens, index)
            if not ending_tokens:
                continue

            prefix_token = self._prefix_token(tokens, index, normalized)
            start = prefix_token.start if prefix_token else token.start
            final_token = ending_tokens[-1]
            end = final_token.start + final_token.len

            results.append(
                DetectionResult(
                    surface=normalized[start:end],
                    matched_surface=token.form,
                    term=entry.term,
                    language=entry.language.value,
                    prefix=prefix_token.form if prefix_token else None,
                    meaning=entry.meaning,
                    standard_expression=entry.standard_expression,
                    match_type=MatchType.MORPHOLOGY_LEMMA,
                    confidence=0.92,
                    start=start,
                    end=end,
                )
            )
        return results

    @staticmethod
    def _following_endings(tokens: list[Token], index: int) -> list[Token]:
        endings: list[Token] = []
        previous_end = tokens[index].start + tokens[index].len
        for token in tokens[index + 1 :]:
            if token.start != previous_end or not token.tag.startswith(ENDING_TAGS):
                break
            endings.append(token)
            previous_end = token.start + token.len
        return endings

    @staticmethod
    def _prefix_token(
        tokens: list[Token], index: int, normalized: str
    ) -> Token | None:
        if index == 0:
            return None
        previous = tokens[index - 1]
        if previous.form not in KOREAN_EMPHASIS_PREFIXES:
            return None
        between = normalized[previous.start + previous.len : tokens[index].start]
        return previous if not between or between.isspace() else None

