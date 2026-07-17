from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ExecutionHistoryManager:
    """Archive the previous artifact set and compare it with the new execution."""

    TRACKED_FILES = (
        "runtime-result.json",
        "publication-package.json",
        "article.md",
        "improvement-report.md",
        "execution-manifest.json",
        "artifact-validation.json",
        "publication-checklist.md",
        "publication-approval.json",
        "approval-history.json",
    )

    def capture_previous(self, output_dir: Path) -> dict[str, Any] | None:
        output_dir = Path(output_dir)
        runtime_path = output_dir / "runtime-result.json"
        if not runtime_path.is_file():
            return None
        try:
            runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        execution_id = str(runtime.get("execution_id") or "UNKNOWN")
        archive_dir = output_dir / ".history" / execution_id
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived: list[str] = []
        for name in self.TRACKED_FILES:
            source = output_dir / name
            if source.is_file():
                shutil.copy2(source, archive_dir / name)
                archived.append(name)
        return {
            "execution_id": execution_id,
            "request_id": runtime.get("request_id"),
            "status": runtime.get("status"),
            "archive_dir": str(Path(".history") / execution_id),
            "archived_files": archived,
            "snapshot": self._snapshot(output_dir),
        }

    def build_diff(self, previous: dict[str, Any] | None, output_dir: Path, current: dict[str, Any]) -> dict[str, Any]:
        current_snapshot = self._snapshot(output_dir)
        previous_snapshot = (previous or {}).get("snapshot", {})
        changed_files = sorted(
            name for name in set(previous_snapshot) | set(current_snapshot)
            if previous_snapshot.get(name, {}).get("sha256") != current_snapshot.get(name, {}).get("sha256")
        )
        package_changes = self._package_changes(previous, output_dir)
        return {
            "diff_version": "1.0.0",
            "baseline": "previous_execution" if previous else "initial_execution",
            "previous_execution_id": (previous or {}).get("execution_id"),
            "current_execution_id": current.get("execution_id"),
            "request_id": current.get("request_id"),
            "changed": bool(previous and (changed_files or package_changes)),
            "changed_files": changed_files if previous else [],
            "publication_changes": package_changes,
            "current_checksums": current_snapshot,
        }

    def update_history(self, output_dir: Path, previous: dict[str, Any] | None, current: dict[str, Any], diff: dict[str, Any]) -> dict[str, Any]:
        path = Path(output_dir) / "execution-history.json"
        entries: list[dict[str, Any]] = []
        if path.is_file():
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                entries = list(payload.get("executions") or [])
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
                entries = []
        if previous:
            previous_entry = {
                "execution_id": previous.get("execution_id"),
                "request_id": previous.get("request_id"),
                "status": previous.get("status"),
                "archive_dir": previous.get("archive_dir"),
                "superseded": True,
            }
            replaced = False
            for index, entry in enumerate(entries):
                if entry.get("execution_id") == previous.get("execution_id"):
                    entries[index] = previous_entry
                    replaced = True
                    break
            if not replaced:
                entries.append(previous_entry)
        entries = [e for e in entries if e.get("execution_id") != current.get("execution_id")]
        entries.append({
            "execution_id": current.get("execution_id"),
            "request_id": current.get("request_id"),
            "status": current.get("status"),
            "archive_dir": None,
            "superseded": False,
            "changed_from_previous": diff.get("changed", False),
        })
        return {
            "history_version": "1.0.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "request_id": current.get("request_id"),
            "execution_count": len(entries),
            "latest_execution_id": current.get("execution_id"),
            "executions": entries,
        }

    @staticmethod
    def _snapshot(output_dir: Path) -> dict[str, dict[str, Any]]:
        snapshot: dict[str, dict[str, Any]] = {}
        for name in ExecutionHistoryManager.TRACKED_FILES:
            path = Path(output_dir) / name
            if path.is_file():
                raw = path.read_bytes()
                snapshot[name] = {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        return snapshot

    @staticmethod
    def _package_changes(previous: dict[str, Any] | None, output_dir: Path) -> list[dict[str, Any]]:
        if not previous:
            return []
        previous_package = Path(output_dir) / str(previous.get("archive_dir")) / "publication-package.json"
        current_package = Path(output_dir) / "publication-package.json"
        if not previous_package.is_file() or not current_package.is_file():
            return []
        try:
            before = json.loads(previous_package.read_text(encoding="utf-8"))
            after = json.loads(current_package.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return []
        changes = []
        for field in ("publish_decision", "seo_title", "meta_description", "h1", "article_content"):
            if before.get(field) != after.get(field):
                changes.append({"field": field, "before": before.get(field), "after": after.get(field)})
        return changes
