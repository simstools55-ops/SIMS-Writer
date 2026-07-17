#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    [sys.executable, "-m", "pytest"],
    [sys.executable, "tools/validators/validate_knowledge.py"],
    [sys.executable, "tools/validators/validate_patterns.py"],
    [sys.executable, "tools/validators/validate_quality_rules.py"],
    [sys.executable, "tools/validators/validate_claude_package.py"],
    [sys.executable, "tests/migration/test_sims_core_migration.py"],
]


def main() -> int:
    failures: list[str] = []
    for command in COMMANDS:
        label = " ".join(command[1:])
        print(f"\n=== {label} ===", flush=True)
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode != 0:
            failures.append(label)
    passed = len(COMMANDS) - len(failures)
    print(f"\nRepository release gate: {passed}/{len(COMMANDS)} passed")
    if failures:
        print("Failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
