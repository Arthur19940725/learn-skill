from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

FRONTMATTER_BOUNDARY = "---"
ALLOWED_FRONTMATTER_FIELDS = {"name", "description"}
BEHAVIOR_EVAL_FIELDS = {"id", "prompt", "expected_output", "files"}
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
NAME_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
YAML_IMPLICIT_NAME_PATTERN = re.compile(
    r"(?:true|false|null|yes|no|on|off|~|[+-]?[0-9][0-9_]*|0[xob][0-9a-f_]+|[0-9]{4}-[0-9]{2}-[0-9]{2})",
    re.IGNORECASE,
)


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    for index, item in enumerate(value):
        _require_nonempty_string(item, f"{label}[{index}]")
    return value


def _parse_quoted_description(raw_value: str) -> str:
    try:
        value = json.loads(raw_value)
    except json.JSONDecodeError as error:
        raise ValueError("frontmatter description must use a quoted or block scalar") from error
    return _require_nonempty_string(value, "frontmatter description")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != FRONTMATTER_BOUNDARY:
        raise ValueError("SKILL.md must start with a frontmatter boundary")

    try:
        end_index = lines.index(FRONTMATTER_BOUNDARY, 1)
    except ValueError as error:
        raise ValueError("SKILL.md frontmatter is not closed") from error

    frontmatter_lines = lines[1:end_index]
    metadata: dict[str, str] = {}
    index = 0
    while index < len(frontmatter_lines):
        line = frontmatter_lines[index]
        match = re.fullmatch(r"([a-z][a-z0-9-]*):(?:\s+(.*))?", line)
        if not match:
            raise ValueError(f"unsupported or malformed frontmatter line: {line!r}")

        key, raw_value = match.groups()
        if key not in ALLOWED_FRONTMATTER_FIELDS:
            raise ValueError(f"unsupported frontmatter field: {key}")
        if key in metadata:
            raise ValueError(f"duplicate frontmatter field: {key}")

        if raw_value == "|":
            if key != "description":
                raise ValueError("frontmatter name must use a plain slug scalar")
            block_lines: list[str] = []
            index += 1
            while index < len(frontmatter_lines) and frontmatter_lines[index].startswith("  "):
                block_lines.append(frontmatter_lines[index][2:])
                index += 1
            metadata[key] = _require_nonempty_string(
                "\n".join(block_lines).strip(), "frontmatter description"
            )
            continue

        normalized = raw_value.strip() if raw_value is not None else ""
        if key == "description":
            metadata[key] = _parse_quoted_description(normalized)
        else:
            if (
                not NAME_PATTERN.fullmatch(normalized)
                or YAML_IMPLICIT_NAME_PATTERN.fullmatch(normalized)
                or len(normalized) > MAX_NAME_LENGTH
            ):
                raise ValueError(
                    f"frontmatter name must be a lowercase hyphenated slug of at most {MAX_NAME_LENGTH} characters"
                )
            metadata[key] = normalized
        index += 1

    if set(metadata) != ALLOWED_FRONTMATTER_FIELDS:
        missing = sorted(ALLOWED_FRONTMATTER_FIELDS - set(metadata))
        raise ValueError(f"missing frontmatter fields: {missing}")
    if len(metadata["description"]) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"frontmatter description must be at most {MAX_DESCRIPTION_LENGTH} characters"
        )

    body = "\n".join(lines[end_index + 1 :])
    if not body.strip():
        raise ValueError("SKILL.md body must not be empty")
    return metadata, body


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_nonstandard_constant(value: str) -> None:
    raise ValueError(f"invalid JSON constant: {value}")


def load_json_strict(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonstandard_constant,
        )
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error


def _validate_attachment(skill_root: Path, relative_path: str, label: str) -> None:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must stay inside the skill directory")
    resolved_root = skill_root.resolve()
    resolved_path = (skill_root / path).resolve()
    if resolved_root not in resolved_path.parents or not resolved_path.is_file():
        raise ValueError(f"{label} does not exist inside the skill: {relative_path}")


def validate_behavior_evals(data: Any, skill_root: Path) -> None:
    if not isinstance(data, dict) or set(data) != {"skill_name", "evals"}:
        raise ValueError("behavior eval root must contain exactly skill_name and evals")
    skill_name = _require_nonempty_string(data["skill_name"], "skill_name")
    if skill_name != skill_root.name:
        raise ValueError(
            f"behavior eval skill_name must match directory name: {skill_root.name}"
        )

    cases = data["evals"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("evals must be a non-empty list")
    seen_ids: set[int] = set()
    for index, case in enumerate(cases):
        label = f"evals[{index}]"
        if not isinstance(case, dict) or set(case) != BEHAVIOR_EVAL_FIELDS:
            raise ValueError(f"{label} has invalid fields")
        case_id = case["id"]
        if not isinstance(case_id, int) or isinstance(case_id, bool) or case_id <= 0:
            raise ValueError(f"{label}.id must be a positive integer")
        if case_id in seen_ids:
            raise ValueError(f"duplicate eval id: {case_id}")
        seen_ids.add(case_id)
        _require_nonempty_string(case["prompt"], f"{label}.prompt")
        _require_nonempty_string(case["expected_output"], f"{label}.expected_output")
        files = _require_string_list(case["files"], f"{label}.files")
        for file_index, relative_path in enumerate(files):
            _validate_attachment(skill_root, relative_path, f"{label}.files[{file_index}]")
