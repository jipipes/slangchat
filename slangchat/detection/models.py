from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class MatchType(str, Enum):
    DICTIONARY_EXACT = "dictionary_exact"
    DICTIONARY_VARIANT = "dictionary_variant"
    MORPHOLOGY_LEMMA = "morphology_lemma"


class DetectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: str
    matched_surface: str
    term: str
    language: str
    prefix: str | None = None
    meaning: str
    standard_expression: str
    match_type: MatchType
    confidence: float = Field(ge=0.0, le=1.0)
    start: int = Field(ge=0)
    end: int = Field(ge=0)
