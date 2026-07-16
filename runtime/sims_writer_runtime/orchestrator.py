from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any
from .models import STAGES, StageRecord, RuntimeResult
from .asset_loader import build_manifest
from .adapters.input_adapters import normalize_generic, normalize_sbm
from .adapters.manual_model import ManualModelAdapter

class RuntimeOrchestrator:
    def __init__(self, repo_root: Path, adapter: ManualModelAdapter | None = None):
        self.repo_root = repo_root
        self.adapter = adapter or ManualModelAdapter()

    def execute(self, raw: dict[str, Any], input_type: str = "generic") -> RuntimeResult:
        execution_id = f"EXE-{uuid4().hex[:12].upper()}"
        records = [StageRecord(name=s) for s in STAGES]
        artifacts: dict[str, Any] = {"raw_request": raw}
        manifest = build_manifest(self.repo_root)
        manifest["execution_id"] = execution_id
        manifest["locked_at"] = datetime.now(timezone.utc).isoformat()
        try:
            self._pass(records, "intake")
            request = normalize_sbm(raw) if input_type == "sbm" else normalize_generic(raw)
            artifacts["normalized_request"] = request
            self._pass(records, "normalization")

            source_status = "unavailable" if request.get("target_url") else "not_applicable"
            artifacts["source_snapshot"] = {"status": source_status, "target_url": request.get("target_url")}
            self._warn(records, "source_acquisition", "Alpha runtime does not fetch external content")

            artifacts["knowledge_assembly"] = {"coverage": "partial", "selected": [], "note": "registry connection verified"}
            self._warn(records, "knowledge_assembly", "Knowledge selection execution is scaffolded")

            plan = {
                "plan_id": f"PLN-{execution_id[4:]}",
                "primary_intent": request["main_query"],
                "main_answer": None,
                "status": "manual_review_required",
            }
            artifacts["content_plan"] = plan
            self._warn(records, "content_planning", "Main answer requires production adapter")

            action = "manual_review" if source_status == "unavailable" else "revise"
            artifacts["decision_action_plan"] = {"action": action, "components": [], "reason": "Alpha deterministic decision"}
            self._pass(records, "decision_evaluation")

            artifacts["pattern_selection"] = {"selected_patterns": [], "blocked_by_action": action == "manual_review"}
            self._pass(records, "pattern_selection")

            draft = self.adapter.produce(request, plan)
            artifacts["content_draft"] = draft
            self._manual(records, "content_production", "Production adapter not installed")

            artifacts["quality_report"] = {
                "publish_recommendation": "manual_review_required",
                "blockers": ["article_content_missing"],
                "framework_version": "1.0.0",
            }
            self._manual(records, "quality_validation", "Publication blocker remains")
            self._skip(records, "refinement", "No production draft to refine")

            artifacts["publication_package"] = {
                "publish_decision": "manual_review_required",
                "article_content": None,
                "quality_summary": artifacts["quality_report"],
                "runtime_notice": "Runtime connectivity verified; article generation is intentionally not implemented in this alpha.",
            }
            self._manual(records, "publication_packaging", "Package is diagnostic, not publish ready")
            status = "manual_review_required"
        except Exception as exc:
            current = next((r for r in records if r.status == "pending"), records[-1])
            current.status = "failed"
            current.error = {"category": "runtime", "message": str(exc), "retryable": False}
            request = artifacts.get("normalized_request", {"request_id":"UNKNOWN"})
            status = "failed"
        return RuntimeResult(execution_id, request.get("request_id", "UNKNOWN"), status, records, manifest, artifacts)

    @staticmethod
    def _record(records, name): return next(r for r in records if r.name == name)
    def _pass(self, records, name): self._record(records,name).status = "passed"
    def _warn(self, records, name, msg):
        r=self._record(records,name); r.status="passed_with_warning"; r.warnings.append(msg)
    def _manual(self, records, name, msg):
        r=self._record(records,name); r.status="manual_review_required"; r.warnings.append(msg)
    def _skip(self, records, name, msg):
        r=self._record(records,name); r.status="skipped"; r.warnings.append(msg)
