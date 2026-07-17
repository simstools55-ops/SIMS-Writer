from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ClaudeUATSessionError(ValueError):
    pass


REQUIRED_REQUEST_KEYS = ("article_id",)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in value.strip())
    return cleaned.strip("-") or "article"


class ClaudeUATSessionBuilder:
    """Build a traceable real-article UAT session without fabricating evidence."""

    def prepare(self, request_dir: Path, output_dir: Path, session_id: str | None = None) -> dict[str, Any]:
        request_dir = request_dir.resolve()
        output_dir = output_dir.resolve()
        if not request_dir.is_dir():
            raise ClaudeUATSessionError(f"request directory not found: {request_dir}")
        source_paths = sorted(path for path in request_dir.glob("*.json") if path.is_file())
        if not source_paths:
            raise ClaudeUATSessionError("no request JSON files found")

        resolved_session_id = session_id or datetime.now(timezone.utc).strftime("UAT-%Y%m%dT%H%M%SZ")
        session_root = output_dir / _safe_name(resolved_session_id)
        if session_root.exists():
            raise ClaudeUATSessionError(f"session already exists: {session_root}")
        requests_out = session_root / "requests"
        responses_out = session_root / "responses"
        evidence_out = session_root / "evidence"
        validation_out = session_root / "validation"
        for directory in (requests_out, responses_out, evidence_out, validation_out):
            directory.mkdir(parents=True, exist_ok=True)

        records: list[dict[str, Any]] = []
        article_ids: set[str] = set()
        for index, source in enumerate(source_paths, start=1):
            try:
                payload = json.loads(source.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ClaudeUATSessionError(f"invalid request JSON {source.name}: {exc}") from exc
            missing = [key for key in REQUIRED_REQUEST_KEYS if not str(payload.get(key, "")).strip()]
            if missing:
                raise ClaudeUATSessionError(f"request {source.name} missing: {', '.join(missing)}")
            article_id = str(payload["article_id"]).strip()
            if article_id in article_ids:
                raise ClaudeUATSessionError(f"duplicate article_id: {article_id}")
            article_ids.add(article_id)
            request_id = str(payload.get("request_id") or f"REQ-{resolved_session_id}-{index:03d}")
            target_name = f"{index:02d}-{_safe_name(article_id)}.json"
            target = requests_out / target_name
            normalized = dict(payload)
            normalized.setdefault("request_id", request_id)
            target.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            evidence_name = f"{index:02d}-{_safe_name(article_id)}-evidence.json"
            evidence_path = evidence_out / evidence_name
            evidence = {
                "evidence_version": "1.1",
                "evidence_id": f"{resolved_session_id}-{index:03d}",
                "session_id": resolved_session_id,
                "article_id": article_id,
                "request_id": request_id,
                "request_file": f"requests/{target_name}",
                "request_sha256": _sha256(target),
                "response_file": f"responses/{index:02d}-{_safe_name(article_id)}-claude-output.json",
                "response_sha256": "",
                "validation_file": f"validation/{index:02d}-{_safe_name(article_id)}-validation.json",
                "outcome": "pending",
                "scores": {
                    "japanese_quality": 0,
                    "factual_grounding": 0,
                    "source_preservation": 0,
                    "internal_links": 0,
                    "output_completeness": 0,
                    "beginner_usability": 0,
                },
                "blockers": [],
                "unresolved_items": [],
                "setup": {"operator_level": "developer", "completed": False, "notes": ""},
                "review_notes": "",
                "reviewed_at": "",
                "reviewer": "",
            }
            evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            records.append({
                "article_id": article_id,
                "request_id": request_id,
                "request_file": f"requests/{target_name}",
                "request_sha256": evidence["request_sha256"],
                "response_file": evidence["response_file"],
                "evidence_file": f"evidence/{evidence_name}",
                "status": "pending",
            })

        manifest = {
            "session_version": "1.1",
            "session_id": resolved_session_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "prepared",
            "counts": {"requests": len(records), "completed": 0, "pending": len(records)},
            "records": records,
        }
        manifest_path = session_root / "session-manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (session_root / "README.md").write_text(self._readme(resolved_session_id), encoding="utf-8")
        return {"session_root": str(session_root), "manifest": manifest}

    @staticmethod
    def _readme(session_id: str) -> str:
        return f"""# SIMS Writer Claude実記事UATセッション\n\n- Session ID: `{session_id}`\n- 状態: `prepared`\n\n## 手順\n\n1. `requests/`の依頼を1件ずつClaude Projectへ送信する。\n2. JSON応答を対応する`responses/`の予定ファイル名で保存する。\n3. Runtimeの`--validate-claude-output`で検証し、結果を`validation/`へ保存する。\n4. `evidence/`の対応ファイルを実測結果で更新する。\n5. 推測で点数や合格を記入しない。未解決事項は`blockers`へ残す。\n6. 全件後、`--evaluate-user-test-readiness`を実行する。\n\n`outcome`は確認前の`pending`から、実測後に`generated`または`manual_review_required`へ変更してください。\n"""
