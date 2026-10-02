#!/usr/bin/env python3
"""Install this repository's Claude Code skills and subagents.

Usage: python install.py [--force] [--dry-run] [--list]
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILLS_SOURCE = ROOT / "skills"
AGENTS_SOURCE = ROOT / "agents"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="replace existing installed items")
    parser.add_argument("--dry-run", action="store_true", help="show actions without writing")
    parser.add_argument("--list", action="store_true", help="list source skills and agents, then exit")
    return parser.parse_args(argv)


def items() -> tuple[list[Path], list[Path]]:
    skills = sorted(path for path in SKILLS_SOURCE.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    agents = sorted(AGENTS_SOURCE.glob("*.md"))
    return skills, agents


def print_list(skills: list[Path], agents: list[Path]) -> None:
    print("Skills:")
    print(*(path.name for path in skills), sep="\n")
    print("\nAgents:")
    print(*(path.name for path in agents), sep="\n")


def install_item(source: Path, destination_dir: Path, *, force: bool, dry_run: bool) -> None:
    destination = destination_dir / source.name
    if destination.exists() or destination.is_symlink():
        if not force:
            print(f"  skip (exists): {source.name}")
            return
        if not dry_run:
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
    print(f"  install: {source.name} -> {destination_dir}")
    if dry_run:
        return
    if source.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    skills, agents = items()
    if args.list:
        print_list(skills, agents)
        return 0

    home = Path(os.environ.get("HOME", str(Path.home())))
    skills_destination = home / ".claude" / "skills"
    agents_destination = home / ".claude" / "agents"
    if not args.dry_run:
        skills_destination.mkdir(parents=True, exist_ok=True)
        agents_destination.mkdir(parents=True, exist_ok=True)

    print("== Skills ==")
    for skill in skills:
        install_item(skill, skills_destination, force=args.force, dry_run=args.dry_run)
    print("== Agents ==")
    for agent in agents:
        install_item(agent, agents_destination, force=args.force, dry_run=args.dry_run)
    print("\nDry run complete, nothing was written." if args.dry_run else "\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
