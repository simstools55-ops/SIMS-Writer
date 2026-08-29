from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runtime"))

from sims_writer_runtime.editorial_decision import build_publication_result
from sims_writer_runtime.presentation_formatter import build_human_presentation, render_human_markdown, contains_machine_terms


def test_versions_and_shared():
    assert (ROOT / "VERSION").read_text(encoding="utf-8").strip() == "3.3.3"
    assert (ROOT / "SHARED_VERSION").read_text(encoding="utf-8").strip() == "3.5.1"


def test_runtime_preserves_reason_and_expected_effect():
    result = build_publication_result([{
        "component": "internal_link",
        "component_label": "本文（システム設定の見直し手順セクション末尾）",
        "change_type": "ADD",
        "before": None,
        "after": "なお、入力音ではなくキーボード位置の不具合なら関連記事をご覧ください。",
        "reason": "Doctor診断で承認された関連内部リンクだからです。",
        "expected_effect": "関連する別症状の読者を適切な記事へ案内できます。",
        "evidence_level": "HIGH",
        "copy_ready": True,
    }])
    item = result["public_ok_changes"][0]
    assert item["before"] == "（該当箇所なし・新規追加）"
    assert item["reason"].startswith("Doctor診断")
    assert "適切な記事" in item["expected_effect"]


def test_a000024_doctor_referral_is_copy_ready_and_hides_machine_fields():
    publication = {
        "public_ok_changes": [
            {
                "target": "本文（システム設定の見直し手順セクション末尾）",
                "before": "（該当箇所なし・新規追加）",
                "after": "なお、入力音ではなく「キーボードの表示位置がずれる」場合は関連記事をご覧ください。",
                "reason": "関連性の高いDoctor承認済み内部リンクのためです。",
                "expected_effect": "別のキーボード症状で困る読者を適切な記事へ案内できます。",
            },
            {
                "target": "本文（音量調整の方法セクション末尾）",
                "before": "（該当箇所なし・新規追加）",
                "after": "アラーム音が勝手に小さくなる場合は別記事で詳しく解説しています。",
                "reason": "音量関連のDoctor承認済み内部リンクのためです。",
                "expected_effect": "入力音以外の音量トラブルを適切な記事へ案内できます。",
            },
        ],
        "user_decision_changes": [],
    }
    pres = build_human_presentation(
        publication,
        request_mode="DOCTOR_REFERRAL_TREATMENT",
        doctor_presentation={
            "what_to_do": "Doctor診断に基づき、関連性の高い内部リンク2件だけを追加します。",
            "what_not_to_do": ["タイトル", "H1", "URL", "大規模な本文変更"],
            "next_step": "修正後、結果JSONをSBMへ登録してください。",
            "allowed_scope": ["INTERNAL_LINK_ADD"],
            "blocked_scope": ["FULL_REWRITE"],
        },
    )
    md = render_human_markdown(pres, '{"format":"SIMS_FEEDBACK_V2","contract_version":"4.2"}')
    assert md.startswith("今回の修正は、そのまま公開できます。")
    assert md.count("**Before**") == 2
    assert md.count("**After**") == 2
    assert md.count("**理由**") == 2
    assert md.count("**期待する効果**") == 2
    assert "（該当箇所なし・新規追加）" in md
    assert "## 今回変更しないもの" in md
    assert not contains_machine_terms(md)
    assert md.rstrip().endswith("```")


def test_template_makes_before_after_mandatory_for_doctor_referral():
    text = (ROOT / "presentation" / "FEEDBACK_TEMPLATE.md").read_text(encoding="utf-8")
    assert "Doctor Referralでも省略禁止" in text
    assert "**理由**" in text
    assert "**期待する効果**" in text
    assert "allowed_scope" in text and "表示しない" in text
