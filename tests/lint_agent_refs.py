import re
import sys
from pathlib import Path

TEMPLATE = "explorer.prompt.tmpl"
TEMPLATE_PLACEHOLDERS = {"QUESTION", "ANCHOR", "DEPTH", "ANGLE", "OUTPUT_EXTRAS"}
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

    template = root / "agents" / TEMPLATE
    if not template.exists():
        problems.append(f"agents/{TEMPLATE} is missing")
    else:
        found = set(re.findall(r"\{([A-Z_]+)\}", template.read_text()))
        if found != TEMPLATE_PLACEHOLDERS:
            problems.append(f"agents/{TEMPLATE} placeholders {sorted(found)} != {sorted(TEMPLATE_PLACEHOLDERS)}")

    for skill in sorted((root / "skills").rglob("*.md")):
        text = skill.read_text()
        rel = skill.relative_to(root)
        refs = {m for p in REF_PATTERNS for m in p.findall(text)}
        for name in sorted(refs - known):
            problems.append(f"{rel} references unknown agent '{name}'")
        if "explorer" in refs and TEMPLATE not in text:
            problems.append(f"{rel} spawns explorer without citing {TEMPLATE}")
    return problems


if __name__ == "__main__":
    found = lint(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    print("\n".join(found) or "ok")
    sys.exit(1 if found else 0)
