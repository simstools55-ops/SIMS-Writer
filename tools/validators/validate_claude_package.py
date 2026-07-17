#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / "claude"
MANIFEST = CLAUDE / "manifest.json"
REQUIRED = {
    "CLAUDE_PROJECT_INSTRUCTIONS.md",
    "README.md",
    "SETUP_GUIDE.md",
    "USER_TEST_REHEARSAL.md",
    "TEST_CHECKLIST.md",
    "REAL_ARTICLE_UAT_RESULT_TEMPLATE.json",
    "knowledge/SIMS_WRITER_KNOWLEDGE_PACK.md",
    "templates/IMPROVEMENT_REQUEST_TEMPLATE.json",
    "examples/EXAMPLE_REQUEST.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    files = {str(path.relative_to(CLAUDE)).replace("\\", "/") for path in CLAUDE.rglob("*") if path.is_file() and path != MANIFEST}
    missing = sorted(REQUIRED - files)
    if missing:
        errors.append(f"missing required files: {missing}")
    if len(files) > 11:
        errors.append(f"too many distribution files: {len(files)}")
    if sum((CLAUDE / item).stat().st_size for item in files) >= 120_000:
        errors.append("distribution exceeds 120KB")

    expected = {
        "package_version": "1.15.0-preview.1",
        "status": "quality_uat_preview",
        "files": {item: sha256(CLAUDE / item) for item in sorted(files)},
    }
    if not MANIFEST.is_file():
        errors.append("manifest.json is missing")
    else:
        actual = json.loads(MANIFEST.read_text(encoding="utf-8"))
        if actual != expected:
            errors.append("manifest.json does not match distribution files")

    print(f"Claude package files: {len(files)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Claude distribution package: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
