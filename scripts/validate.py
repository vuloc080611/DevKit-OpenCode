#!/usr/bin/env python3
"""Validate devkit-opencode repository structure, skills, commands, JSONC config, and links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_CORE_SKILLS = {
    "grill-me",
    "spec-writer",
    "project-planner",
    "architecture-decision",
    "tdd-workflow",
    "incremental-implementation",
    "systematic-debugging",
    "verification-before-done",
    "code-review",
    "security-review",
    "performance-review",
    "refactor-safe",
    "code-simplification",
    "git-commit",
    "changelog-generator",
    "readme-generator",
    "docs-writer",
    "api-designer",
    "database-schema",
    "frontend-component",
    "docker-setup",
    "dsa-explainer",
    "leetcode-helper",
    "assignment-helper",
}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", re.S)
FENCE_RE = re.compile(r"```.*?```", re.S)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)")


def strip_jsonc_comments(raw: str) -> str:
    """Strip // line comments and /* */ block comments outside JSON string literals."""
    out: list[str] = []
    i = 0
    n = len(raw)
    in_string = False
    escaped = False

    while i < n:
        ch = raw[i]
        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
            continue

        if ch == '"':
            in_string = True
            out.append(ch)
            i += 1
        elif raw.startswith("//", i):
            while i < n and raw[i] != "\n":
                i += 1
        elif raw.startswith("/*", i):
            end = raw.find("*/", i + 2)
            i = n if end == -1 else end + 2
        else:
            out.append(ch)
            i += 1

    return "".join(out)


def check_markdown_links(md_file: Path, errors: list[str]) -> None:
    """Verify relative links outside fenced code blocks resolve to existing paths."""
    content = FENCE_RE.sub("", md_file.read_text(encoding="utf-8"))
    for target in LINK_RE.findall(content):
        target = target.strip()
        if not target or target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            rel = md_file.relative_to(ROOT)
            errors.append(f"{rel}: broken relative link `{target}`")


def validate_skills(errors: list[str]) -> list[str]:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        errors.append("Missing skills/ directory")
        return []

    discovered = sorted(p.name for p in skills_dir.iterdir() if p.is_dir())
    missing_core = REQUIRED_CORE_SKILLS - set(discovered)
    if missing_core:
        errors.append(f"Missing core skills: {sorted(missing_core)}")

    for skill in discovered:
        if not NAME_RE.match(skill) or len(skill) > 64:
            errors.append(f"skills/{skill}: directory name must match ^[a-z0-9]+(-[a-z0-9]+)*$ and <= 64 chars")

        md_path = skills_dir / skill / "SKILL.md"
        if not md_path.is_file():
            errors.append(f"skills/{skill}: missing SKILL.md")
            continue

        text = md_path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"skills/{skill}/SKILL.md: missing or malformed YAML frontmatter")
            continue

        fm_text, body = match.group(1), match.group(2)
        fm_name = re.search(r"^name:\s*(.+)$", fm_text, re.M)
        fm_desc = re.search(r"^description:\s*(.+)$", fm_text, re.M)
        fm_compat = re.search(r"^compatibility:\s*(.+)$", fm_text, re.M)

        if not fm_name or fm_name.group(1).strip() != skill:
            errors.append(f"skills/{skill}/SKILL.md: frontmatter `name` does not match directory `{skill}`")

        if not fm_desc:
            errors.append(f"skills/{skill}/SKILL.md: missing frontmatter `description`")
        else:
            desc = fm_desc.group(1).strip()
            if not (1 <= len(desc) <= 1024):
                errors.append(f"skills/{skill}/SKILL.md: `description` length {len(desc)} outside 1..1024")

        if not fm_compat or "opencode" not in fm_compat.group(1).lower():
            errors.append(f"skills/{skill}/SKILL.md: `compatibility` must specify opencode")

        if "## Step-by-Step" not in body and "## Mandatory" not in body:
            errors.append(f"skills/{skill}/SKILL.md: missing Step-by-Step / Mandatory workflow section")
        if "## Anti-Patterns" not in body:
            errors.append(f"skills/{skill}/SKILL.md: missing Anti-Patterns section")
        if "## Examples" not in body:
            errors.append(f"skills/{skill}/SKILL.md: missing Examples section")

        check_markdown_links(md_path, errors)

    return discovered


def validate_commands(errors: list[str]) -> list[str]:
    commands_dir = ROOT / "commands"
    if not commands_dir.is_dir():
        return []

    cmds = sorted(p for p in commands_dir.glob("*.md") if p.is_file())
    for cmd_path in cmds:
        text = cmd_path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"commands/{cmd_path.name}: missing or malformed YAML frontmatter")
            continue
        fm_text, body = match.group(1), match.group(2)
        fm_desc = re.search(r"^description:\s*(.+)$", fm_text, re.M)
        fm_agent = re.search(r"^agent:\s*(.+)$", fm_text, re.M)

        if not fm_desc or not fm_desc.group(1).strip():
            errors.append(f"commands/{cmd_path.name}: missing frontmatter `description`")
        if fm_agent and fm_agent.group(1).strip() not in {"build", "plan"}:
            errors.append(f"commands/{cmd_path.name}: invalid `agent` `{fm_agent.group(1).strip()}`")
        if not body.strip():
            errors.append(f"commands/{cmd_path.name}: empty prompt template body")

    return [p.stem for p in cmds]


def validate_config(skills: list[str], errors: list[str]) -> None:
    jsonc_path = ROOT / "config" / "opencode.jsonc.example"
    if not jsonc_path.is_file():
        errors.append("Missing config/opencode.jsonc.example")
        return

    try:
        cfg = json.loads(strip_jsonc_comments(jsonc_path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        errors.append(f"config/opencode.jsonc.example: invalid JSONC ({exc})")
        return

    skill_perms = cfg.get("permission", {}).get("skill", {})
    missing = set(skills) - set(skill_perms.keys())
    if missing:
        errors.append(f"config/opencode.jsonc.example: missing skills under permission.skill: {sorted(missing)}")


def validate_docs(skills: list[str], errors: list[str]) -> None:
    for rel in ["AGENTS.md", "README.md", "INSTALL.md", "LICENSE"]:
        if not (ROOT / rel).is_file():
            errors.append(f"Missing required root file: {rel}")

    agents_path = ROOT / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        for skill in skills:
            if f"`{skill}`" not in agents_text:
                errors.append(f"AGENTS.md: missing skill reference `{skill}`")

    doc_candidates = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "INSTALL.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CHANGELOG.md",
    ]
    if (ROOT / "docs").is_dir():
        doc_candidates.extend(sorted((ROOT / "docs").glob("*.md")))

    for doc in doc_candidates:
        if doc.is_file():
            check_markdown_links(doc, errors)


def main() -> int:
    errors: list[str] = []
    skills = validate_skills(errors)
    commands = validate_commands(errors)
    validate_config(skills, errors)
    validate_docs(skills, errors)

    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"VALIDATION PASSED: {len(skills)} skills, {len(commands)} commands, "
        "AGENTS.md, opencode.jsonc.example, and all Markdown links verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
