from __future__ import annotations

from copy import deepcopy
from typing import Any

from ..editorial_decision import build_internal_audit_record, build_publication_result, user_visible_publication_result


PUBLIC_COMPONENTS = (
    ("seo_title", "SEOタイトル"),
    ("meta_description", "メタディスクリプション"),
    ("introduction", "導入文"),
    ("h1", "H1"),
    ("article_content", "本文"),
)


def build_publication_view(initial_draft: dict[str, Any], qa_result: dict[str, Any]) -> dict[str, Any]:
    """Build one canonical user-facing view from the final QA result.

    The view never exposes an unreviewed draft as the publication candidate.
    Before/After entries are emitted only for fields actually changed by QA.
    """
    final_draft = deepcopy(qa_result.get("final_draft") or {})
    verdict = qa_result.get("final_verdict", "FAIL")
    publishable = bool(qa_result.get("publishable"))
    changes: list[dict[str, Any]] = []

    for field, label in PUBLIC_COMPONENTS:
        before = initial_draft.get(field)
        after = final_draft.get(field)
        if before != after:
            changes.append({
                "component": field,
                "label": label,
                "before": before,
                "after": after,
                "reason": _reason_for_field(field, qa_result),
                "implementation_status": "implemented",
            })

    advisory = _advisory_messages(qa_result)
    candidate_changes = []
    for item in changes:
        candidate_changes.append({
            **item,
            "component_label": item.get("label"),
            "copy_ready": publishable,
            "evidence_sufficient": publishable,
            "qa_status": "PASS" if publishable else "REQUIRED_FIX",
        })
    publication_result = build_publication_result(candidate_changes)
    internal_audit = build_internal_audit_record(
        publication_result=publication_result, qa_result=qa_result
    )
    return {
        "qa_contract": qa_result.get("qa_contract", "SIMS_EDITORIAL_QA_V1"),
        "qa_engine_version": qa_result.get("qa_engine_version"),
        "publication_verdict": verdict,
        "publication_verdict_label": _verdict_label(verdict),
        "initial_verdict": qa_result.get("initial_verdict", verdict),
        "publishable": publishable,
        "release_action": qa_result.get("release_action"),
        "public_message": _public_message(verdict),
        "auto_fix_applied": bool(qa_result.get("auto_fix_applied")),
        "auto_fixes": deepcopy(qa_result.get("auto_fixes") or []),
        "review_cycles_used": int(qa_result.get("review_cycles_used") or 0),
        "review_trace": deepcopy(qa_result.get("review_trace") or []),
        "unresolved_findings": _unresolved_findings(qa_result),
        "qa_changes": changes,
        "advisories": advisory,
        "publication_content": final_draft if publishable else None,
        "held_draft": final_draft if not publishable else None,
        "publication_result": user_visible_publication_result(publication_result),
        "internal_audit_record": internal_audit,
    }


def apply_qa_to_feedback(feedback: dict[str, Any] | None, publication_view: dict[str, Any]) -> dict[str, Any]:
    """Build the Contract 4.0 minimal public/SBM payload.

    Validation, QA, diagnosis and audit details remain in internal_audit_record
    and are deliberately excluded from the user-facing feedback object.
    """
    source = deepcopy(feedback or {})
    result = {
        "format": "SIMS_FEEDBACK_V2",
        "contract_version": "4.0",
        "site_id": source.get("site_id"),
        "site_name": source.get("site_name"),
        "site_url": source.get("site_url"),
        "article_id": source.get("article_id") or "UNKNOWN",
        "article_url": source.get("article_url") or "",
        "completed_at": source.get("completed_at"),
        "publication_result": deepcopy(publication_view.get("publication_result") or {
            "change_summary": [], "public_ok_changes": [], "user_decision_changes": []
        }),
        "recommended_review_days": source.get("recommended_review_days"),
        "next_action": source.get("next_action"),
    }
    return result


def _reason_for_field(field: str, qa_result: dict[str, Any]) -> str:
    records = (qa_result.get("refinement_result") or {}).get("revision_records") or []
    labels: list[str] = []
    for record in records:
        for route in record.get("routes") or []:
            recovery = route.get("recovery_type")
            if recovery and recovery not in labels:
                labels.append(recovery)
    if labels:
        return "Publication QA auto-fix: " + ", ".join(labels)
    return f"Publication QA corrected {field} before release"


def _advisory_messages(qa_result: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    for report_key in ("final_quality_report", "final_foundation_report"):
        report = qa_result.get(report_key) or {}
        for issue in report.get("issues") or report.get("warnings") or []:
            if isinstance(issue, str):
                message = issue
            else:
                message = issue.get("message") or issue.get("reason") or issue.get("rule_id")
            if message and message not in messages:
                messages.append(str(message))
    return messages


def _public_message(verdict: str) -> str:
    return {
        "PASS": "公開できます。",
        "PASS_WITH_WARNING": "公開できます。注意事項を確認してください。",
        "PASS_WITH_MINOR_FIX": "軽微な修正を反映済みです。修正後の内容を公開できます。",
        "PASS_WITH_REQUIRED_FIX": "公開前の修正が必要です。現在の内容は公開しないでください。",
        "FAIL": "公開できません。手動レビューが必要です。",
    }.get(verdict, "公開判定を確認できません。")


def _unresolved_findings(qa_result: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for report_key in ("final_quality_report", "final_foundation_report"):
        report = qa_result.get(report_key) or {}
        for key in ("issues", "failed_rules", "blocking_issues"):
            for item in report.get(key) or []:
                normalized = item if isinstance(item, dict) else {"message": str(item)}
                if normalized not in findings:
                    findings.append(normalized)
    return findings


def _verdict_label(verdict: str) -> str:
    return {
        "PASS": "公開可能",
        "PASS_WITH_WARNING": "注意事項付きで公開可能",
        "PASS_WITH_MINOR_FIX": "軽微な修正後に公開可能",
        "PASS_WITH_REQUIRED_FIX": "修正後に公開可能",
        "FAIL": "公開不可",
    }.get(verdict, "判定不明")
