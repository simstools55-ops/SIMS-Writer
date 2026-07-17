from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ClaudeUATEvidenceIngestError(ValueError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(65536), b''):
            digest.update(chunk)
    return digest.hexdigest()


class ClaudeUATEvidenceIngestor:
    """Verify and consolidate a prepared UAT session without inventing evidence."""

    def ingest(self, session_root: Path) -> dict[str, Any]:
        session_root = session_root.resolve()
        manifest_path = session_root / 'session-manifest.json'
        if not manifest_path.is_file():
            raise ClaudeUATEvidenceIngestError('session-manifest.json not found')
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClaudeUATEvidenceIngestError(f'invalid session manifest: {exc}') from exc

        records_out: list[dict[str, Any]] = []
        completed = 0
        pending = 0
        invalid = 0
        tampered = 0
        for record in manifest.get('records', []):
            errors: list[str] = []
            request_path = session_root / record['request_file']
            evidence_path = session_root / record['evidence_file']
            if not request_path.is_file():
                errors.append('request file missing')
            elif _sha256(request_path) != record.get('request_sha256'):
                errors.append('request SHA-256 mismatch')
                tampered += 1
            try:
                evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                evidence = {}
                errors.append(f'invalid evidence file: {exc}')

            if evidence.get('article_id') != record.get('article_id'):
                errors.append('article_id mismatch')
            if evidence.get('request_id') != record.get('request_id'):
                errors.append('request_id mismatch')
            if evidence.get('request_sha256') != record.get('request_sha256'):
                errors.append('evidence request SHA-256 mismatch')

            outcome = str(evidence.get('outcome', '')).strip()
            response_rel = str(evidence.get('response_file', record.get('response_file', '')))
            response_path = session_root / response_rel if response_rel else None
            if outcome == 'pending':
                pending += 1
            elif outcome in {'generated', 'manual_review_required'}:
                if response_path is None or not response_path.is_file():
                    errors.append('completed evidence response file missing')
                else:
                    actual_response_sha = _sha256(response_path)
                    if evidence.get('response_sha256') != actual_response_sha:
                        errors.append('response SHA-256 missing or mismatch')
                        tampered += 1
                validation_rel = str(evidence.get('validation_file', ''))
                validation_path = session_root / validation_rel if validation_rel else None
                if validation_path is None or not validation_path.is_file():
                    errors.append('validation file missing')
                completed += 1
            else:
                errors.append(f'invalid outcome: {outcome or "empty"}')

            if errors:
                invalid += 1
            records_out.append({
                'article_id': record.get('article_id', ''),
                'evidence_file': record.get('evidence_file', ''),
                'outcome': outcome,
                'valid': not errors,
                'errors': errors,
            })

        status = 'complete' if records_out and invalid == 0 and pending == 0 else ('invalid' if invalid else 'in_progress')
        report = {
            'ingest_version': '1.0',
            'session_id': manifest.get('session_id', ''),
            'evaluated_at': datetime.now(timezone.utc).isoformat(),
            'status': status,
            'counts': {
                'records': len(records_out),
                'completed': completed,
                'pending': pending,
                'invalid': invalid,
                'tamper_signals': tampered,
            },
            'records': records_out,
        }
        report_path = session_root / 'uat-evidence-ingest-report.json'
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        manifest['status'] = status
        manifest['counts'] = {
            'requests': len(records_out),
            'completed': completed,
            'pending': pending,
            'invalid': invalid,
        }
        for source, result in zip(manifest.get('records', []), records_out):
            source['status'] = 'invalid' if not result['valid'] else result['outcome']
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return report
