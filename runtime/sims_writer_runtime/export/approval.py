from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .history import ExecutionHistoryManager


class PublicationApprovalError(RuntimeError):
    """Raised when a publication approval transition is invalid or unsafe."""


class PublicationApprovalManager:
    """Manage review, rejection, approval, and final publication snapshots."""

    APPROVAL_FILE = "publication-approval.json"
    HISTORY_FILE = "approval-history.json"
    FINALIZATION_FILE = "finalization-manifest.json"
    FINALIZED_FILES = ExecutionHistoryManager.TRACKED_FILES

    def initialize(self, output_dir: Path, execution_id: str, request_id: str | None) -> dict[str, Any]:
        output_dir = Path(output_dir)
        current = self._read_optional(output_dir / self.APPROVAL_FILE)
        if current and current.get("execution_id") == execution_id:
            return current
        payload = {
            "approval_version": "1.0.0",
            "execution_id": execution_id,
            "request_id": request_id,
            "status": "pending_review",
            "reviewer": None,
            "reason": None,
            "updated_at": self._now(),
            "finalized_at": None,
        }
        self._write_json(output_dir / self.APPROVAL_FILE, payload)
        self._append_history(output_dir, "pending_review", payload, note="artifact_set_generated")
        return payload

    def approve(self, output_dir: Path, reviewer: str, note: str | None = None) -> dict[str, Any]:
        output_dir = Path(output_dir)
        reviewer = self._required(reviewer, "reviewer")
        runtime, validation, approval = self._load_current(output_dir)
        if validation.get("artifact_status") != "valid" or not validation.get("release_ready"):
            raise PublicationApprovalError("only valid release-ready artifacts can be approved")
        if approval.get("execution_id") != runtime.get("execution_id"):
            raise PublicationApprovalError("approval execution_id does not match current artifacts")
        if approval.get("status") == "finalized":
            raise PublicationApprovalError("finalized artifacts cannot be approved again")
        approval.update({
            "status": "approved",
            "reviewer": reviewer,
            "reason": note,
            "updated_at": self._now(),
            "finalized_at": None,
        })
        self._write_json(output_dir / self.APPROVAL_FILE, approval)
        self._append_history(output_dir, "approved", approval, note=note)
        return approval

    def reject(self, output_dir: Path, reviewer: str, reason: str) -> dict[str, Any]:
        output_dir = Path(output_dir)
        reviewer = self._required(reviewer, "reviewer")
        reason = self._required(reason, "reason")
        runtime, _, approval = self._load_current(output_dir)
        if approval.get("execution_id") != runtime.get("execution_id"):
            raise PublicationApprovalError("approval execution_id does not match current artifacts")
        if approval.get("status") == "finalized":
            raise PublicationApprovalError("finalized artifacts cannot be rejected")
        approval.update({
            "status": "rejected",
            "reviewer": reviewer,
            "reason": reason,
            "updated_at": self._now(),
            "finalized_at": None,
        })
        self._write_json(output_dir / self.APPROVAL_FILE, approval)
        self._append_history(output_dir, "rejected", approval, note=reason)
        return approval

    def finalize(self, output_dir: Path, reviewer: str | None = None) -> dict[str, Any]:
        output_dir = Path(output_dir)
        runtime, validation, approval = self._load_current(output_dir)
        if approval.get("status") != "approved":
            raise PublicationApprovalError("artifacts must be approved before finalization")
        if reviewer and reviewer != approval.get("reviewer"):
            raise PublicationApprovalError("finalizing reviewer does not match approving reviewer")
        if validation.get("artifact_status") != "valid" or not validation.get("release_ready"):
            raise PublicationApprovalError("artifacts are no longer release-ready")
        execution_id = str(runtime.get("execution_id") or "").strip()
        if approval.get("execution_id") != execution_id:
            raise PublicationApprovalError("approval execution_id does not match current artifacts")

        release_dir = output_dir / "release" / execution_id
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        for name in self.FINALIZED_FILES:
            source = output_dir / name
            if not source.is_file():
                raise PublicationApprovalError(f"required finalization artifact is missing: {name}")
            shutil.copy2(source, release_dir / name)
            copied.append(name)

        finalized_at = self._now()
        approval.update({"status": "finalized", "updated_at": finalized_at, "finalized_at": finalized_at})
        self._write_json(output_dir / self.APPROVAL_FILE, approval)
        self._write_json(release_dir / self.APPROVAL_FILE, approval)
        checksums = self._checksums(release_dir, copied)
        manifest = {
            "finalization_version": "1.0.0",
            "execution_id": execution_id,
            "request_id": runtime.get("request_id"),
            "status": "finalized",
            "reviewer": approval.get("reviewer"),
            "finalized_at": finalized_at,
            "release_dir": str(Path("release") / execution_id),
            "files": copied,
            "checksums": checksums,
            "release_ready": True,
        }
        self._write_json(output_dir / self.FINALIZATION_FILE, manifest)
        self._write_json(release_dir / self.FINALIZATION_FILE, manifest)
        self._append_history(output_dir, "finalized", approval, note="immutable_release_snapshot_created")
        return manifest

    def _load_current(self, output_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        runtime = self._read_json(output_dir / "runtime-result.json", "runtime result")
        validation = self._read_json(output_dir / "artifact-validation.json", "artifact validation")
        approval_path = output_dir / self.APPROVAL_FILE
        if not approval_path.is_file():
            self.initialize(output_dir, str(runtime.get("execution_id") or ""), runtime.get("request_id"))
        approval = self._read_json(approval_path, "publication approval")
        return runtime, validation, approval

    def _append_history(self, output_dir: Path, action: str, approval: dict[str, Any], note: str | None) -> None:
        path = output_dir / self.HISTORY_FILE
        payload = self._read_optional(path) or {"approval_history_version": "1.0.0", "events": []}
        events = list(payload.get("events") or [])
        events.append({
            "sequence": len(events) + 1,
            "action": action,
            "execution_id": approval.get("execution_id"),
            "request_id": approval.get("request_id"),
            "reviewer": approval.get("reviewer"),
            "note": note,
            "occurred_at": self._now(),
        })
        payload.update({
            "updated_at": self._now(),
            "latest_execution_id": approval.get("execution_id"),
            "event_count": len(events),
            "events": events,
        })
        self._write_json(path, payload)

    @staticmethod
    def _required(value: str | None, label: str) -> str:
        text = str(value or "").strip()
        if not text:
            raise PublicationApprovalError(f"{label} is required")
        return text

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _write_json(path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def _read_json(cls, path: Path, label: str) -> dict[str, Any]:
        payload = cls._read_optional(path)
        if payload is None:
            raise PublicationApprovalError(f"{label} was not found or is invalid: {path}")
        return payload

    @staticmethod
    def _read_optional(path: Path) -> dict[str, Any] | None:
        if not path.is_file():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    @staticmethod
    def _checksums(directory: Path, names: list[str]) -> dict[str, str]:
        return {name: hashlib.sha256((directory / name).read_bytes()).hexdigest() for name in names}
