from __future__ import annotations

from copy import deepcopy
from typing import Any

from .contracts import QAReviewCycle, QAReviewPolicy


class PublicationQAEngine:
    """公開前の品質評価・限定修正・再評価・公開判定を統括する。"""

    VERDICT_PASS = "PASS"
    VERDICT_WARNING = "PASS_WITH_WARNING"
    VERDICT_MINOR_FIX = "PASS_WITH_MINOR_FIX"
    VERDICT_REQUIRED_FIX = "PASS_WITH_REQUIRED_FIX"
    VERDICT_FAIL = "FAIL"

    def __init__(self, quality_engine, foundation_validator, refinement_engine):
        self.quality_engine = quality_engine
        self.foundation_validator = foundation_validator
        self.refinement_engine = refinement_engine

    def review(self, request: dict[str, Any], draft: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        policy = QAReviewPolicy.from_context(context)
        initial_draft = deepcopy(draft)
        current = deepcopy(draft)
        initial_quality = self.quality_engine.evaluate(current, context)
        initial_foundation = self.foundation_validator.evaluate(request, current)
        initial_verdict = self._verdict(initial_quality, initial_foundation, auto_fixed=False)
        quality, foundation, verdict = initial_quality, initial_foundation, initial_verdict
        cycles: list[dict[str, Any]] = []
        all_revision_records: list[dict[str, Any]] = []

        last_refinement = {
            "revised_draft": current,
            "revision_records": [],
            "quality_report": quality,
            "action_plan": {"manual_review_required": False, "targeted_revisions": [], "manual_reviews": [], "resume_stages": []},
            "auto_rounds_used": 0,
            "status": quality.get("publish_recommendation", "revision_required"),
        }
        for cycle_no in range(1, policy.max_review_cycles + 1):
            if not policy.allow_auto_fix or verdict == self.VERDICT_FAIL:
                break
            before = deepcopy(current)
            refinement = self.refinement_engine.refine(current, quality, context)
            last_refinement = refinement
            candidate = refinement["revised_draft"]
            candidate, blocked = self._restore_protected(before, candidate, policy.protected_fields)
            changed = self._changed_top_level_fields(before, candidate)
            records = [r for r in refinement.get("revision_records", []) if self._record_allowed(r, policy)]
            auto_fixed = bool(changed and records)
            if not auto_fixed:
                break
            current = candidate
            quality = self.quality_engine.evaluate(current, context)
            foundation = self.foundation_validator.evaluate(request, current)
            next_verdict = self._verdict(quality, foundation, auto_fixed=True)
            cycle = QAReviewCycle(cycle_no, verdict, next_verdict, True, changed, blocked, records)
            cycles.append(cycle.to_dict())
            all_revision_records.extend(records)
            verdict = next_verdict
            if verdict in (self.VERDICT_PASS, self.VERDICT_WARNING, self.VERDICT_MINOR_FIX, self.VERDICT_FAIL):
                break

        any_fix = bool(all_revision_records)
        final_verdict = verdict
        if any_fix and final_verdict == self.VERDICT_PASS:
            final_verdict = self.VERDICT_MINOR_FIX
        publishable = final_verdict in {self.VERDICT_PASS, self.VERDICT_WARNING, self.VERDICT_MINOR_FIX}
        return {
            "qa_engine_version": "1.1.0",
            "qa_contract": "SIMS_EDITORIAL_QA_V1",
            "policy": policy.to_dict(),
            "initial_verdict": initial_verdict,
            "final_verdict": final_verdict,
            "publishable": publishable,
            "auto_fix_applied": any_fix,
            "auto_fixes": self._auto_fixes(all_revision_records),
            "review_cycles_used": len(cycles),
            "review_trace": cycles,
            "initial_quality_report": initial_quality,
            "initial_foundation_report": initial_foundation,
            "final_quality_report": quality,
            "final_foundation_report": foundation,
            "refinement_result": {
                **last_refinement,
                "revised_draft": current,
                "quality_report": quality,
                "revision_records": all_revision_records,
                "auto_rounds_used": len(all_revision_records),
                "status": quality.get("publish_recommendation", last_refinement.get("status", "revision_required")),
            },
            "final_draft": current,
            "release_action": self._release_action(final_verdict),
            "manual_review_required": final_verdict in (self.VERDICT_REQUIRED_FIX, self.VERDICT_FAIL),
        }

    def _verdict(self, quality: dict[str, Any], foundation: dict[str, Any], auto_fixed: bool) -> str:
        foundation_status = foundation.get("status")
        recommendation = quality.get("publish_recommendation")
        issues = quality.get("issues") or []
        if recommendation in ("rejected", "manual_review_required"):
            return self.VERDICT_FAIL
        if foundation_status == "fail" or recommendation == "revision_required":
            return self.VERDICT_REQUIRED_FIX
        if recommendation == "publish_ready_with_advisory" or foundation_status == "pass_with_warnings":
            return self.VERDICT_WARNING
        if any(i.get("result") in ("warning", "unable_to_verify") for i in issues):
            return self.VERDICT_WARNING
        return self.VERDICT_PASS

    @staticmethod
    def _changed_top_level_fields(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
        return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))

    @staticmethod
    def _restore_protected(before: dict[str, Any], after: dict[str, Any], protected_fields: tuple[str, ...]) -> tuple[dict[str, Any], list[str]]:
        result = deepcopy(after)
        blocked: list[str] = []
        for field in protected_fields:
            if before.get(field) != result.get(field):
                result[field] = deepcopy(before.get(field))
                blocked.append(field)
        return result, blocked

    @staticmethod
    def _record_allowed(record: dict[str, Any], policy: QAReviewPolicy) -> bool:
        routes = record.get("routes") or []
        return bool(routes) and all(r.get("recovery_type") in policy.allowed_auto_fix_classes for r in routes)

    @staticmethod
    def _auto_fixes(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        fixes=[]
        for record in records:
            routes=record.get("routes") or []
            fixes.append({
                "component": record.get("component") or record.get("target_component") or "unknown",
                "action": record.get("action") or record.get("revision_type") or "targeted_revision",
                "rules": [r.get("rule_id") or r.get("recovery_type") for r in routes if r.get("rule_id") or r.get("recovery_type")],
            })
        return fixes

    @staticmethod
    def _release_action(verdict: str) -> str:
        return {
            "PASS": "publish",
            "PASS_WITH_WARNING": "publish_with_advisory",
            "PASS_WITH_MINOR_FIX": "publish_corrected_version",
            "PASS_WITH_REQUIRED_FIX": "hold_and_revise",
            "FAIL": "stop_publication_and_manual_review",
        }[verdict]
