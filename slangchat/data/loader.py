from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pydantic import TypeAdapter, ValidationError

from slangchat.data.schema import SlangEntry


class DatasetValidationError(ValueError):
    """Raised when a slang dataset violates cross-entry constraints."""


def load_entries(path: str | Path) -> list[SlangEntry]:
    source = Path(path)
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise DatasetValidationError(f"invalid JSON in {source}: {exc}") from exc

    try:
        entries = TypeAdapter(list[SlangEntry]).validate_python(raw)
    except ValidationError as exc:
        raise DatasetValidationError(str(exc)) from exc

    _validate_dataset(entries)
    return entries


def _validate_dataset(entries: list[SlangEntry]) -> None:
    if not entries:
        raise DatasetValidationError("dataset must contain at least one entry")

    duplicate_ids = _duplicates(entry.id for entry in entries)
    if duplicate_ids:
        raise DatasetValidationError(f"duplicate ids: {', '.join(duplicate_ids)}")

    keys = [f"{entry.language.value}:{entry.term.casefold()}" for entry in entries]
    duplicate_terms = _duplicates(keys)
    if duplicate_terms:
        raise DatasetValidationError(
            f"duplicate language/term pairs: {', '.join(duplicate_terms)}"
        )

    surface_owner: dict[tuple[str, str], str] = {}
    collisions: list[str] = []
    for entry in entries:
        for surface in [entry.term, *entry.variants]:
            key = (entry.language.value, surface.casefold())
            previous = surface_owner.get(key)
            if previous and previous != entry.id:
                collisions.append(f"{surface} ({previous}, {entry.id})")
            surface_owner[key] = entry.id
    if collisions:
        raise DatasetValidationError(f"surface-form collisions: {', '.join(collisions)}")


def _duplicates(values: object) -> list[str]:
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)

