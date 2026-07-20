import json
import tempfile
import unittest
from pathlib import Path

from slangchat.data.loader import DatasetValidationError, load_entries


class DatasetValidationTests(unittest.TestCase):
    def test_sample_dataset_is_valid(self) -> None:
        entries = load_entries("data/slang.json")
        self.assertEqual(len(entries), 6)
        self.assertEqual({entry.language.value for entry in entries}, {"ko", "en"})

    def test_duplicate_surface_forms_are_rejected(self) -> None:
        source = json.loads(Path("data/slang.json").read_text(encoding="utf-8"))
        source[1]["variants"].append("킹받네")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "invalid.json"
            target.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(
                DatasetValidationError, "surface-form collisions"
            ):
                load_entries(target)

    def test_language_must_match_id_prefix(self) -> None:
        source = json.loads(Path("data/slang.json").read_text(encoding="utf-8"))
        source[0]["language"] = "en"
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "invalid.json"
            target.write_text(json.dumps(source, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(
                DatasetValidationError, "id prefix must match language"
            ):
                load_entries(target)


if __name__ == "__main__":
    unittest.main()
