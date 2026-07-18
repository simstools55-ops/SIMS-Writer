from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
import re

@dataclass
class FoundationIssue:
    code: str
    severity: str
    message: str
    evidence: list[str]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

class QualityFoundationValidator:
    """実記事テスト由来の検索診断・整合性・Contract検査。"""

    NUMERIC_TOKEN = re.compile(r"\d+(?:\.\d+)?(?:\s*[〜～~-]\s*\d+(?:\.\d+)?)?\s*(?:時間|分|日|か月|ヶ月|年|歳|円|%|％|位|件|個|種類|ステップ)")
    SCOPE_WORDS = ("完全", "すべて", "全機種", "全種類", "年代別", "種類別", "コピペOK", "そのまま使える")

    def evaluate(self, request: dict[str, Any], draft: dict[str, Any]) -> dict[str, Any]:
        issues: list[FoundationIssue] = []
        reasons = self._diagnose_search(request)
        self._numeric_consistency(draft, issues)
        self._scope_consistency(draft, issues)
        self._contract_consistency(draft, issues)
        blocking = [i for i in issues if i.severity == "blocking"]
        status = "fail" if blocking else ("pass_with_warnings" if issues else "pass")
        return {
            "framework_version": "1.0.0",
            "status": status,
            "reason_codes": reasons,
            "warning_codes": [i.code for i in issues],
            "issues": [i.to_dict() for i in issues],
            "blocking_issues": [i.to_dict() for i in blocking],
        }

    def _diagnose_search(self, request: dict[str, Any]) -> list[str]:
        perf = request.get("performance") or {}
        pos = self._float(perf.get("average_position") or perf.get("position"))
        ctr = self._float(perf.get("ctr"))
        impressions = self._float(perf.get("impressions"))
        reasons: list[str] = []
        if pos is None:
            return reasons
        if pos <= 10:
            if ctr is not None and ctr < 2:
                reasons.append("RC_CTR_LOW_FOR_POSITION")
            if impressions is not None and impressions >= 500 and ctr is not None and ctr < 2:
                reasons.append("RC_HIGH_IMPRESSIONS_LOW_CTR")
        elif pos <= 20:
            reasons.append("RC_CTR_AND_CONTENT_IMPROVEMENT")
        else:
            reasons.append("RC_POSITION_TOO_LOW_FOR_CTR_ONLY")
        return reasons

    def _numeric_consistency(self, draft: dict[str, Any], issues: list[FoundationIssue]) -> None:
        title = str(draft.get("seo_title") or "")
        body = self._body(draft)
        title_tokens = self.NUMERIC_TOKEN.findall(title)
        if not title_tokens:
            return
        body_tokens = self.NUMERIC_TOKEN.findall(body)
        for token in title_tokens:
            normalized = self._norm(token)
            if not any(self._norm(x) == normalized for x in body_tokens):
                issues.append(FoundationIssue(
                    "WC_TITLE_BODY_MISMATCH", "blocking",
                    "SEOタイトルの数値・期間が本文で同じ条件として確認できません。",
                    [f"title={token}", f"body_numeric_tokens={body_tokens[:20]}"]
                ))

    def _scope_consistency(self, draft: dict[str, Any], issues: list[FoundationIssue]) -> None:
        title = str(draft.get("seo_title") or "")
        body = self._body(draft)
        for word in self.SCOPE_WORDS:
            if word in title and word not in body:
                issues.append(FoundationIssue(
                    "WC_SCOPE_MISMATCH", "warning",
                    f"タイトルの範囲表現「{word}」を本文側で確認できません。",
                    [word]
                ))

    def _contract_consistency(self, draft: dict[str, Any], issues: list[FoundationIssue]) -> None:
        fb = draft.get("sims_feedback") or draft.get("feedback") or {}
        if not isinstance(fb, dict) or not fb:
            return
        changes = fb.get("changes") or {}
        new_values = fb.get("new_values") or {}
        if changes.get("seo_title") and not str(new_values.get("seo_title") or "").strip():
            issues.append(FoundationIssue("WC_NEW_VALUE_MISMATCH", "blocking", "seo_title変更がtrueですが変更後値が空です。", []))
        if changes.get("description") and not str(new_values.get("description") or "").strip():
            issues.append(FoundationIssue("WC_NEW_VALUE_MISMATCH", "blocking", "description変更がtrueですが変更後値が空です。", []))
        mode = fb.get("execution_mode")
        estimated = fb.get("estimated_fields") or []
        if mode == "graceful_degradation" and not estimated:
            issues.append(FoundationIssue("WC_EXECUTION_MODE_MISMATCH", "blocking", "graceful_degradationにはestimated_fieldsが必要です。", []))
        if changes.get("seo_title") and fb.get("next_action") == "monitor":
            issues.append(FoundationIssue("WC_NEXT_ACTION_MISMATCH", "blocking", "SEOタイトル変更後は原則remeasureです。", []))
        warnings = fb.get("warnings") or []
        if warnings and fb.get("confidence") == "high":
            issues.append(FoundationIssue("WC_CONFIDENCE_WARNING_MISMATCH", "warning", "warningがあるためconfidenceの再評価が必要です。", [str(x) for x in warnings[:5]]))

    @staticmethod
    def _body(draft: dict[str, Any]) -> str:
        parts = [str(draft.get(k) or "") for k in ("introduction", "article_content", "conclusion")]
        for section in draft.get("sections") or []:
            if isinstance(section, dict):
                parts.extend([str(section.get("heading") or ""), str(section.get("content") or section.get("text") or "")])
        for faq in draft.get("faq") or []:
            if isinstance(faq, dict): parts.extend([str(faq.get("question") or ""), str(faq.get("answer") or "")])
            else: parts.append(str(faq))
        return "\n".join(parts)

    @staticmethod
    def _norm(value: str) -> str:
        return re.sub(r"\s+", "", value).replace("～", "〜").replace("~", "〜").replace("-", "〜")

    @staticmethod
    def _float(value: Any) -> float | None:
        if value is None or value == "": return None
        try:
            return float(str(value).replace("%", "").replace("％", ""))
        except (ValueError, TypeError):
            return None
