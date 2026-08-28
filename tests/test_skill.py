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
)

ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "learn"
SKILL_PATH = SKILL_ROOT / "SKILL.md"
CORE_PATH = SKILL_ROOT / "references" / "core-workflows.md"
SUPPLEMENTAL_PATH = SKILL_ROOT / "references" / "supplemental-methods.md"
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
OPENAI_PATH = SKILL_ROOT / "agents" / "openai.yaml"
README_PATHS = (ROOT / "README.md", ROOT / "README.en.md")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def local_markdown_links(path: Path) -> list[Path]:
    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", read_text(path))
    targets: list[Path] = []
    for link in links:
        target = link.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+://", target, re.IGNORECASE):
            continue
        targets.append((path.parent / target).resolve())
    return targets


class SkillStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = read_text(SKILL_PATH)
        cls.core_text = read_text(CORE_PATH)
        cls.supplemental_text = read_text(SUPPLEMENTAL_PATH)
        cls.metadata, cls.skill_body = parse_frontmatter(cls.skill_text)
        cls.evals = load_json_strict(EVALS_PATH)
        cls.openai_text = read_text(OPENAI_PATH)

    def test_frontmatter_and_agent_metadata(self) -> None:
        self.assertEqual(self.metadata["name"], SKILL_ROOT.name)
        self.assertLessEqual(len(self.metadata["name"]), MAX_NAME_LENGTH)
        self.assertLessEqual(len(self.metadata["description"]), MAX_DESCRIPTION_LENGTH)
        self.assertTrue(self.metadata["description"].startswith("This skill should be used when"))
        self.assertIn("$learn", self.openai_text)

    def test_skill_is_a_lean_progressive_router(self) -> None:
        self.assertLess(len(self.skill_text.splitlines()), 120)
        self.assertIn("references/core-workflows.md", self.skill_text)
        self.assertIn("references/supplemental-methods.md", self.skill_text)
        self.assertIn("Adaptive assessment", self.skill_text)
        self.assertIn("Supplemental study support", self.skill_text)

    def test_trusted_state_and_interaction_boundaries(self) -> None:
        self.assertIn("trusted state visible", self.skill_text)
        self.assertIn("bare numbered continuation", self.skill_text)
        self.assertIn("ask exactly one question at a time and stop", self.skill_text)
        self.assertIn("Do not claim the learner understands", self.skill_text)
        self.assertIn("No evidenced error yet", self.skill_text)

    def test_canonical_core_workflows(self) -> None:
        headings = re.findall(r"^## ([1-6])\. ", self.core_text, re.MULTILINE)
        self.assertEqual(headings, ["1", "2", "3", "4", "5", "6"])
        for level in (
            "Complete Beginner",
            "Basic Understanding",
            "Practical User",
            "Problem Solver",
            "Independent Project Builder",
        ):
            self.assertIn(level, self.core_text)

    def test_twenty_hour_plan_is_staged(self) -> None:
        self.assertIn("compact 10-row map", self.core_text)
        self.assertIn("fully expand only Sessions 1–2", self.core_text)
        self.assertIn("`Covered` and `Remaining`", self.core_text)
        self.assertIn("Five active-recall questions", self.core_text)

    def test_assessment_profiles_are_disjoint(self) -> None:
        self.assertIn("Quick Active Recall", self.core_text)
        self.assertIn("3–7 primary questions", self.core_text)
        edge_hits = [line for line in self.core_text.splitlines() if "exactly 10 primary questions" in line]
        self.assertEqual(len(edge_hits), 1)
        self.assertIn("Edge Quiz", edge_hits[0])
        self.assertIn("8–12 primary questions", self.core_text)
        self.assertIn("Solid`, `Shaky`, `Misconception`, or `Blind spot", self.core_text)

    def test_cheat_sheet_and_resource_limits(self) -> None:
        self.assertIn("400–700 Chinese characters or 350–600 English words", self.core_text)
        self.assertIn("Never pad the list", self.core_text)
        schedule = [line for line in self.core_text.splitlines() if "A seven-day plan" in line]
        self.assertEqual(len(schedule), 1)
        self.assertIn("only when", schedule[0])

    def test_source_retention_and_error_evidence(self) -> None:
        self.assertIn("Label direct source claims", self.supplemental_text)
        self.assertIn("learner supplies closed-source evidence", self.supplemental_text)
        self.assertIn("D0, D1, D3, D7, D14, D30, D60, and D120", self.supplemental_text)
        self.assertIn("Create an error entry only from evidence", self.supplemental_text)

    def test_behavior_evals_are_current_and_complete(self) -> None:
        validate_behavior_evals(self.evals, SKILL_ROOT)
        cases = self.evals["evals"]
        self.assertEqual([case["id"] for case in cases], list(range(1, 24)))
        prompts = "\n".join(case["prompt"] for case in cases)
        for phrase in ("20小时", "费曼", "官方资源", "错题本", "间隔复习"):
            self.assertIn(phrase, prompts)
        self.assertTrue(any("code repair task" in case["expected_output"] for case in cases))

    def test_local_markdown_links_exist(self) -> None:
        markdown_files = [SKILL_PATH, CORE_PATH, SUPPLEMENTAL_PATH, *README_PATHS]
        missing = [
            target
            for source in markdown_files
            for target in local_markdown_links(source)
            if not target.exists()
        ]
        self.assertEqual(missing, [])

    def test_obsolete_architecture_files_are_absent(self) -> None:
        obsolete = (
            SKILL_ROOT / "references" / "templates.md",
            SKILL_ROOT / "evals" / "contract_evals.json",
            SKILL_ROOT / "evals" / "trigger_evals.json",
            SKILL_ROOT / "evals" / "stateful_transcripts.json",
        )
        self.assertTrue(all(not path.exists() for path in obsolete))

    def test_readmes_describe_current_structure_and_limits(self) -> None:
        for path in README_PATHS:
            text = read_text(path)
            self.assertIn("23", text, path.name)
            self.assertIn("core-workflows.md", text, path.name)
            self.assertIn("supplemental-methods.md", text, path.name)
            self.assertNotIn("references/templates.md", text, path.name)
            self.assertIn("does not execute model", text.lower(), path.name)


if __name__ == "__main__":
    unittest.main()
