#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAUDE = ROOT / "claude"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the curated SIMS Writer Claude distribution ZIP")
    parser.add_argument("--output", default=str(ROOT / "dist"))
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / "SIMS-Writer-Claude-Quality-UAT-v1.10.0.zip"
    files = sorted(path for path in CLAUDE.rglob("*") if path.is_file())
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("SIMS-Writer-Claude") / path.relative_to(CLAUDE))
    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"corrupt archive member: {bad}")
    digest = sha256_bytes(archive.read_bytes())
    report = {"status": "built", "archive": archive.name, "files": len(files), "sha256": digest}
    (output / "claude-distribution-build.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"archive={archive} files={len(files)} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
