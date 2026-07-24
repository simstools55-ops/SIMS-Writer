from __future__ import annotations

from copy import deepcopy
from typing import Any


class PublicationQAEngine:
    """公開前の品質評価・安全な自動修正・再評価を統括する。"""

    VERDICT_PASS = "PASS"
    VERDICT_WARNING = "PASS_WITH_WARNING"
    VERDICT_MINOR_FIX = "PASS_WITH_MINOR_FIX"
    VERDICT_REQUIRED_FIX = "PASS_WITH_REQUIRED_FIX"
    VERDICT_FAIL = "FAIL"

    def __init__(self, quality_engine, foundation_validator, refinement_engine):
        self.quality_engine = quality_engine
        self.foundation_validator = foundation_validator
        self.refinement_engine = refinement_engine

    def review(
        self,
        request: dict[str, Any],
        draft: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = context or {}
        initial_draft = deepcopy(draft)
        initial_quality = self.quality_engine.evaluate(initial_draft, context)
        initial_foundation = self.foundation_validator.evaluate(request, initial_draft)
        initial_verdict = self._verdict(initial_quality, initial_foundation, auto_fixed=False)

        refinement = self.refinement_engine.refine(initial_draft, initial_quality, context)
        final_draft = refinement["revised_draft"]
        final_quality = refinement["quality_report"]
        final_foundation = self.foundation_validator.evaluate(request, final_draft)
        auto_fixed = bool(refinement.get("revision_records"))
        final_verdict = self._verdict(final_quality, final_foundation, auto_fixed=auto_fixed)

        publishable = final_verdict in {
            self.VERDICT_PASS,
            self.VERDICT_WARNING,
            self.VERDICT_MINOR_FIX,
        }
        return {
            "qa_engine_version": "1.0.0",
            "initial_verdict": initial_verdict,
            "final_verdict": final_verdict,
            "publishable": publishable,
            "auto_fix_applied": auto_fixed,
            "initial_quality_report": initial_quality,
            "initial_foundation_report": initial_foundation,
            "refinement_result": refinement,
            "final_quality_report": final_quality,
            "final_foundation_report": final_foundation,
            "final_draft": final_draft,
            "release_action": self._release_action(final_verdict),
        }

    def _verdict(self, quality: dict[str, Any], foundation: dict[str, Any], auto_fixed: bool) -> str:
        foundation_status = foundation.get("status")
        recommendation = quality.get("publish_recommendation")
        issues = quality.get("issues") or []

        if foundation_status == "fail":
            return self.VERDICT_REQUIRED_FIX
        if recommendation in ("rejected", "manual_review_required"):
            return self.VERDICT_FAIL
        if recommendation == "revision_required":
            return self.VERDICT_REQUIRED_FIX
        if auto_fixed:
            return self.VERDICT_MINOR_FIX
        if recommendation == "publish_ready_with_advisory" or foundation_status == "pass_with_warnings":
            return self.VERDICT_WARNING
        if any(i.get("result") in ("warning", "unable_to_verify") for i in issues):
            return self.VERDICT_WARNING
        return self.VERDICT_PASS

    @staticmethod
    def _release_action(verdict: str) -> str:
        return {
            "PASS": "publish",
            "PASS_WITH_WARNING": "publish_with_advisory",
            "PASS_WITH_MINOR_FIX": "publish_corrected_version",
            "PASS_WITH_REQUIRED_FIX": "hold_and_revise",
            "FAIL": "stop_publication_and_manual_review",
        }[verdict]
