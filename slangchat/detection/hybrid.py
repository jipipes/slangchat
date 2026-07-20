from __future__ import annotations

from collections.abc import Iterable

from slangchat.data.schema import SlangEntry
from slangchat.detection.dictionary import DictionarySlangDetector
from slangchat.detection.models import DetectionResult
from slangchat.detection.morphology import KiwiSlangDetector


class HybridSlangDetector:
    """Prefer high-confidence dictionary matches and backfill Kiwi lemma matches."""

    def __init__(self, entries: Iterable[SlangEntry]) -> None:
        materialized = list(entries)
        self._dictionary = DictionarySlangDetector(materialized)
        self._morphology = KiwiSlangDetector(materialized)

    def detect(self, text: str) -> list[DetectionResult]:
        candidates = [
            *self._dictionary.detect(text),
            *self._morphology.detect(text),
        ]
        selected: list[DetectionResult] = []
        for candidate in sorted(
            candidates,
            key=lambda item: (-item.confidence, -(item.end - item.start), item.start),
        ):
            if any(
                candidate.start < chosen.end and candidate.end > chosen.start
                for chosen in selected
            ):
                continue
            selected.append(candidate)
        return sorted(selected, key=lambda item: item.start)

