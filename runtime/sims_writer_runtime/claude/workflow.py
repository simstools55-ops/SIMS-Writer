from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evidence_ingest import ClaudeUATEvidenceIngestor
from .readiness import ClaudeUserTestReadinessEvaluator, write_readiness_report
from .setup_evidence import BeginnerSetupEvidenceError, BeginnerSetupEvidenceValidator


class ClaudeUATReadinessWorkflow:
    """Run evidence ingestion, beginner setup validation, and readiness evaluation."""

    def run(self, session_root: Path, output_dir: Path) -> dict[str, Any]:
        session_root = session_root.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        ingest = ClaudeUATEvidenceIngestor().ingest(session_root)
        setup_path = session_root / "beginner-setup-evidence.json"
        try:
            setup = BeginnerSetupEvidenceValidator().validate_file(setup_path).to_dict()
        except BeginnerSetupEvidenceError as exc:
            setup = {
                "valid": False,
                "completed": False,
                "operator_level": "",
                "passed_steps": 0,
                "total_steps": len(BeginnerSetupEvidenceValidator.required_steps),
                "blockers": [],
                "errors": [str(exc)],
            }

        readiness = ClaudeUserTestReadinessEvaluator().evaluate_directory(
            session_root / "evidence", beginner_setup_override=bool(setup["valid"] and setup["completed"])
        )
        workflow_ready = ingest["status"] == "complete" and setup["valid"] and setup["completed"] and readiness["ready"]
        report = {
            "workflow_version": "1.0",
            "status": "user_test_ready" if workflow_ready else "not_user_test_ready",
            "ready": workflow_ready,
            "session_id": ingest.get("session_id", ""),
            "ingest": ingest,
            "beginner_setup": setup,
            "readiness": readiness,
        }
        (output_dir / "claude-uat-readiness-workflow.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        write_readiness_report(readiness, output_dir)
        lines = [
            "# Claude UAT 最終運用判定",
            "",
            f"- 判定: **{report['status']}**",
            f"- 証拠取り込み: `{ingest['status']}`",
            f"- 初心者セットアップ: `{'passed' if setup['valid'] and setup['completed'] else 'not_passed'}`",
            f"- 品質Readiness: `{readiness['status']}`",
        ]
        (output_dir / "claude-uat-readiness-workflow.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return report
