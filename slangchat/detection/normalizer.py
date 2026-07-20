from __future__ import annotations

import re
import unicodedata


WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Normalize Unicode and collapse whitespace without removing punctuation."""

    normalized = unicodedata.normalize("NFKC", text)
    return WHITESPACE_PATTERN.sub(" ", normalized).strip()

