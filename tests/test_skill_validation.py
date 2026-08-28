from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.skill_validation import (
    load_json_strict,
    parse_frontmatter,
    validate_behavior_evals,
)

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "learn"


def behavior_case(*, prompt: object = "prompt", files: object = None) -> dict[str, object]:
    return {
        "skill_name": "learn",
        "evals": [
            {
                "id": 1,
                "prompt": prompt,
                "expected_output": "output",
                "files": [] if files is None else files,
            }
        ],
    }


class FrontmatterValidationTests(unittest.TestCase):
    def test_accepts_quoted_and_block_descriptions(self) -> None:
        documents = (
            '---\nname: learn\ndescription: "Useful learning skill"\n---\nBody',
            "---\nname: learn\ndescription: |\n  Useful learning skill\n---\nBody",
        )
        for document in documents:
            with self.subTest(document=document):
                metadata, body = parse_frontmatter(document)
                self.assertEqual(metadata["name"], "learn")
                self.assertEqual(metadata["description"], "Useful learning skill")
                self.assertEqual(body, "Body")

    def test_rejects_duplicate_or_missing_fields(self) -> None:
        documents = (
            '---\nname: learn\nname: other\ndescription: "test"\n---\nBody',
            "---\nname: learn\n---\nBody",
            '---\nname: true\ndescription: "test"\n---\nBody',
        )
        for document in documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_frontmatter(document)

    def test_rejects_malformed_description(self) -> None:
        with self.assertRaises(ValueError):
            parse_frontmatter("---\nname: learn\ndescription: unquoted\n---\nBody")


class JsonValidationTests(unittest.TestCase):
    def test_rejects_duplicate_json_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"skill_name":"learn","skill_name":"other"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_json_strict(path)

    def test_rejects_non_finite_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nan.json"
            path.write_text('{"value": NaN}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_json_strict(path)

    def test_behavior_schema_accepts_current_shape(self) -> None:
        validate_behavior_evals(behavior_case(), SKILL_ROOT)

    def test_behavior_schema_rejects_extra_fields(self) -> None:
        data = behavior_case()
        data["evals"][0]["expectations"] = ["obsolete field"]
        with self.assertRaises(ValueError):
            validate_behavior_evals(data, SKILL_ROOT)

    def test_behavior_schema_rejects_duplicate_ids(self) -> None:
        data = behavior_case()
        data["evals"].append(dict(data["evals"][0]))
        with self.assertRaises(ValueError):
            validate_behavior_evals(data, SKILL_ROOT)

    def test_behavior_schema_rejects_bad_prompt_type(self) -> None:
        with self.assertRaises(ValueError):
            validate_behavior_evals(behavior_case(prompt=7), SKILL_ROOT)

    def test_behavior_schema_rejects_escaping_attachment(self) -> None:
        with self.assertRaises(ValueError):
            validate_behavior_evals(behavior_case(files=["../README.md"]), SKILL_ROOT)


if __name__ == "__main__":
    unittest.main()
