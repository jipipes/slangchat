from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Language(str, Enum):
    KO = "ko"
    EN = "en"


class Register(str, Enum):
    INFORMAL = "informal"
    VULGAR = "vulgar"
    INTERNET = "internet"


class ReviewStatus(str, Enum):
    DRAFT = "draft"
    VERIFIED = "verified"


class SlangEntry(BaseModel):
    """A reviewed slang dictionary entry used by the detection engine."""

    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, populate_by_name=True
    )

    id: str = Field(pattern=r"^(ko|en)_\d{3}$")
    language: Language
    term: str = Field(min_length=1)
    variants: list[str] = Field(default_factory=list)
    meaning: str = Field(min_length=2)
    standard_expression: str = Field(min_length=1)
    usage_register: Register = Field(alias="register")
    intensity: int = Field(ge=1, le=5)
    example: str = Field(min_length=2)
    source: str = Field(min_length=2)
    review_status: ReviewStatus

    @field_validator("variants")
    @classmethod
    def variants_must_be_unique_and_nonempty(cls, variants: list[str]) -> list[str]:
        if any(not variant.strip() for variant in variants):
            raise ValueError("variants cannot contain empty strings")
        normalized = [variant.casefold() for variant in variants]
        if len(normalized) != len(set(normalized)):
            raise ValueError("variants must be unique")
        return variants

    @model_validator(mode="after")
    def id_language_must_match(self) -> "SlangEntry":
        if not self.id.startswith(f"{self.language.value}_"):
            raise ValueError("id prefix must match language")
        if self.term.casefold() in {variant.casefold() for variant in self.variants}:
            raise ValueError("variants must not repeat the canonical term")
        return self
