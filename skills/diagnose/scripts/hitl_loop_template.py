#!/usr/bin/env python3
"""Copy and edit this portable human-in-the-loop reproduction template."""

from __future__ import annotations


def step(instruction: str) -> None:
    input(f"\n>>> {instruction}\n    [Enter when done] ")


def capture(question: str) -> str:
    return input(f"\n>>> {question}\n    > ")


def main() -> None:
    step("Open the app at http://localhost:3000 and sign in.")
    errored = capture("Click the 'Export' button. Did it throw an error? (y/n)")
    error_message = capture("Paste the error message (or 'none'):")
    print("\n--- Captured ---")
    print(f"ERRORED={errored}")
    print(f"ERROR_MSG={error_message}")


if __name__ == "__main__":
    main()
