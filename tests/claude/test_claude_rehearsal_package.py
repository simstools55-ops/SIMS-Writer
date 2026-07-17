from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE = ROOT / "claude"


def test_rehearsal_guides_exist_and_state_not_user_test_ready() -> None:
    rehearsal = (CLAUDE / "USER_TEST_REHEARSAL.md").read_text(encoding="utf-8")
    checklist = (CLAUDE / "TEST_CHECKLIST.md").read_text(encoding="utf-8")
    assert "一般利用者テスト開始版ではありません" in rehearsal
    assert "manual_review_required" in rehearsal
    assert "内部リンク" in checklist
    assert "日本語品質" in checklist


def test_manifest_matches_all_distribution_files() -> None:
    completed = subprocess.run(
        [sys.executable, "tools/validators/validate_claude_package.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_distribution_builder_creates_verified_zip(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "tools/build_claude_distribution.py", "--output", str(tmp_path)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    archive = tmp_path / "SIMS-Writer-Claude-Quality-UAT-v1.14.0.zip"
    report = json.loads((tmp_path / "claude-distribution-build.json").read_text(encoding="utf-8"))
    assert archive.is_file()
    assert report["status"] == "built"
    with zipfile.ZipFile(archive) as zf:
        assert zf.testzip() is None
        names = set(zf.namelist())
        assert "SIMS-Writer-Claude/CLAUDE_PROJECT_INSTRUCTIONS.md" in names
        assert "SIMS-Writer-Claude/USER_TEST_REHEARSAL.md" in names
        assert "SIMS-Writer-Claude/REAL_ARTICLE_UAT_RESULT_TEMPLATE.json" in names
        assert "SIMS-Writer-Claude/manifest.json" in names
