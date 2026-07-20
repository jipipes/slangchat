from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from slangchat.data.schema import Language, SlangEntry
from slangchat.detection.models import DetectionResult, MatchType
from slangchat.detection.normalizer import normalize_text


KOREAN_EMPHASIS_PREFIXES = ("완전", "개", "핵", "존", "씨")


@dataclass(frozen=True)
class _Candidate:
    entry: SlangEntry
    surface: str
    match_type: MatchType
    prefix: str | None
    pattern: re.Pattern[str]


class DictionarySlangDetector:
    """Detect reviewed dictionary terms, variants, and Korean prefixed forms."""

    def __init__(self, entries: Iterable[SlangEntry]) -> None:
        self._candidates = self._build_candidates(entries)

    def detect(self, text: str) -> list[DetectionResult]:
        normalized = normalize_text(text)
        matches: list[tuple[int, int, _Candidate, str]] = []

        for candidate in self._candidates:
            for match in candidate.pattern.finditer(normalized):
                matches.append((match.start(), match.end(), candidate, match.group(0)))

        selected: list[tuple[int, int, _Candidate, str]] = []
        for match in sorted(matches, key=self._priority):
            start, end, _, _ = match
            if any(start < chosen_end and end > chosen_start for chosen_start, chosen_end, *_ in selected):
                continue
            selected.append(match)

        return [self._to_result(match) for match in sorted(selected, key=lambda item: item[0])]

    @staticmethod
    def _priority(match: tuple[int, int, _Candidate, str]) -> tuple[int, int, int]:
        start, end, candidate, _ = match
        prefix_rank = 0 if candidate.prefix else 1
        return (prefix_rank, -(end - start), start)

    @staticmethod
    def _to_result(match: tuple[int, int, _Candidate, str]) -> DetectionResult:
        start, end, candidate, surface = match
        confidence = 0.99 if candidate.match_type == MatchType.DICTIONARY_EXACT else 0.96
        return DetectionResult(
            surface=surface,
            matched_surface=candidate.surface,
            term=candidate.entry.term,
            language=candidate.entry.language.value,
            prefix=candidate.prefix,
            meaning=candidate.entry.meaning,
            standard_expression=candidate.entry.standard_expression,
            match_type=candidate.match_type,
            confidence=confidence,
            start=start,
            end=end,
        )

    @classmethod
    def _build_candidates(cls, entries: Iterable[SlangEntry]) -> list[_Candidate]:
        candidates: list[_Candidate] = []
        for entry in entries:
            surfaces = [(entry.term, MatchType.DICTIONARY_EXACT)]
            surfaces.extend(
                (variant, MatchType.DICTIONARY_VARIANT) for variant in entry.variants
            )
            for surface, match_type in surfaces:
                candidates.append(
                    _Candidate(
                        entry=entry,
                        surface=surface,
                        match_type=match_type,
                        prefix=None,
                        pattern=cls._compile_pattern(surface),
                    )
                )
                if entry.language == Language.KO:
                    for prefix in KOREAN_EMPHASIS_PREFIXES:
                        candidates.append(
                            _Candidate(
                                entry=entry,
                                surface=surface,
                                match_type=match_type,
                                prefix=prefix,
                                pattern=cls._compile_pattern(
                                    surface, prefix=prefix
                                ),
                            )
                        )
        return candidates

    @staticmethod
    def _compile_pattern(surface: str, prefix: str | None = None) -> re.Pattern[str]:
        escaped_surface = re.escape(normalize_text(surface)).replace(r"\ ", r"\s+")
        expression = escaped_surface
        if prefix:
            expression = rf"{re.escape(prefix)}\s*{escaped_surface}"
        return re.compile(rf"(?<![\w]){expression}(?![\w])", re.IGNORECASE)

