import hashlib
import json
from pathlib import Path

from runtime.sims_writer_runtime.claude.evidence_ingest import ClaudeUATEvidenceIngestor
from runtime.sims_writer_runtime.claude.evidence_pack import ClaudeUATSessionBuilder


def _write_request(path: Path, article_id: str) -> None:
    path.write_text(json.dumps({'article_id': article_id, 'existing_content': '本文'}, ensure_ascii=False), encoding='utf-8')


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_pending_session_is_in_progress(tmp_path: Path) -> None:
    req = tmp_path / 'requests'; req.mkdir(); _write_request(req / 'a.json', 'A1')
    result = ClaudeUATSessionBuilder().prepare(req, tmp_path / 'sessions', 'UAT-1')
    report = ClaudeUATEvidenceIngestor().ingest(Path(result['session_root']))
    assert report['status'] == 'in_progress'
    assert report['counts']['pending'] == 1


def test_completed_evidence_is_verified(tmp_path: Path) -> None:
    req = tmp_path / 'requests'; req.mkdir(); _write_request(req / 'a.json', 'A1')
    root = Path(ClaudeUATSessionBuilder().prepare(req, tmp_path / 'sessions', 'UAT-2')['session_root'])
    evidence_path = next((root / 'evidence').glob('*.json'))
    evidence = json.loads(evidence_path.read_text())
    response = root / evidence['response_file']; response.write_text('{"status":"generated"}', encoding='utf-8')
    validation = root / evidence['validation_file']; validation.write_text('{"valid":true}', encoding='utf-8')
    evidence['outcome'] = 'generated'; evidence['response_sha256'] = _sha(response)
    evidence_path.write_text(json.dumps(evidence), encoding='utf-8')
    report = ClaudeUATEvidenceIngestor().ingest(root)
    assert report['status'] == 'complete'
    assert report['counts']['invalid'] == 0


def test_request_tampering_is_detected(tmp_path: Path) -> None:
    req = tmp_path / 'requests'; req.mkdir(); _write_request(req / 'a.json', 'A1')
    root = Path(ClaudeUATSessionBuilder().prepare(req, tmp_path / 'sessions', 'UAT-3')['session_root'])
    next((root / 'requests').glob('*.json')).write_text('{}', encoding='utf-8')
    report = ClaudeUATEvidenceIngestor().ingest(root)
    assert report['status'] == 'invalid'
    assert report['counts']['tamper_signals'] == 1


def test_completed_without_response_is_invalid(tmp_path: Path) -> None:
    req = tmp_path / 'requests'; req.mkdir(); _write_request(req / 'a.json', 'A1')
    root = Path(ClaudeUATSessionBuilder().prepare(req, tmp_path / 'sessions', 'UAT-4')['session_root'])
    evidence_path = next((root / 'evidence').glob('*.json'))
    evidence = json.loads(evidence_path.read_text()); evidence['outcome'] = 'generated'
    evidence_path.write_text(json.dumps(evidence), encoding='utf-8')
    report = ClaudeUATEvidenceIngestor().ingest(root)
    assert report['status'] == 'invalid'
    assert report['counts']['invalid'] == 1
