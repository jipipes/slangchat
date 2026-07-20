from __future__ import annotations

import argparse
from collections import Counter

from slangchat.data.loader import DatasetValidationError, load_entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SlangChat JSON dataset")
    parser.add_argument("path", nargs="?", default="data/slang.json")
    args = parser.parse_args()

    try:
        entries = load_entries(args.path)
    except (OSError, DatasetValidationError) as exc:
        print(f"FAIL: {exc}")
        return 1

    languages = Counter(entry.language.value for entry in entries)
    verified = sum(entry.review_status.value == "verified" for entry in entries)
    summary = ", ".join(f"{language}={count}" for language, count in sorted(languages.items()))
    print(f"PASS: {len(entries)} entries ({summary}), verified={verified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

