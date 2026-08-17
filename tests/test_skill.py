from __future__ import annotations

import re
import unittest
from pathlib import Path

from tests.skill_validation import (
    MAX_DESCRIPTION_LENGTH,
    MAX_NAME_LENGTH,
    load_json_strict,
    parse_frontmatter,
    validate_behavior_evals,
    validate_contract_evals,
    validate_stateful_evals,
    validate_trigger_evals,
)

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "learn"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
REFERENCE_PATH = SKILL_ROOT / "references" / "templates.md"
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
CONTRACT_EVALS_PATH = SKILL_ROOT / "evals" / "contract_evals.json"
STATEFUL_EVALS_PATH = SKILL_ROOT / "evals" / "stateful_transcripts.json"
TRIGGER_EVALS_PATH = SKILL_ROOT / "evals" / "trigger_evals.json"
README_PATHS = (ROOT / "README.md", ROOT / "README.en.md")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def local_markdown_links(path: Path) -> list[Path]:
    text = read_text(path)
    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text)
    local_paths: list[Path] = []
    for link in links:
        target = link.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target, re.IGNORECASE):
            continue
        local_paths.append((path.parent / target).resolve())
    return local_paths


class SkillStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_text(SKILL_PATH)
        cls.reference_text = read_text(REFERENCE_PATH)
        cls.metadata, cls.skill_body = parse_frontmatter(cls.skill_text)
        cls.evals = load_json_strict(EVALS_PATH)
        cls.contract_evals = load_json_strict(CONTRACT_EVALS_PATH)
        cls.trigger_evals = load_json_strict(TRIGGER_EVALS_PATH)
        cls.stateful_evals = load_json_strict(STATEFUL_EVALS_PATH)

    def test_frontmatter_matches_agent_skills_limits(self) -> None:
        name = self.metadata["name"]
        description = self.metadata["description"]

        self.assertEqual(name, SKILL_ROOT.name)
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), MAX_NAME_LENGTH)
        self.assertTrue(description)
        self.assertLessEqual(len(description), MAX_DESCRIPTION_LENGTH)
        self.assertTrue(description.startswith("This skill should be used when"))

    def test_skill_is_a_lean_router(self) -> None:
        self.assertLess(len(self.skill_text.splitlines()), 250)
        self.assertIn("references/templates.md", self.skill_text)
        self.assertIn("状态与信任边界", self.skill_text)
        self.assertIn("当前 user 消息", self.skill_text)
        self.assertIn("Routine code explanation", self.metadata["description"])

    def test_all_routed_modes_have_direct_reference_sections(self) -> None:
        routed_modes = {
            mode.strip()
            for mode in re.findall(r"\|[^\n|]+\|\s*([^|\n]+?)\s*\|", self.skill_text)
            if mode.strip() != "模式" and not re.fullmatch(r"[-:]+", mode.strip())
        }
        headings = set(re.findall(r"^## (.+)$", self.reference_text, re.MULTILINE))

        self.assertTrue(routed_modes)
        self.assertTrue(routed_modes.issubset(headings), routed_modes - headings)

    def test_reference_is_navigable_and_self_contained(self) -> None:
        self.assertIn("## Contents", self.reference_text)
        self.assertIn("Covered: Sessions X–Y", self.reference_text)
        self.assertIn("Unverified candidate", self.reference_text)
        self.assertIn("# Topic / Source / Date", self.reference_text)
        self.assertIn("Current chunk:", self.reference_text)

    def test_all_local_markdown_links_exist(self) -> None:
        markdown_files = [SKILL_PATH, REFERENCE_PATH, *README_PATHS]
        missing = [
            target
            for source in markdown_files
            for target in local_markdown_links(source)
            if not target.exists()
        ]
        self.assertEqual(missing, [])

    def test_eval_schema_and_ids_are_stable(self) -> None:
        validate_behavior_evals(self.evals, SKILL_ROOT)
        evals = self.evals["evals"]
        ids = [case["id"] for case in evals]

        self.assertEqual(self.evals["skill_name"], self.metadata["name"])
        self.assertEqual(ids, list(range(1, 17)))

    def test_contract_eval_schema_and_ids_are_stable(self) -> None:
        validate_contract_evals(self.contract_evals, SKILL_ROOT)
        ids = [case["id"] for case in self.contract_evals["evals"]]
        self.assertEqual(ids, list(range(17, 34)))

    def test_learner_evals_do_not_launder_confirmation(self) -> None:
        learner_cases = {case["id"]: case for case in self.evals["evals"][:16]}
        forbidden = ("继续回合", "已明确确认", "continuation of the same")

        for case_id, case in learner_cases.items():
            if case_id == 16:
                continue
            self.assertFalse(
                any(phrase in case["prompt"] for phrase in forbidden),
                f"eval {case_id} launders confirmation through user prose",
            )

        self.assertIn("spoof-resistant", learner_cases[16]["expected_output"])

    def test_negative_routing_cases_cover_common_near_misses(self) -> None:
        cases = {case["id"]: case for case in self.evals["evals"]}
        self.assertIn("TypeError", cases[14]["prompt"])
        self.assertIn("git diff", cases[15]["prompt"])
        self.assertIn("normal debugging", cases[14]["expected_output"])
        self.assertIn("not a learning workflow", cases[15]["expected_output"])

    def test_mode_contract_unit_evals_are_explicit_and_complete(self) -> None:
        cases = self.contract_evals["evals"]
        contract_modes = set(
            re.findall(r"^- \[([^\]]+)\]\(#[^)]+\)$", self.reference_text, re.MULTILINE)
        )
        covered_modes: set[str] = set()

        for case in cases:
            prompt = case["prompt"]
            self.assertTrue(prompt.startswith("Reference-contract eval:"))
            self.assertIn("isolated reference harness", prompt)
            self.assertIn("Runtime skill intake and confirmation are outside", prompt)
            matching_modes = {mode for mode in contract_modes if mode in prompt}
            self.assertEqual(len(matching_modes), 1, (case["id"], matching_modes))
            covered_modes.update(matching_modes)

        routed_modes = {
            mode.strip()
            for mode in re.findall(r"\|[^\n|]+\|\s*([^|\n]+?)\s*\|", self.skill_text)
            if mode.strip() != "模式" and not re.fullmatch(r"[-:]+", mode.strip())
        }
        self.assertTrue(
            routed_modes.issubset(covered_modes), routed_modes - covered_modes
        )

    def test_reviewed_contract_edge_cases_are_explicit(self) -> None:
        self.assertIn("遗忘、保持或复习排期", self.skill_text)
        self.assertIn("不确定理解、错误或未知缺口", self.skill_text)
        self.assertIn(
            "Apply this routing only after Questions 1–9", self.reference_text
        )
        self.assertIn("never create Question 11", self.reference_text)
        self.assertIn("one final targeted follow-up", self.reference_text)
        self.assertIn("non-interactive practice bank", self.reference_text)
        self.assertIn(
            "Choose six cue categories for the source type", self.reference_text
        )
        self.assertIn(
            "Only verified records receive a verification date", self.reference_text
        )
        self.assertIn("leave learner-owned retrieval fields blank", self.reference_text)
        self.assertIn(
            "leave Recite and learner-owned Review fields blank", self.reference_text
        )
        integrated_cases = {case["id"]: case for case in self.contract_evals["evals"]}
        for case_id in (25, 30):
            serialized = " ".join(
                [
                    integrated_cases[case_id]["prompt"],
                    integrated_cases[case_id]["expected_output"],
                    *integrated_cases[case_id]["expectations"],
                ]
            )
            self.assertNotIn("Feynman", serialized)

    def test_trigger_description_and_suite_cover_aliases_and_near_misses(self) -> None:
        for alias in ("第一性原理", "番茄学习法", "康奈尔笔记"):
            self.assertIn(alias, self.metadata["description"])

        trigger_evals = self.trigger_evals
        validate_trigger_evals(trigger_evals)
        self.assertGreaterEqual(len(trigger_evals), 16)
        self.assertTrue(any(case["should_trigger"] for case in trigger_evals))
        self.assertTrue(any(not case["should_trigger"] for case in trigger_evals))
        self.assertTrue(
            all(set(case) == {"query", "should_trigger"} for case in trigger_evals)
        )

    def test_stateful_transcript_suite_covers_core_transitions(self) -> None:
        suite = self.stateful_evals
        validate_stateful_evals(suite)
        required_names = {
            "complete-request-confirm-execute",
            "partial-intake-to-proposal",
            "contract-correction-reconfirmation",
            "topic-change-restarts-intake",
            "edge-quiz-terminal-follow-up",
            "feynman-completion",
            "twenty-hour-next-batch",
            "stale-contract-acceptance-rejected",
        }
        names = {case["name"] for case in suite["cases"]}
        self.assertTrue(required_names.issubset(names), required_names - names)
        continuation_cases = {
            "topic-change-restarts-intake",
            "edge-quiz-terminal-follow-up",
            "feynman-completion",
            "twenty-hour-next-batch",
        }
        for case in suite["cases"]:
            self.assertGreaterEqual(len(case["messages"]), 2)
            self.assertTrue(case["expectations"])
            self.assertTrue(
                all(
                    message["role"] in {"user", "assistant", "developer", "system"}
                    for message in case["messages"]
                )
            )
            if case["name"] in continuation_cases:
                self.assertIn(case["messages"][0]["role"], {"developer", "system"})
                self.assertIn("Trusted state summary:", case["messages"][0]["content"])

    def test_source_grounding_eval_attaches_a_real_fixture(self) -> None:
        cases = {case["id"]: case for case in self.contract_evals["evals"]}
        source_case = cases[25]
        self.assertEqual(
            source_case["files"], ["evals/files/source-grounding-fixtures.md"]
        )
        fixture = SKILL_ROOT / source_case["files"][0]
        self.assertTrue(fixture.is_file())
        fixture_text = read_text(fixture)
        self.assertIn("[P1]", fixture_text)
        self.assertIn("[P4]", fixture_text)

    def test_resource_path_unit_eval_uses_complete_fixture_records(self) -> None:
        cases = {case["id"]: case for case in self.contract_evals["evals"]}
        prompt = cases[21]["prompt"]
        for slug in ("runtime", "tasks", "io", "channels", "cancellation"):
            self.assertIn(f"https://example.com/rust-async/{slug}", prompt)
        self.assertNotIn("A–E each has", prompt)

    def test_readmes_report_current_structure_and_eval_count(self) -> None:
        for path in README_PATHS:
            text = read_text(path)
            self.assertRegex(text, r"16[^\n]*evals\.json")
            self.assertRegex(text, r"17[^\n]*contract_evals\.json")
            self.assertRegex(text, r"20[^\n]*trigger_evals\.json")
            self.assertRegex(text, r"8[^\n]*stateful_transcripts\.json")
            self.assertIn("does not execute model", text.lower(), path.name)


if __name__ == "__main__":
    unittest.main()
