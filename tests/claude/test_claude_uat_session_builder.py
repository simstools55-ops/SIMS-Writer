from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from runtime.sims_writer_runtime.claude.evidence_pack import ClaudeUATSessionBuilder, ClaudeUATSessionError


def write_request(path: Path, article_id: str, request_id: str | None = None) -> None:
    payload = {"article_id": article_id, "existing_content": "本文です。"}
    if request_id:
        payload["request_id"] = request_id
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_prepares_traceable_session_without_fabricated_results(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    write_request(requests / "a.json", "A000001", "REQ-1")
    write_request(requests / "b.json", "A000002")
    result = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "out", "UAT-TEST-001")
    root = Path(result["session_root"])
    manifest = json.loads((root / "session-manifest.json").read_text(encoding="utf-8"))
    assert manifest["counts"] == {"requests": 2, "completed": 0, "pending": 2}
    assert len(list((root / "evidence").glob("*.json"))) == 2
    evidence = json.loads(next((root / "evidence").glob("*.json")).read_text(encoding="utf-8"))
    assert evidence["outcome"] == "pending"
    assert all(value == 0 for value in evidence["scores"].values())
    request_path = root / evidence["request_file"]
    assert evidence["request_sha256"] == hashlib.sha256(request_path.read_bytes()).hexdigest()


def test_rejects_duplicate_articles(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    write_request(requests / "a.json", "A000001")
    write_request(requests / "b.json", "A000001")
    with pytest.raises(ClaudeUATSessionError, match="duplicate article_id"):
        ClaudeUATSessionBuilder().prepare(requests, tmp_path / "out", "UAT-DUP")


def test_rejects_invalid_or_missing_requests(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    (requests / "bad.json").write_text("{}", encoding="utf-8")
    with pytest.raises(ClaudeUATSessionError, match="missing"):
        ClaudeUATSessionBuilder().prepare(requests, tmp_path / "out")


def test_rejects_existing_session(tmp_path: Path) -> None:
    requests = tmp_path / "requests"
    requests.mkdir()
    write_request(requests / "a.json", "A1")
    builder = ClaudeUATSessionBuilder()
    builder.prepare(requests, tmp_path / "out", "SAME")
    with pytest.raises(ClaudeUATSessionError, match="already exists"):
        builder.prepare(requests, tmp_path / "out", "SAME")
