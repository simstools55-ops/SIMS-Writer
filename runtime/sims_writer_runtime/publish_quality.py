from __future__ import annotations

from dataclasses import dataclass
from typing import Any

IMPROVEMENT_JUDGMENTS = {"improvement_recommended", "minor_improvement", "maintain_current"}
SEARCH_INTENTS = {"comparison", "purchase", "informational", "troubleshooting", "how_to", "unknown"}


@dataclass(frozen=True)
class PublishQualityAssessment:
    improvement_judgment: str
    search_intent: str
    reason: str
    estimated_minutes: int


def classify_search_intent(main_query: str, title: str = "") -> str:
    text = f"{main_query} {title}".lower()
    if any(token in text for token in ("比較", "違い", "どっち", "おすすめ")):
        return "comparison"
    if any(token in text for token in ("価格", "料金", "購入", "最安", "公式")):
        return "purchase"
    if any(token in text for token in ("できない", "エラー", "不具合", "直らない")):
        return "troubleshooting"
    if any(token in text for token in ("方法", "やり方", "設定", "使い方")):
        return "how_to"
    if main_query.strip():
        return "informational"
    return "unknown"


def classify_search_intents(main_query: str, title: str = "") -> tuple[str, str | None]:
    """Return one primary intent and an optional secondary intent.

    Secondary intent is emitted only when the text contains a distinct,
    decision-relevant signal in addition to the primary intent.
    """
    primary = classify_search_intent(main_query, title)
    text = f"{main_query} {title}".lower()
    secondary: str | None = None
    if primary == "comparison" and any(token in text for token in ("購入", "価格", "料金", "最安", "公式", "おすすめ")):
        secondary = "purchase"
    elif primary == "informational" and any(token in text for token in ("方法", "やり方", "設定", "使い方")):
        secondary = "how_to"
    if secondary == primary:
        secondary = None
    return primary, secondary


def assess_improvement_need(*, ctr: float | None, impressions: float | None,
                            average_position: float | None, title_aligned: bool,
                            intro_answer_first: bool) -> PublishQualityAssessment:
    """Conservative editor-style judgment for partial-mode improvements."""
    measurable = impressions is None or impressions >= 50
    strong_rank = average_position is not None and average_position <= 5
    weak_ctr = ctr is not None and ctr < 0.02

    if strong_rank and not weak_ctr and title_aligned and intro_answer_first:
        return PublishQualityAssessment(
            "maintain_current", "unknown",
            "順位・CTR・タイトル整合性が良好で、大幅変更による悪化リスクが上回るため",
            0,
        )
    if strong_rank and measurable and (weak_ctr or not title_aligned or not intro_answer_first):
        return PublishQualityAssessment(
            "minor_improvement", "unknown",
            "順位は良好なため本文を維持し、タイトル・導入などクリック判断に近い箇所だけを調整するため",
            10,
        )
    return PublishQualityAssessment(
        "improvement_recommended", "unknown",
        "検索意図との不一致または成果指標の改善余地があり、対象箇所の修正が有効と判断したため",
        20,
    )


def validate_before_after_editorial(before_after: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    for index, item in enumerate(before_after):
        path = f"before_after[{index}]"
        if not item.get("reason"):
            issues.append(f"{path}.reason is required")
        if not item.get("expected_effect"):
            issues.append(f"{path}.expected_effect is required")
        if item.get("before") == item.get("after") and not item.get("unchanged_reason"):
            issues.append(f"{path}.unchanged_reason is required when content is unchanged")
    return issues


def validate_comparison_article(draft: dict[str, Any]) -> list[str]:
    """Check that comparison outputs remain internally consistent."""
    if draft.get("search_intent") != "comparison":
        return []
    issues: list[str] = []
    criteria = draft.get("comparison_criteria") or []
    if not criteria:
        issues.append("comparison_criteria is required for comparison articles")
    if not draft.get("comparison_summary"):
        issues.append("comparison_summary is required for comparison articles")
    if not draft.get("recommended_for"):
        issues.append("recommended_for is required for comparison articles")
    if not draft.get("final_conclusion"):
        issues.append("final_conclusion is required for comparison articles")
    winner = draft.get("recommended_product")
    summary = str(draft.get("comparison_summary") or "")
    conclusion = str(draft.get("final_conclusion") or "")
    if winner and winner not in summary and winner not in conclusion:
        issues.append("recommended_product must agree with the comparison summary or final conclusion")
    return issues
