from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .acceptance import ClaudeOutputAcceptanceError, ClaudeOutputValidator


class ClaudeUATResultRegistrationError(ValueError):
    pass


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ClaudeUATResultRegistrar:
    """Validate and register Claude UAT responses without inventing human scores."""

    def __init__(self, repo_root: Path):
        self.validator = ClaudeOutputValidator(repo_root)

    def register(self, session_root: Path, result_dir: Path) -> dict[str, Any]:
        session_root = session_root.resolve()
        result_dir = result_dir.resolve()
        manifest_path = session_root / "session-manifest.json"
        if not manifest_path.is_file():
            raise ClaudeUATResultRegistrationError("session-manifest.json not found")
        if not result_dir.is_dir():
            raise ClaudeUATResultRegistrationError(f"result directory not found: {result_dir}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClaudeUATResultRegistrationError(f"invalid session manifest: {exc}") from exc

        records = manifest.get("records")
        if not isinstance(records, list) or not records:
            raise ClaudeUATResultRegistrationError("session manifest has no records")

        output_records: list[dict[str, Any]] = []
        imported = rejected = missing = skipped = 0
        for record in records:
            article_id = str(record.get("article_id", ""))
            request_path = session_root / str(record.get("request_file", ""))
            response_target = session_root / str(record.get("response_file", ""))
            evidence_path = session_root / str(record.get("evidence_file", ""))
            validation_rel = str(record.get("response_file", "")).replace(
                "responses/", "validation/"
            ).replace("-claude-output.json", "-validation.json")
            validation_target = session_root / validation_rel
            source = self._find_source(result_dir, response_target.name, article_id)
            errors: list[str] = []

            if str(record.get("status", "pending")) not in {"pending", "prepared"}:
                skipped += 1
                output_records.append({
                    "article_id": article_id,
                    "status": "skipped",
                    "source_file": "",
                    "errors": ["record is not pending; existing result was not overwritten"],
                })
                continue
            if source is None:
                missing += 1
                output_records.append({
                    "article_id": article_id,
                    "status": "missing",
                    "source_file": "",
                    "errors": [f"expected response not found: {response_target.name}"],
                })
                continue
            if not request_path.is_file():
                errors.append("request file missing")
            if not evidence_path.is_file():
                errors.append("evidence file missing")
            if errors:
                rejected += 1
                output_records.append({
                    "article_id": article_id,
                    "status": "rejected",
                    "source_file": str(source),
                    "errors": errors,
                })
                continue

            try:
                report = self.validator.validate_file(source, request_path)
            except (ClaudeOutputAcceptanceError, json.JSONDecodeError) as exc:
                rejected += 1
                output_records.append({
                    "article_id": article_id,
                    "status": "rejected",
                    "source_file": str(source),
                    "errors": [str(exc)],
                })
                continue
            if not report.valid or report.normalized_output is None:
                rejected += 1
                output_records.append({
                    "article_id": article_id,
                    "status": "rejected",
                    "source_file": str(source),
                    "errors": report.errors,
                    "warnings": report.warnings,
                })
                continue

            response_target.parent.mkdir(parents=True, exist_ok=True)
            validation_target.parent.mkdir(parents=True, exist_ok=True)
            response_target.write_text(
                json.dumps(report.normalized_output, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            validation_target.write_text(
                json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            try:
                evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                rejected += 1
                response_target.unlink(missing_ok=True)
                validation_target.unlink(missing_ok=True)
                output_records.append({
                    "article_id": article_id,
                    "status": "rejected",
                    "source_file": str(source),
                    "errors": [f"invalid evidence file: {exc}"],
                })
                continue
            evidence["response_file"] = str(record.get("response_file", ""))
            evidence["response_sha256"] = _sha256(response_target)
            evidence["validation_file"] = validation_rel
            evidence["outcome"] = report.normalized_output["status"]
            evidence["unresolved_items"] = list(report.normalized_output.get("unresolved_items", []))
            evidence["reviewed_at"] = ""
            evidence["reviewer"] = ""
            evidence_path.write_text(
                json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            record["status"] = "awaiting_human_review"
            imported += 1
            output_records.append({
                "article_id": article_id,
                "status": "registered",
                "outcome": report.normalized_output["status"],
                "source_file": str(source),
                "response_file": str(record.get("response_file", "")),
                "validation_file": validation_rel,
                "warnings": report.warnings,
                "errors": [],
            })

        total = len(records)
        manifest["status"] = "awaiting_human_review" if imported == total else "registration_incomplete"
        manifest["counts"] = {
            "requests": total,
            "registered": imported,
            "pending": missing,
            "rejected": rejected,
            "skipped": skipped,
        }
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        status = "complete" if imported == total else ("failed" if imported == 0 and rejected else "partial")
        result = {
            "registration_version": "1.0",
            "session_id": str(manifest.get("session_id", "")),
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "counts": {
                "records": total,
                "registered": imported,
                "rejected": rejected,
                "missing": missing,
                "skipped": skipped,
            },
            "human_review_required": imported > 0,
            "records": output_records,
        }
        (session_root / "uat-result-registration-report.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return result

    @staticmethod
    def _find_source(result_dir: Path, expected_name: str, article_id: str) -> Path | None:
        candidates = [
            result_dir / expected_name,
            result_dir / "responses" / expected_name,
            result_dir / f"{article_id}.json",
            result_dir / f"{article_id}-claude-output.json",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        return None
