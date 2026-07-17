import json
from pathlib import Path

import pytest

from runtime.sims_writer_runtime.claude.evidence_pack import ClaudeUATSessionBuilder
from runtime.sims_writer_runtime.claude.operator_pack import ClaudeUATOperatorPackBuilder, ClaudeUATOperatorPackError


def _request(path: Path, article_id: str) -> None:
    path.write_text(json.dumps({"article_id": article_id, "title": f"記事 {article_id}"}, ensure_ascii=False), encoding="utf-8")


def test_builds_guided_operator_pack(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    _request(requests / "a.json", "A000001")
    _request(requests / "b.json", "A000002")
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-001")
    result = ClaudeUATOperatorPackBuilder().build(Path(session["session_root"]), tmp_path / "out")
    root = Path(result["pack_root"])
    assert result["manifest"]["article_count"] == 2
    assert (root / "README.md").is_file()
    assert (root / "SCORING_GUIDE.md").is_file()
    assert (root / "PROGRESS_CHECKLIST.md").is_file()
    prompt = (root / "prompts" / "01-A000001-prompt.md").read_text(encoding="utf-8")
    assert '"article_id": "A000001"' in prompt
    assert "responses/01-A000001-claude-output.json" in prompt


def test_pack_does_not_change_session_evidence(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    _request(requests / "a.json", "A000001")
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-002")
    session_root = Path(session["session_root"])
    evidence = next((session_root / "evidence").glob("*.json"))
    before = evidence.read_bytes()
    ClaudeUATOperatorPackBuilder().build(session_root, tmp_path / "out")
    assert evidence.read_bytes() == before


def test_rejects_missing_request_file(tmp_path: Path) -> None:
    root = tmp_path / "session"
    root.mkdir()
    (root / "session-manifest.json").write_text(json.dumps({
        "session_id": "UAT-X", "records": [{"article_id": "A1", "request_file": "requests/missing.json"}]
    }), encoding="utf-8")
    with pytest.raises(ClaudeUATOperatorPackError, match="request file missing"):
        ClaudeUATOperatorPackBuilder().build(root, tmp_path / "out")
