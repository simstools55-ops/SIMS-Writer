from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .history import ExecutionHistoryManager
from .validator import PublicationArtifactValidator


class ArtifactRollbackError(RuntimeError):
    """Raised when a requested artifact rollback cannot be completed safely."""


class ArtifactRollbackManager:
    """Restore a previously archived publication artifact set."""

    def rollback(self, output_dir: Path, target_execution_id: str) -> dict[str, Any]:
        output_dir = Path(output_dir)
        target_execution_id = str(target_execution_id).strip()
        if not target_execution_id:
            raise ArtifactRollbackError("target_execution_id is required")

        history_path = output_dir / "execution-history.json"
        if not history_path.is_file():
            raise ArtifactRollbackError("execution-history.json was not found")
        history = self._read_json(history_path, "execution history")

        target_entry = next(
            (entry for entry in history.get("executions", []) if entry.get("execution_id") == target_execution_id),
            None,
        )
        if target_entry is None:
            raise ArtifactRollbackError(f"execution is not registered in history: {target_execution_id}")

        archive_dir = output_dir / ".history" / target_execution_id
        if not archive_dir.is_dir():
            raise ArtifactRollbackError(f"archive directory was not found: {archive_dir}")

        missing = [
            name for name in ExecutionHistoryManager.TRACKED_FILES
            if not (archive_dir / name).is_file()
        ]
        if missing:
            raise ArtifactRollbackError("archive is incomplete: " + ", ".join(missing))

        current = self._current_execution(output_dir)
        history_manager = ExecutionHistoryManager()
        archived_current = history_manager.capture_previous(output_dir)

        restored: list[str] = []
        for name in ExecutionHistoryManager.TRACKED_FILES:
            shutil.copy2(archive_dir / name, output_dir / name)
            restored.append(name)

        restored_runtime = self._read_json(output_dir / "runtime-result.json", "restored runtime result")
        if restored_runtime.get("execution_id") != target_execution_id:
            raise ArtifactRollbackError("restored runtime execution_id does not match target")

        validation = PublicationArtifactValidator().validate(output_dir)
        (output_dir / "artifact-validation.json").write_text(
            json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        rolled_back_from = (current or {}).get("execution_id")
        updated_entries = []
        for entry in history.get("executions", []):
            item = dict(entry)
            item["superseded"] = item.get("execution_id") != target_execution_id
            if item.get("execution_id") == target_execution_id:
                item["archive_dir"] = str(Path(".history") / target_execution_id)
                item["restored"] = True
            updated_entries.append(item)

        updated_history = {
            "history_version": "1.1.0",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "request_id": restored_runtime.get("request_id"),
            "execution_count": len(updated_entries),
            "latest_execution_id": target_execution_id,
            "last_operation": "rollback",
            "rolled_back_from_execution_id": rolled_back_from,
            "executions": updated_entries,
        }
        history_path.write_text(json.dumps(updated_history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        manifest = {
            "rollback_version": "1.0.0",
            "rolled_back_at": datetime.now(timezone.utc).isoformat(),
            "target_execution_id": target_execution_id,
            "rolled_back_from_execution_id": rolled_back_from,
            "request_id": restored_runtime.get("request_id"),
            "restored_files": restored,
            "archived_current_execution": archived_current,
            "artifact_status": validation.get("artifact_status"),
            "release_ready": validation.get("release_ready"),
            "checksums": self._checksums(output_dir, restored),
        }
        (output_dir / "rollback-manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return manifest

    @staticmethod
    def _read_json(path: Path, label: str) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ArtifactRollbackError(f"invalid {label}: {path}") from exc
        if not isinstance(payload, dict):
            raise ArtifactRollbackError(f"invalid {label}: object expected")
        return payload

    def _current_execution(self, output_dir: Path) -> dict[str, Any] | None:
        path = output_dir / "runtime-result.json"
        if not path.is_file():
            return None
        return self._read_json(path, "current runtime result")

    @staticmethod
    def _checksums(output_dir: Path, names: list[str]) -> dict[str, str]:
        return {
            name: hashlib.sha256((output_dir / name).read_bytes()).hexdigest()
            for name in names
        }
