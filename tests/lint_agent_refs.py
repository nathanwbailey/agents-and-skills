import re
import sys
from pathlib import Path

MODEL = "claude-sonnet-5"
EFFORT = "medium"
REF_PATTERNS = [
    re.compile(r"subagent_type`?[:=]\s*[`\"']?([A-Za-z][\w-]*)"),
    re.compile(r"agentName=([A-Za-z][\w-]*)"),
    re.compile(r"the `([A-Za-z][\w-]*)` subagent"),
]


def agent_names(root: Path) -> set[str]:
    names = set()
    for f in (root / "agents").glob("*.md"):
        m = re.search(r"^name:\s*(\S+)", f.read_text(), re.M)
        if m:
            names.add(m.group(1))
    return names


def lint(root: Path) -> list[str]:
    root = Path(root)
    known = agent_names(root)
    problems = []

    for f in sorted((root / "agents").glob("*.md")):
        fm = f.read_text().split("\n---\n", 1)[0]
        for key, want in (("model", MODEL), ("effort", EFFORT)):
            m = re.search(rf"^{key}:\s*(\S+)", fm, re.M)
            if not m or m.group(1) != want:
                problems.append(f"agents/{f.name} must set {key}: {want}")

    for skill in sorted((root / "skills").rglob("*.md")):
        text = skill.read_text()
        rel = skill.relative_to(root)
        if re.search(r"^\s*- `model`:", text, re.M):
            problems.append(f"{rel} passes model at spawn, overriding the agent pin")
        refs = {m for p in REF_PATTERNS for m in p.findall(text)}
        for name in sorted(refs - known):
            problems.append(f"{rel} references unknown agent '{name}'")
    return problems


if __name__ == "__main__":
    found = lint(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    print("\n".join(found) or "ok")
    sys.exit(1 if found else 0)
