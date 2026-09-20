import re
import sys
from pathlib import Path

BANNED = re.compile(
    r"\bcursor\b|grok|gpt-5|claude-fable|claude-opus|thinking-(?:max|xhigh)|pstack|"
    r"\bcloud\b|\borigin pr\b|(?-i:\bOrigin\b)|command -v origin|"
    r"your configured|the configured|configurable|setup-pstack|\.codex",
    re.I,
)
SKIP_DIRS = {"node_modules", "__pycache__", ".git", "tests"}
SKIP_FILES = {"bun.lock"}
SKIP_PREFIXES = ("skills/poteto-mode/scripts/watch-pr/",)


def banned_terms(root: Path) -> list[str]:
    root = Path(root)
    hits = []
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if not f.is_file() or SKIP_DIRS & set(rel.parts) or f.name in SKIP_FILES:
            continue
        if str(rel).startswith(SKIP_PREFIXES):
            continue
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            m = BANNED.search(line)
            if m:
                hits.append(f"{rel}:{n} mentions '{m.group(0)}'")
    return hits


if __name__ == "__main__":
    found = banned_terms(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    print("\n".join(found) or "ok")
    sys.exit(1 if found else 0)
