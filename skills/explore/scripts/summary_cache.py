#!/usr/bin/env python3
"""Check or write mirrored file summaries without trusting stale source content."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

HASH_LINE = re.compile(r"<!-- explore-sha256: ([0-9a-f]{64}) -->")
SOURCE_LINE = re.compile(r"<!-- explore-source: (.+) -->")
DOCUMENTATION_SUFFIXES = frozenset({".md", ".mdx", ".markdown", ".rst", ".adoc"})
DOCUMENTATION_DIRECTORIES = frozenset({"doc", "docs", "documentation"})


def is_documentation(relative: Path) -> bool:
    """Return whether this source should be read without a mirrored summary."""
    return relative.suffix.lower() in DOCUMENTATION_SUFFIXES or any(
        part.lower() in DOCUMENTATION_DIRECTORIES for part in relative.parts[:-1]
    )


def source_and_summary(repo: Path, source_name: str) -> tuple[Path, Path]:
    """Resolve a repository source and its mirrored summary path safely."""
    root = repo.resolve()
    if Path(source_name).is_absolute():
        raise ValueError("source must be repository-relative")
    source = (root / source_name).resolve()
    try:
        relative = source.relative_to(root)
    except ValueError as error:
        raise ValueError("source must be inside the repository") from error
    if source == root or relative.parts[0] == "summaries":
        raise ValueError("source must be a repository file outside summaries/")
    summary = root / "summaries" / f"{relative.as_posix()}.md"
    try:
        summary.resolve().relative_to(root)
    except ValueError as error:
        raise ValueError("summary path must be inside the repository") from error
    return source, summary


def source_hash(source: Path) -> str:
    """Hash source bytes with CRLF normalized to LF across checkouts."""
    return hashlib.sha256(source.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def accepted_source_hashes(source: Path) -> set[str]:
    """Accept canonical hashes and hashes written from older CRLF checkouts."""
    normalized = source.read_bytes().replace(b"\r\n", b"\n")
    return {
        hashlib.sha256(normalized).hexdigest(),
        hashlib.sha256(normalized.replace(b"\n", b"\r\n")).hexdigest(),
    }


def status(repo: Path, source_name: str) -> tuple[str, Path]:
    """Report whether a source has an eligible and fresh summary."""
    source, summary = source_and_summary(repo, source_name)
    if is_documentation(source.relative_to(repo.resolve())):
        return "skipped", summary
    if not source.is_file():
        return "missing-source", summary
    if not summary.is_file():
        return "missing", summary
    lines = summary.read_text(encoding="utf-8").splitlines()
    source_match = SOURCE_LINE.fullmatch(lines[0]) if len(lines) > 0 else None
    hash_match = HASH_LINE.fullmatch(lines[1]) if len(lines) > 1 else None
    relative = source.relative_to(repo.resolve()).as_posix()
    fresh = (
        hash_match is not None
        and source_match is not None
        and hash_match.group(1) in accepted_source_hashes(source)
        and source_match.group(1) == relative
    )
    return ("fresh" if fresh else "stale"), summary


def write_summary(repo: Path, source_name: str, body: str) -> Path:
    """Write a summary for an eligible source with its current hash."""
    source, summary = source_and_summary(repo, source_name)
    if is_documentation(source.relative_to(repo.resolve())):
        raise ValueError("documentation files do not have mirrored summaries")
    if not source.is_file():
        raise FileNotFoundError(f"missing source: {source_name}")
    relative = source.relative_to(repo.resolve()).as_posix()
    content = (
        f"<!-- explore-source: {relative} -->\n"
        f"<!-- explore-sha256: {source_hash(source)} -->\n\n"
        f"{body.strip()}\n"
    )
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(content, encoding="utf-8")
    return summary


def main(argv: list[str] | None = None) -> int:
    """Run the check or write command for one repository source."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "write"):
        sub = commands.add_parser(command)
        sub.add_argument("--repo", required=True, type=Path)
        sub.add_argument("--source", required=True)
        if command == "write":
            sub.add_argument("--body-file", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            result, summary = status(args.repo, args.source)
            print(f"{result}\t{summary}")
        else:
            print(write_summary(args.repo, args.source, args.body_file.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
