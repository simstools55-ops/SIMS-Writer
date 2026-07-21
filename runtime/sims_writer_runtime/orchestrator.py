from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any
from .models import STAGES, StageRecord, RuntimeResult
from .asset_loader import build_manifest
from .adapters.input_adapters import normalize_generic, normalize_sbm
from .adapters.manual_model import ManualModelAdapter
from .adapters.model_protocol import ProductionAdapter
from .quality.engine import QualityValidationEngine
from .quality.foundation import QualityFoundationValidator
from .refinement.engine import TargetedRefinementEngine
from .editorial_signals import build_editorial_signals

class RuntimeOrchestrator:
    def __init__(self, repo_root: Path, adapter: ProductionAdapter | None = None):
        self.repo_root = repo_root
        self.adapter = adapter or ManualModelAdapter()
        self.quality_engine = QualityValidationEngine(repo_root)
        self.quality_foundation = QualityFoundationValidator()
        self.refinement_engine = TargetedRefinementEngine(self.quality_engine)

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
            artifacts["source_identity"] = {
                "site_id": request.get("site_id"),
                "site_name": request.get("site_name"),
                "site_url": request.get("site_url"),
                "article_id": request.get("article_id"),
                "article_url": request.get("target_url"),
            }
            if request.get("main_query_inferred"):
                self._warn(records, "normalization", "main_query was inferred from the title")
            elif request.get("main_query_missing"):
                self._warn(records, "normalization", "main_query is missing; query-dependent checks will be degraded")
            else:
                self._pass(records, "normalization")

            source_status = "unavailable" if request.get("target_url") else "not_applicable"
            artifacts["source_snapshot"] = {"status": source_status, "target_url": request.get("target_url")}
            self._warn(records, "source_acquisition", "Alpha runtime does not fetch external content")

            artifacts["editorial_signals"] = build_editorial_signals(request)
            artifacts["knowledge_assembly"] = {
                "coverage": "partial",
                "selected": ["shared-editorial-knowledge@1.0.0"],
                "shared_editorial_signals": artifacts["editorial_signals"],
                "note": "Shared Knowledge is applied as advisory signals under Writer preservation constraints",
            }
            self._pass(records, "knowledge_assembly")

            plan = {
                "plan_id": f"PLN-{execution_id[4:]}",
                "primary_intent": request.get("main_query") or request.get("seo_title") or request.get("current_title") or "",
                "main_answer": None,
                "status": "degraded" if request.get("main_query_missing") else "ready",
            }
            artifacts["content_plan"] = plan
            if request.get("main_query_missing"):
                self._warn(records, "content_planning", "Query-dependent planning was skipped; other improvements remain available")
            else:
                self._warn(records, "content_planning", "Main answer requires production adapter")

            action = "revise"
            action_reason = "Continue with available input; unavailable source is advisory"
            artifacts["decision_action_plan"] = {"action": action, "components": [], "reason": action_reason, "editorial_signals": artifacts["editorial_signals"]}
            self._pass(records, "decision_evaluation")

            artifacts["pattern_selection"] = {"selected_patterns": ["PT-PLN-008", "PT-SEO-008", "PT-SEO-009", "PT-EVD-007"], "blocked_by_action": False, "selection_basis": "shared_editorial_signals"}
            if request.get("article_catalog"):
                self._pass(records, "pattern_selection")
            else:
                artifacts["internal_link_selection"] = {"status": "skipped", "reason": "article_catalog is unavailable"}
                self._skip(records, "pattern_selection", "article_catalog is unavailable; internal-link selection only was skipped")

            draft = self.adapter.produce(request, plan, source_snapshot=artifacts["source_snapshot"], knowledge_assembly=artifacts["knowledge_assembly"], decision_action_plan=artifacts["decision_action_plan"], pattern_selection=artifacts["pattern_selection"])
            artifacts["content_draft"] = draft
            
            if draft.get("article_content"):
                self._pass(records, "content_production")
            else:
                self._manual(records, "content_production", "Production adapter did not return article content")

            quality_context = {
                "main_query": request.get("main_query"),
                "sources": artifacts.get("source_evidence", []),
                "experience_verified": bool(draft.get("experience_verified", False)),
                "model_assisted_checks": draft.get("model_assisted_checks", {}),
            }
            artifacts["quality_report"] = self.quality_engine.evaluate(draft, quality_context)
            artifacts["quality_foundation_report"] = self.quality_foundation.evaluate(request, draft)
            decision = artifacts["quality_report"]["publish_recommendation"]
            if decision == "publish_ready": self._pass(records, "quality_validation")
            elif decision == "publish_ready_with_advisory": self._warn(records, "quality_validation", "Quality rules completed with advisories")
            else: self._manual(records, "quality_validation", "Quality rules require revision or review")
            refinement = self.refinement_engine.refine(draft, artifacts["quality_report"], quality_context)
            artifacts["refinement_result"] = refinement
            draft = refinement["revised_draft"]
            artifacts["content_draft"] = draft
            artifacts["quality_report"] = refinement["quality_report"]
            artifacts["quality_foundation_report"] = self.quality_foundation.evaluate(request, draft)
            decision = artifacts["quality_report"]["publish_recommendation"]
            if refinement["revision_records"]:
                self._warn(records, "refinement", f"Applied {len(refinement['revision_records'])} targeted auto-fix round(s)")
            elif refinement["status"] == "manual_review_required":
                self._manual(records, "refinement", "Remaining issues require manual review")
            elif refinement["status"] == "revision_required":
                self._warn(records, "refinement", "Targeted model revision plan was generated")
            else:
                self._pass(records, "refinement")

            artifacts["publication_package"] = {"publish_decision":decision,"article_content":draft.get("article_content"),"seo_title":draft.get("seo_title"),"meta_description":draft.get("meta_description"),"h1":draft.get("h1"),"quality_summary":artifacts["quality_report"],"quality_foundation":artifacts["quality_foundation_report"],"refinement_summary":refinement,"runtime_notice":"All 42 canonical Quality Rules were executed and safe targeted fixes were applied before packaging. Context-dependent issues remain explicit."}
            if decision in ("revision_required", "manual_review_required", "rejected"): self._manual(records, "publication_packaging", "Package requires revision or review")
            elif decision == "publish_ready_with_advisory": self._warn(records, "publication_packaging", "Package generated with advisory")
            else: self._pass(records, "publication_packaging")
            status = decision
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
