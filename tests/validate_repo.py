from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_SKILLS = {
    "architect", "arena", "blast-radius", "bro", "code-review-since",
    "codebase-design", "create-engineering-verification-skill", "diagnose",
    "domain-modeling", "explore", "grilling", "handoff", "multitask",
    "principle-prove-it-works", "principle-test-behavior-not-implementation",
    "prototype", "recall", "research", "review-session", "technical-writing",
    "test-driven-development", "to-issues", "unslop", "why", "write-a-skill",
}
REQUIRED_AGENTS = {"explorer", "general-purpose", "reviewer"}
FOREIGN = re.compile(r"codex|openai|gpt-|\.agents/|spawn_agent|list_agents|\bcursor\b", re.I)
AGENT_REF = re.compile(r"subagent_type`?\s*[:=]\s*`?[\"']?([a-z][a-z0-9-]*)")


def frontmatter(path: Path) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.S)
    values: dict[str, str] = {}
    for line in (match.group(1).splitlines() if match else []):
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def validation_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skills = {p.parent.name: p for p in (root / "skills").glob("*/SKILL.md")}
    if set(skills) != REQUIRED_SKILLS:
        errors.append(f"skill names must be {sorted(REQUIRED_SKILLS)}")
    for name, path in skills.items():
        fm = frontmatter(path)
        if fm.get("name") != name:
            errors.append(f"{path.relative_to(root)} name must match directory")
        if not fm.get("description"):
            errors.append(f"{path.relative_to(root)} missing description")
    agents = {p.stem: p for p in (root / "agents").glob("*.md")}
    if set(agents) != REQUIRED_AGENTS:
        errors.append(f"agent names must be {sorted(REQUIRED_AGENTS)}")
    for name, path in agents.items():
        fm = frontmatter(path)
        for key in ("name", "description", "model"):
            if not fm.get(key):
                errors.append(f"{path.relative_to(root)} missing {key}")
        if fm.get("name") != name:
            errors.append(f"{path.relative_to(root)} name must match filename")
    for path in [*(root / "skills").rglob("*"), *(root / "agents").rglob("*"), root / "README.md", root / "CLAUDE.md", root / "install.py"]:
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if FOREIGN.search(text):
            errors.append(f"{path.relative_to(root)} mentions a non-Claude runtime")
        if path.suffix == ".md":
            for ref in AGENT_REF.findall(text):
                if ref not in REQUIRED_AGENTS:
                    errors.append(f"{path.relative_to(root)} references unknown agent {ref!r}")
    return errors


if __name__ == "__main__":
    found = validation_errors()
    print("\n".join(found) or "ok")
    raise SystemExit(bool(found))
