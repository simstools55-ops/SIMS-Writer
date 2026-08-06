from pathlib import Path


def _draft():
    return {
        "seo_title": "トリバゴの仕組み｜手数料と収益モデル",
        "meta_description": "トリバゴの手数料はかからない仕組みを解説します。",
        "h1": "トリバゴの仕組みと手数料",
        "introduction": "トリバゴの手数料はかかりません。",
        "article_content": "Q10. トリバゴの手数料はいくら？\nA. 手数料はかかりません。",
        "conclusion": "利用者は無料です。",
        "sections": [{"level": 2, "heading": "トリバゴの収益モデルと手数料｜なぜ無料で使えるのか", "content": "手数料はかかりません。"}],
    }


def test_fee_subject_rule_and_asset_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "quality/rules/factuality/QF-FAC-006-fee-subject-clarity.yaml").exists()
    assert (root / "runtime/fee-subject-auto-repair-v3.0.2.md").exists()


def test_ambiguous_fee_claim_is_auto_repaired():
    from runtime.sims_writer_runtime.quality.engine import QualityValidationEngine
    from runtime.sims_writer_runtime.refinement.engine import TargetedRefinementEngine
    root = Path(__file__).resolve().parents[1]
    engine = QualityValidationEngine(root)
    context = {
        "main_query": "トリバゴ 仕組み",
        "sources": ["official-help"],
        "publication_integrity_audit": {"ambiguous_fee_claims": ["手数料の支払主体が不明"]},
        "auto_repair": {"fee_claim_repairs": [
            {"component": "meta_description", "before": "トリバゴの手数料はかからない仕組みを解説します。", "after": "利用者がトリバゴへ直接支払う手数料はありません。予約サイト側の費用は予約確定前に確認してください。"},
            {"component": "introduction", "before": "トリバゴの手数料はかかりません。", "after": "利用者がトリバゴへ直接支払う手数料はありません。"},
            {"component": "article_content", "before": "A. 手数料はかかりません。", "after": "A. 利用者がトリバゴへ直接支払う手数料はありません。トリバゴは予約サイトから支払われる送客手数料などで収益を得ます。予約サイト側のサービス料や税は総額確認が必要です。"},
            {"component": "sections", "before": "トリバゴの収益モデルと手数料｜なぜ無料で使えるのか", "after": "トリバゴの収益モデルと手数料｜利用者は無料？誰が支払う？"},
            {"component": "sections", "before": "手数料はかかりません。", "after": "利用者がトリバゴへ直接支払う手数料はありません。"},
        ]},
    }
    report = engine.evaluate(_draft(), context)
    assert any(i["rule_id"] == "QF-FAC-006" for i in report["issues"])
    result = TargetedRefinementEngine(engine).refine(_draft(), report, context)
    revised = result["revised_draft"]
    assert "利用者がトリバゴへ直接支払う手数料はありません" in revised["meta_description"]
    assert "誰が支払う" in revised["sections"][0]["heading"]
    assert not any(i["rule_id"] == "QF-FAC-006" for i in result["quality_report"]["issues"])
