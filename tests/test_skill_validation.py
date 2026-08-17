from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests.skill_validation import (
    load_json_strict,
    parse_frontmatter,
    validate_behavior_evals,
    validate_contract_evals,
    validate_stateful_evals,
    validate_trigger_evals,
)

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "learn"


def behavior_case(
    *,
    prompt: object = "prompt",
    files: object = None,
    skill_name: object = "learn",
) -> dict[str, object]:
    return {
        "skill_name": skill_name,
        "evals": [
            {
                "id": 1,
                "prompt": prompt,
                "expected_output": "output",
                "files": [] if files is None else files,
                "expectations": ["expectation"],
            }
        ],
    }


def stateful_case(
    *,
    format_name: object = "stateful-transcript-fixtures-v1",
    role: object = "assistant",
) -> dict[str, object]:
    return {
        "format": format_name,
        "purpose": "test",
        "cases": [
            {
                "name": "case",
                "messages": [
                    {"role": role, "content": "context"},
                    {"role": "user", "content": "request"},
                ],
                "expectations": ["expectation"],
            }
        ],
    }


class FrontmatterValidationTests(unittest.TestCase):
    def test_accepts_metadata_at_length_limits(self) -> None:
        name = "a" * 64
        description = "d" * 1024
        metadata, _ = parse_frontmatter(
            f"---\nname: {name}\ndescription: |\n  {description}\n---\nBody"
        )
        self.assertEqual(metadata, {"name": name, "description": description})

    def test_rejects_metadata_over_length_limits(self) -> None:
        documents = (
            f"---\nname: {'a' * 65}\ndescription: |\n  test\n---\nBody",
            f"---\nname: learn\ndescription: |\n  {'d' * 1025}\n---\nBody",
        )
        for document in documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_frontmatter(document)

    def test_rejects_duplicate_and_malformed_fields(self) -> None:
        invalid_documents = (
            "---\nname: learn\nname: other\ndescription: |\n  test\n---\nBody",
            "---\nname: [learn\ndescription: |\n  test\n---\nBody",
            "---\nname: learn\ndescription: |\n  \n---\nBody",
            "---\nname: |\n  NOT A SLUG!\ndescription: |\n  test\n---\nBody",
        )
        for document in invalid_documents:
            with self.subTest(document=document), self.assertRaises(ValueError):
                parse_frontmatter(document)

    def test_rejects_ambiguous_plain_scalars(self) -> None:
        invalid_values = (
            "valid: broken",
            "# comment",
            "- item",
            "true",
            "2026-08-14",
        )
        for value in invalid_values:
            document = f"---\nname: learn\ndescription: {value}\n---\nBody"
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_frontmatter(document)

    def test_rejects_yaml_implicit_names(self) -> None:
        invalid_names = (
            "true",
            "false",
            "null",
            "yes",
            "no",
            "on",
            "off",
            "123",
            "0x10",
            "0o10",
            "0b10",
            "2026-08-14",
        )
        for name in invalid_names:
            document = f"---\nname: {name}\ndescription: |\n  test\n---\nBody"
            with self.subTest(name=name), self.assertRaises(ValueError):
                parse_frontmatter(document)


class JsonValidationTests(unittest.TestCase):
    def test_rejects_non_finite_numbers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            for index, value in enumerate(("NaN", "Infinity", "-Infinity")):
                path = Path(directory) / f"non-finite-{index}.json"
                path.write_text(f'{{"value": {value}}}', encoding="utf-8")
                with self.subTest(value=value), self.assertRaises(ValueError):
                    load_json_strict(path)

    def test_rejects_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate-key.json"
            path.write_text('{"key": 1, "key": 2}', encoding="utf-8")
            with self.assertRaises(ValueError):
                load_json_strict(path)

    def test_behavior_skill_name_matches_directory(self) -> None:
        with self.assertRaises(ValueError):
            validate_behavior_evals(behavior_case(skill_name="other"), SKILL_ROOT)

    def test_behavior_type_and_path_failures_are_independent(self) -> None:
        with self.assertRaises(ValueError):
            validate_behavior_evals(behavior_case(prompt=42), SKILL_ROOT)
        with self.assertRaises(ValueError):
            validate_behavior_evals(behavior_case(files=["../escape.md"]), SKILL_ROOT)

    def test_contract_format_is_versioned(self) -> None:
        data = {
            "format": "garbage",
            "reference": "references/templates.md",
            "purpose": "test",
            "evals": behavior_case()["evals"],
        }
        with self.assertRaises(ValueError):
            validate_contract_evals(data, SKILL_ROOT)

    def test_trigger_requires_boolean_decision(self) -> None:
        with self.assertRaises(ValueError):
            validate_trigger_evals([{"query": "query", "should_trigger": "yes"}])

    def test_stateful_format_is_versioned(self) -> None:
        with self.assertRaises(ValueError):
            validate_stateful_evals(stateful_case(format_name="garbage"))

    def test_stateful_role_type_returns_validation_error(self) -> None:
        with self.assertRaises(ValueError):
            validate_stateful_evals(stateful_case(role=[]))


if __name__ == "__main__":
    unittest.main()
