from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

FRONTMATTER_BOUNDARY = "---"
ALLOWED_FRONTMATTER_FIELDS = {"name", "description"}
BEHAVIOR_EVAL_FIELDS = {
    "id",
    "prompt",
    "expected_output",
    "files",
    "expectations",
}
STATEFUL_ROLES = {"user", "assistant", "developer", "system"}


def _require_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _require_string_list(
    value: Any, label: str, *, allow_empty: bool = False
) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    if not allow_empty and not value:
        raise ValueError(f"{label} must not be empty")
    for index, item in enumerate(value):
        _require_nonempty_string(item, f"{label}[{index}]")
    return value


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
            block_lines: list[str] = []
            index += 1
            while index < len(frontmatter_lines) and frontmatter_lines[
                index
            ].startswith("  "):
                block_lines.append(frontmatter_lines[index][2:])
                index += 1
            if not block_lines:
                raise ValueError(f"frontmatter block field {key} must not be empty")
            metadata[key] = "\n".join(block_lines).strip()
            continue

        if raw_value is None or not raw_value.strip():
            raise ValueError(f"frontmatter field {key} must not be empty")
        if raw_value[0] in "[{&*!|>'\"%@`":
            raise ValueError(
                f"frontmatter field {key} must use a plain scalar or block"
            )
        metadata[key] = raw_value.strip()
        index += 1

    if set(metadata) != ALLOWED_FRONTMATTER_FIELDS:
        missing = sorted(ALLOWED_FRONTMATTER_FIELDS - set(metadata))
        raise ValueError(f"missing frontmatter fields: {missing}")

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


def load_json_strict(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys
        )
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON in {path}: {error}") from error


def _validate_expectations(value: Any, label: str) -> None:
    _require_string_list(value, label)


def _validate_attachment(skill_root: Path, relative_path: str, label: str) -> None:
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must stay inside the skill directory")
    resolved_root = skill_root.resolve()
    resolved_path = (skill_root / path).resolve()
    if resolved_root not in resolved_path.parents:
        raise ValueError(f"{label} escapes the skill directory")
    if not resolved_path.is_file():
        raise ValueError(f"{label} does not exist: {relative_path}")


def validate_behavior_evals(data: Any, skill_root: Path) -> None:
    if not isinstance(data, dict) or set(data) != {"skill_name", "evals"}:
        raise ValueError("behavior eval root must contain exactly skill_name and evals")
    _require_nonempty_string(data["skill_name"], "skill_name")
    if not isinstance(data["evals"], list) or not data["evals"]:
        raise ValueError("evals must be a non-empty list")

    seen_ids: set[int] = set()
    for index, case in enumerate(data["evals"]):
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
        files = _require_string_list(case["files"], f"{label}.files", allow_empty=True)
        for file_index, relative_path in enumerate(files):
            _validate_attachment(
                skill_root, relative_path, f"{label}.files[{file_index}]"
            )
        _validate_expectations(case["expectations"], f"{label}.expectations")


def validate_trigger_evals(data: Any) -> None:
    if not isinstance(data, list) or not data:
        raise ValueError("trigger evals must be a non-empty list")
    seen_queries: set[str] = set()
    for index, case in enumerate(data):
        label = f"trigger_evals[{index}]"
        if not isinstance(case, dict) or set(case) != {"query", "should_trigger"}:
            raise ValueError(f"{label} has invalid fields")
        query = _require_nonempty_string(case["query"], f"{label}.query")
        if query in seen_queries:
            raise ValueError(f"duplicate trigger query: {query}")
        seen_queries.add(query)
        if not isinstance(case["should_trigger"], bool):
            raise ValueError(f"{label}.should_trigger must be boolean")


def validate_stateful_evals(data: Any) -> None:
    required_root = {"format", "purpose", "cases"}
    if not isinstance(data, dict) or set(data) != required_root:
        raise ValueError("stateful eval root has invalid fields")
    _require_nonempty_string(data["format"], "format")
    _require_nonempty_string(data["purpose"], "purpose")
    if not isinstance(data["cases"], list) or not data["cases"]:
        raise ValueError("stateful cases must be a non-empty list")

    seen_names: set[str] = set()
    for index, case in enumerate(data["cases"]):
        label = f"cases[{index}]"
        if not isinstance(case, dict) or set(case) != {
            "name",
            "messages",
            "expectations",
        }:
            raise ValueError(f"{label} has invalid fields")
        name = _require_nonempty_string(case["name"], f"{label}.name")
        if name in seen_names:
            raise ValueError(f"duplicate stateful case name: {name}")
        seen_names.add(name)
        messages = case["messages"]
        if not isinstance(messages, list) or len(messages) < 2:
            raise ValueError(f"{label}.messages must contain at least two turns")
        if not isinstance(messages[-1], dict) or messages[-1].get("role") != "user":
            raise ValueError(f"{label}.messages must end with a user turn")
        previous_role: str | None = None
        for message_index, message in enumerate(messages):
            message_label = f"{label}.messages[{message_index}]"
            if not isinstance(message, dict) or set(message) != {"role", "content"}:
                raise ValueError(f"{message_label} has invalid fields")
            role = message["role"]
            if role not in STATEFUL_ROLES:
                raise ValueError(f"{message_label}.role is invalid")
            if role == previous_role:
                raise ValueError(f"{message_label}.role repeats the previous role")
            previous_role = role
            _require_nonempty_string(message["content"], f"{message_label}.content")
        _validate_expectations(case["expectations"], f"{label}.expectations")
