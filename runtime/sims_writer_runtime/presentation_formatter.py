from __future__ import annotations

from copy import deepcopy
from typing import Any

MACHINE_ONLY_TERMS = (
    "allowed_scope", "blocked_scope", "doctor_referral", "actions_permitted",
    "actions_prohibited", "contract_version", "routing", "confidence_percent",
)


def _normalise_public_change(change: dict[str, Any]) -> dict[str, Any]:
    item = deepcopy(change)
    before = item.get("before")
    if before in (None, ""):
        before = "（該当箇所なし・新規追加）"
    return {
        "target": item.get("target") or item.get("component_label") or item.get("component") or "変更箇所",
        "before": before,
        "after": item.get("after") or "",
        "reason": item.get("reason") or item.get("change_reason") or "読者が必要な情報へ自然に進めるようにするためです。",
        "expected_effect": item.get("expected_effect") or item.get("benefit") or "読者にとって内容や導線が分かりやすくなります。",
    }


def build_human_presentation(
    publication_result: dict[str, Any],
    *,
    request_mode: str | None = None,
    doctor_presentation: dict[str, Any] | None = None,
    unchanged_items: list[str] | None = None,
) -> dict[str, Any]:
    """Build the Human Layer without exposing machine-facing referral internals.

    The same presentation shape is used for normal improvements and
    DOCTOR_REFERRAL_TREATMENT.  Before/After is mandatory for every PUBLIC_OK change.
    """
    public_ok = [_normalise_public_change(x) for x in (publication_result.get("public_ok_changes") or [])]
    user_decision = deepcopy(publication_result.get("user_decision_changes") or [])
    status = (
        "公開OKの修正はそのまま反映できます。利用者判断の項目だけ確認してください。"
        if user_decision else "今回の修正は、そのまま公開できます。"
    )
    doctor_presentation = doctor_presentation or {}
    summary = doctor_presentation.get("what_to_do") or doctor_presentation.get("summary")
    if not summary:
        count = len(public_ok)
        summary = f"今回は公開OKの修正を{count}件反映します。" if count else "今回は公開する修正はありません。"
    return {
        "publication_status": status,
        "what_to_do": summary,
        "changes": public_ok,
        "unchanged_items": list(unchanged_items or doctor_presentation.get("what_not_to_do") or []),
        "next_step": doctor_presentation.get("next_step") or "修正後、結果JSONをSBMへ登録してください。",
        "request_mode": request_mode or "STANDARD",
    }


def render_human_markdown(presentation: dict[str, Any], feedback_json: str | None = None) -> str:
    """Render the fixed Presentation Standard. JSON, when supplied, is always last."""
    lines: list[str] = [presentation["publication_status"], "", "## 今回やること", "", str(presentation["what_to_do"])]
    changes = presentation.get("changes") or []
    if changes:
        lines += ["", "## 公開OK（そのままコピペ可能）"]
    for idx, item in enumerate(changes, 1):
        lines += [
            "", f"### 修正{idx}：{item['target']}",
            "", "**Before**", f"> {str(item['before']).replace(chr(10), chr(10)+'> ')}",
            "", "**After**", f"> {str(item['after']).replace(chr(10), chr(10)+'> ')}",
            "", "**理由**", str(item["reason"]),
            "", "**期待する効果**", str(item["expected_effect"]),
        ]
    unchanged = presentation.get("unchanged_items") or []
    if unchanged:
        lines += ["", "## 今回変更しないもの", "", "・" + "\n・".join(map(str, unchanged))]
    lines += ["", "## 次の作業", "", str(presentation["next_step"])]
    if feedback_json is not None:
        lines += ["", "```json", feedback_json.strip(), "```"]
    return "\n".join(lines).rstrip() + "\n"


def contains_machine_terms(markdown: str) -> bool:
    """Check only the Human Layer; the final fenced JSON remains machine-facing by design."""
    human = markdown.split("```json", 1)[0]
    low = human.lower()
    return any(term.lower() in low for term in MACHINE_ONLY_TERMS)
