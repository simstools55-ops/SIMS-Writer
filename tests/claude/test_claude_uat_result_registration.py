from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runtime.sims_writer_runtime.claude.evidence_pack import ClaudeUATSessionBuilder
from runtime.sims_writer_runtime.claude.result_registration import ClaudeUATResultRegistrar


def _request(path: Path, article_id: str, with_content: bool = True) -> None:
    payload = {"article_id": article_id, "title": f"記事 {article_id}"}
    if with_content:
        payload["existing_content"] = "元記事本文です。"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _valid_output(status: str = "generated") -> dict:
    generated = status == "generated"
    return {
        "status": status,
        "seo_title": "改善SEOタイトル" if generated else None,
        "meta_description": "改善後の説明文です。" if generated else None,
        "h1": "改善H1" if generated else None,
        "article_content": "改善された記事本文です。" if generated else None,
        "change_summary": [],
        "faq": [],
        "internal_link_recommendations": [],
        "separate_article_candidates": [],
        "unresolved_items": [] if generated else ["元記事本文の確認が必要"],
    }


def test_bulk_registers_and_validates_responses(tmp_path: Path) -> None:
    requests = tmp_path / "requests"; requests.mkdir()
    _request(requests / "a.json", "A000001")
    _request(requests / "b.json", "A000002")
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-REG-1")
    root = Path(session["session_root"])
    results = tmp_path / "results"; results.mkdir()
    records = session["manifest"]["records"]
    for record in records:
        (results / Path(record["response_file"]).name).write_text(
            json.dumps(_valid_output(), ensure_ascii=False), encoding="utf-8"
        )
    report = ClaudeUATResultRegistrar(Path(__file__).resolve().parents[2]).register(root, results)
    assert report["status"] == "complete"
    assert report["counts"]["registered"] == 2
    evidence = json.loads(next((root / "evidence").glob("*.json")).read_text(encoding="utf-8"))
    response = root / evidence["response_file"]
    assert evidence["outcome"] == "generated"
    assert evidence["response_sha256"] == hashlib.sha256(response.read_bytes()).hexdigest()
    assert all(value == 0 for value in evidence["scores"].values())
    assert evidence["reviewer"] == ""


def test_registers_manual_review_without_inventing_scores(tmp_path: Path) -> None:
    requests = tmp_path / "requests"; requests.mkdir()
    _request(requests / "a.json", "A000001", with_content=False)
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-REG-2")
    root = Path(session["session_root"])
    results = tmp_path / "results"; results.mkdir()
    record = session["manifest"]["records"][0]
    (results / Path(record["response_file"]).name).write_text(
        json.dumps(_valid_output("manual_review_required"), ensure_ascii=False), encoding="utf-8"
    )
    report = ClaudeUATResultRegistrar(Path(__file__).resolve().parents[2]).register(root, results)
    evidence = json.loads(next((root / "evidence").glob("*.json")).read_text(encoding="utf-8"))
    assert report["status"] == "complete"
    assert evidence["outcome"] == "manual_review_required"
    assert evidence["unresolved_items"] == ["元記事本文の確認が必要"]
    assert all(value == 0 for value in evidence["scores"].values())


def test_invalid_response_is_rejected_without_session_response(tmp_path: Path) -> None:
    requests = tmp_path / "requests"; requests.mkdir()
    _request(requests / "a.json", "A000001")
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-REG-3")
    root = Path(session["session_root"])
    results = tmp_path / "results"; results.mkdir()
    record = session["manifest"]["records"][0]
    (results / Path(record["response_file"]).name).write_text('{"status":"generated"}', encoding="utf-8")
    report = ClaudeUATResultRegistrar(Path(__file__).resolve().parents[2]).register(root, results)
    assert report["status"] == "failed"
    assert report["counts"]["rejected"] == 1
    assert not (root / record["response_file"]).exists()
    evidence = json.loads(next((root / "evidence").glob("*.json")).read_text(encoding="utf-8"))
    assert evidence["outcome"] == "pending"


def test_missing_response_keeps_partial_session(tmp_path: Path) -> None:
    requests = tmp_path / "requests"; requests.mkdir()
    _request(requests / "a.json", "A000001")
    _request(requests / "b.json", "A000002")
    session = ClaudeUATSessionBuilder().prepare(requests, tmp_path / "sessions", "UAT-REG-4")
    root = Path(session["session_root"])
    results = tmp_path / "results"; results.mkdir()
    record = session["manifest"]["records"][0]
    (results / Path(record["response_file"]).name).write_text(
        json.dumps(_valid_output(), ensure_ascii=False), encoding="utf-8"
    )
    report = ClaudeUATResultRegistrar(Path(__file__).resolve().parents[2]).register(root, results)
    assert report["status"] == "partial"
    assert report["counts"]["registered"] == 1
    assert report["counts"]["missing"] == 1
