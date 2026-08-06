from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict
from typing import Any
import re
from .router import IssueRouter

PLACEHOLDER_PATTERNS = (r"\bTODO\b", r"\bTBD\b", r"要確認", r"後で追加", r"\[PLACEHOLDER\]", r"\{\{.*?\}\}")
AI_REPLACEMENTS = {
    "いかがでしたでしょうか": "",
    "見ていきましょう": "以下で確認します",
    "ぜひ参考にしてみてください": "必要な項目を確認してください",
    "重要なポイントとなります": "重要です",
}

class TargetedRefinementEngine:
    """安全な決定論的修正を先に行い、残りを明示的な再作業計画へ変換する。"""
    def __init__(self, quality_engine, max_auto_rounds: int = 3, max_targeted_rounds: int = 3):
        self.quality_engine = quality_engine
        self.router = IssueRouter()
        self.max_auto_rounds = max_auto_rounds
        self.max_targeted_rounds = max_targeted_rounds

    def refine(self, draft: dict[str, Any], quality_report: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        current = deepcopy(draft)
        current_context = deepcopy(context or {})
        revisions: list[dict[str, Any]] = []
        report = quality_report
        for round_no in range(1, self.max_auto_rounds + 1):
            routes = [self.router.route(i) for i in report.get("issues", [])]
            auto_routes = [r for r in routes if r.automatic]
            if not auto_routes:
                break
            before = deepcopy(current)
            for route in auto_routes:
                current = self._apply(current, route.recovery_type, current_context)
            if current == before:
                break
            applied_recoveries = {r.recovery_type for r in auto_routes}
            if "fee_subject_disambiguation" in applied_recoveries:
                audit = deepcopy(current_context.get("publication_integrity_audit") or {})
                audit["ambiguous_fee_claims"] = []
                current_context["publication_integrity_audit"] = audit
            revisions.append({"round": round_no, "type": "auto_fix", "routes": [asdict(r) for r in auto_routes]})
            report = self.quality_engine.evaluate(current, current_context)

        remaining_routes = [self.router.route(i) for i in report.get("issues", [])]
        action_plan = self._build_action_plan(remaining_routes)
        return {
            "revised_draft": current,
            "revision_records": revisions,
            "quality_report": report,
            "action_plan": action_plan,
            "auto_rounds_used": len(revisions),
            "status": self._status(report, action_plan),
        }

    def _apply(self, draft: dict[str, Any], recovery_type: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        d = deepcopy(draft)
        context = context or {}
        fields = ("seo_title", "meta_description", "h1", "introduction", "article_content", "conclusion")
        if recovery_type == "placeholder_elimination":
            for key in fields:
                value = d.get(key)
                if isinstance(value, str):
                    for pattern in PLACEHOLDER_PATTERNS:
                        value = re.sub(pattern, "", value, flags=re.IGNORECASE)
                    d[key] = self._clean(value)
        elif recovery_type == "ai_phrase_reduction":
            for key in fields:
                value = d.get(key)
                if isinstance(value, str):
                    for old, new in AI_REPLACEMENTS.items(): value = value.replace(old, new)
                    d[key] = self._clean(value)
        elif recovery_type == "redundancy_reduction":
            for key in ("article_content", "introduction", "conclusion"):
                if isinstance(d.get(key), str): d[key] = self._dedupe_sentences(d[key])
        elif recovery_type == "heading_hierarchy_repair":
            previous = 1
            repaired=[]
            for section in d.get("sections") or []:
                if not isinstance(section, dict): repaired.append(section); continue
                s=deepcopy(section); level=int(s.get("level",2)); level=min(level, previous+1); level=max(2, level)
                s["level"]=level; previous=level; repaired.append(s)
            d["sections"]=repaired
        elif recovery_type == "unsupported_claim_softening":
            replacements = (context.get("auto_repair") or {}).get("claim_replacements") or []
            for key in fields:
                value = d.get(key)
                if isinstance(value, str):
                    for item in replacements:
                        old, new = str(item.get("before") or ""), str(item.get("after") or "")
                        if old: value = value.replace(old, new)
                    d[key] = value
        elif recovery_type == "unverified_value_redaction":
            values = (context.get("auto_repair") or {}).get("unverified_values") or []
            replacement_text = (context.get("auto_repair") or {}).get("verification_text", "公式情報を確認してください")
            for key in fields:
                value = d.get(key)
                if isinstance(value, str):
                    for raw in values:
                        if str(raw): value = value.replace(str(raw), replacement_text)
                    d[key] = value
        elif recovery_type == "fee_subject_disambiguation":
            repairs = (context.get("auto_repair") or {}).get("fee_claim_repairs") or []
            component_aliases = {
                "article_title": "h1", "description": "meta_description", "meta": "meta_description",
                "seo_title": "seo_title", "h1": "h1", "introduction": "introduction",
                "article_content": "article_content", "conclusion": "conclusion",
            }
            for item in repairs:
                component = str(item.get("component") or item.get("target") or "article_content")
                key = component_aliases.get(component, component)
                before, after = str(item.get("before") or ""), str(item.get("after") or "")
                if key == "sections":
                    for section in d.get("sections") or []:
                        if isinstance(section, dict):
                            for field in ("heading", "content"):
                                value = section.get(field)
                                if isinstance(value, str) and before:
                                    section[field] = value.replace(before, after)
                elif isinstance(d.get(key), str) and before:
                    d[key] = d[key].replace(before, after)
                else:
                    for field in fields:
                        value = d.get(field)
                        if isinstance(value, str) and before:
                            d[field] = value.replace(before, after)
                    for section in d.get("sections") or []:
                        if isinstance(section, dict):
                            for field in ("heading", "content"):
                                value = section.get(field)
                                if isinstance(value, str) and before:
                                    section[field] = value.replace(before, after)
        elif recovery_type == "title_promise_softening":
            for key in ("seo_title", "h1", "meta_description", "introduction"):
                value = d.get(key)
                if isinstance(value, str):
                    value = value.replace("徹底比較", "比較").replace("徹底的に比較", "比較").replace("完全ガイド", "ガイド")
                    d[key] = value
        elif recovery_type == "json_publication_sync":
            feedback = d.get("feedback")
            if isinstance(feedback, dict):
                publication = feedback.get("publication_result") or {}
                for item in publication.get("public_ok_changes") or []:
                    target = item.get("target") or item.get("component")
                    if target in d and item.get("after") is not None:
                        d[target] = item.get("after")
        return d

    @staticmethod
    def _clean(value: str) -> str:
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip(" \n、。") + ("。" if value.strip() and not value.strip().endswith(("。","！","？")) else "")

    @staticmethod
    def _dedupe_sentences(text: str) -> str:
        seen=set(); out=[]
        for sentence in re.split(r"(?<=[。！？])", text):
            key=re.sub(r"\s+", "", sentence)
            if not key or key in seen: continue
            seen.add(key); out.append(sentence)
        return "".join(out).strip()

    @staticmethod
    def _build_action_plan(routes):
        return {
            "manual_review_required": any(r.return_stage == "manual_review" for r in routes),
            "targeted_revisions": [asdict(r) for r in routes if not r.automatic and r.return_stage != "manual_review"],
            "manual_reviews": [asdict(r) for r in routes if r.return_stage == "manual_review"],
            "resume_stages": sorted({r.return_stage for r in routes if r.return_stage != "manual_review"}),
        }

    @staticmethod
    def _status(report, plan):
        decision=report.get("publish_recommendation")
        if decision in ("publish_ready", "publish_ready_with_advisory"): return decision
        if plan.get("manual_review_required"): return "manual_review_required"
        return "revision_required"
