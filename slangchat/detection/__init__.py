"""Slang detection and text normalization."""

from slangchat.detection.dictionary import DictionarySlangDetector
from slangchat.detection.hybrid import HybridSlangDetector
from slangchat.detection.models import DetectionResult, MatchType
from slangchat.detection.morphology import KiwiSlangDetector

__all__ = [
    "DetectionResult",
    "DictionarySlangDetector",
    "HybridSlangDetector",
    "KiwiSlangDetector",
    "MatchType",
]
