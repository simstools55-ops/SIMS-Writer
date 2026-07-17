from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import Any
from .models import STAGES, StageRecord, RuntimeResult
from .asset_loader import build_manifest
from .article_context import ArticleContextBuilder
from .intake.request_loader import ImprovementRequestLoader
from .adapters.deterministic_improvement import DeterministicImprovementAdapter
from .adapters.model_protocol import ProductionAdapter
from .quality.engine import QualityValidationEngine
from .refinement.engine import TargetedRefinementEngine
from .source import ArticleSourceAcquisition, UrlSourceFetcher
from .search_intent import SearchIntentAnalyzer

class RuntimeOrchestrator:
    def __init__(self, repo_root: Path, adapter: ProductionAdapter | None = None, *, source_fetch_enabled: bool = False, source_fetcher: UrlSourceFetcher | None = None):
        self.repo_root = repo_root
        self.adapter = adapter or DeterministicImprovementAdapter()
        self.request_loader = ImprovementRequestLoader(repo_root)
        self.quality_engine = QualityValidationEngine(repo_root)
        self.refinement_engine = TargetedRefinementEngine(self.quality_engine)
        self.source_fetch_enabled = source_fetch_enabled
        self.source_acquisition = ArticleSourceAcquisition(fetcher=source_fetcher)
        self.intent_analyzer = SearchIntentAnalyzer()

    def execute(self, raw: dict[str, Any], input_type: str = "auto") -> RuntimeResult:
        execution_id = f"EXE-{uuid4().hex[:12].upper()}"
        records = [StageRecord(name=s) for s in STAGES]
        artifacts: dict[str, Any] = {"raw_request": raw}
        manifest = build_manifest(self.repo_root)
        manifest["execution_id"] = execution_id
        manifest["locked_at"] = datetime.now(timezone.utc).isoformat()
        try:
            self._pass(records, "intake")
            loaded = self.request_loader.load(raw, input_type=input_type)
            request = loaded.payload
            context = ArticleContextBuilder.build(request)
            artifacts["request_metadata"] = {"input_type": loaded.input_type, "schema_version": loaded.schema_version}
            artifacts["normalized_request"] = request
            artifacts["article_context"] = context.to_dict()
            self._pass(records, "normalization")

            source_snapshot = self.source_acquisition.acquire(
                context.existing_content,
                content_format=context.content_format,
                target_url=context.target_url,
                fallback_title=context.current_title,
                fetch_enabled=self.source_fetch_enabled,
            )
            artifacts["source_snapshot"] = source_snapshot.to_dict()
            source_status = source_snapshot.status
            if source_status == "available":
                if source_snapshot.warnings:
                    self._warn(records, "source_acquisition", "; ".join(source_snapshot.warnings))
                else:
                    self._pass(records, "source_acquisition")
            elif source_status == "not_applicable":
                self._skip(records, "source_acquisition", "No existing article source is required")
            else:
                self._manual(records, "source_acquisition", "Existing article content must be supplied for grounded improvement")

            intent_analysis = self.intent_analyzer.analyze(request["main_query"], request.get("supporting_queries") or [])
            artifacts["search_intent_analysis"] = intent_analysis

            artifacts["knowledge_assembly"] = self._assemble_knowledge(request, intent_analysis)
            self._pass(records, "knowledge_assembly")

            plan = self._build_content_plan(request, source_status, execution_id, intent_analysis)
            artifacts["content_plan"] = plan
            if plan["status"] == "ready":
                self._pass(records, "content_planning")
            else:
                self._manual(records, "content_planning", "Existing article content is required for grounded improvement")

            action = "manual_review" if source_status == "missing" else "revise"
            components = list(request.get("improvement_goal") or ["seo_title", "introduction", "faq"])
            artifacts["decision_action_plan"] = {"action": action, "components": components, "reason": "Validated request and supplied source determine the conservative improvement path"}
            self._pass(records, "decision_evaluation")

            artifacts["pattern_selection"] = {"selected_patterns": [], "blocked_by_action": action == "manual_review"}
            self._pass(records, "pattern_selection")

            draft = self.adapter.produce(request, plan, source_snapshot=artifacts["source_snapshot"], search_intent_analysis=intent_analysis, knowledge_assembly=artifacts["knowledge_assembly"], decision_action_plan=artifacts["decision_action_plan"], pattern_selection=artifacts["pattern_selection"])
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
            decision = artifacts["quality_report"]["publish_recommendation"]
            if decision == "publish_ready": self._pass(records, "quality_validation")
            elif decision == "publish_ready_with_advisory": self._warn(records, "quality_validation", "Quality rules completed with advisories")
            else: self._manual(records, "quality_validation", "Quality rules require revision or review")
            refinement = self.refinement_engine.refine(draft, artifacts["quality_report"], quality_context)
            artifacts["refinement_result"] = refinement
            draft = refinement["revised_draft"]
            artifacts["content_draft"] = draft
            artifacts["quality_report"] = refinement["quality_report"]
            decision = artifacts["quality_report"]["publish_recommendation"]
            if refinement["revision_records"]:
                self._warn(records, "refinement", f"Applied {len(refinement['revision_records'])} targeted auto-fix round(s)")
            elif refinement["status"] == "manual_review_required":
                self._manual(records, "refinement", "Remaining issues require manual review")
            elif refinement["status"] == "revision_required":
                self._warn(records, "refinement", "Targeted model revision plan was generated")
            else:
                self._pass(records, "refinement")

            artifacts["publication_package"] = {"publish_decision":decision,"article_content":draft.get("article_content"),"seo_title":draft.get("seo_title"),"meta_description":draft.get("meta_description"),"h1":draft.get("h1"),"quality_summary":artifacts["quality_report"],"refinement_summary":refinement,"runtime_notice":"All 42 canonical Quality Rules were executed and safe targeted fixes were applied before packaging. Context-dependent issues remain explicit."}
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
    def _assemble_knowledge(request: dict[str, Any], intent_analysis: dict[str, Any]) -> dict[str, Any]:
        selected = ["KN-SEO-001", "KN-SEO-CTR", "KN-WRI-INTRO"]
        if request.get("supporting_queries"):
            selected.append("KN-WRI-FAQ")
        if intent_analysis.get("primary", {}).get("intent") == "troubleshooting":
            selected.append("KN-WRI-TROUBLESHOOTING")
        return {
            "coverage": "deterministic_vertical_slice",
            "selected": selected,
            "selection_reason": "CTR improvement baseline selected from request metrics and requested components",
        }

    @staticmethod
    def _build_content_plan(request: dict[str, Any], source_status: str, execution_id: str, intent_analysis: dict[str, Any]) -> dict[str, Any]:
        goals = list(request.get("improvement_goal") or ["seo_title", "introduction", "faq"])
        return {
            "plan_id": f"PLN-{execution_id[4:]}",
            "primary_intent": intent_analysis["primary"]["intent"],
            "primary_intent_label": intent_analysis["primary"]["intent_label"],
            "main_query": request["main_query"],
            "main_answer": f"{request['main_query']}の検索意図に対する結論を冒頭で明確にする",
            "recommended_headings": intent_analysis["heading_recommendations"],
            "faq_candidates": intent_analysis["faq_candidates"],
            "components": goals,
            "status": "ready" if source_status == "available" else "manual_review_required",
        }

    @staticmethod
    def _record(records, name): return next(r for r in records if r.name == name)
    def _pass(self, records, name): self._record(records,name).status = "passed"
    def _warn(self, records, name, msg):
        r=self._record(records,name); r.status="passed_with_warning"; r.warnings.append(msg)
    def _manual(self, records, name, msg):
        r=self._record(records,name); r.status="manual_review_required"; r.warnings.append(msg)
    def _skip(self, records, name, msg):
        r=self._record(records,name); r.status="skipped"; r.warnings.append(msg)
