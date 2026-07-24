from pathlib import Path

from runtime.sims_writer_runtime.quality.engine import QualityValidationEngine
from runtime.sims_writer_runtime.quality.foundation import QualityFoundationValidator
from runtime.sims_writer_runtime.refinement.engine import TargetedRefinementEngine
from runtime.sims_writer_runtime.qa import PublicationQAEngine


def build_engine():
    root = Path(__file__).resolve().parents[2]
    quality = QualityValidationEngine(root)
    foundation = QualityFoundationValidator()
    refinement = TargetedRefinementEngine(quality)
    return PublicationQAEngine(quality, foundation, refinement)


def test_auto_fix_then_publish_corrected_version():
    engine = build_engine()
    request = {"main_query": "テスト 方法", "performance": {"average_position": 8, "ctr": 1, "impressions": 1000}}
    draft = {
        "seo_title": "テスト方法を解説",
        "meta_description": "テスト方法を説明します。",
        "h1": "失敗しない確認手順",
        "introduction": "最初に結論を示し、その後で必要な確認手順を順番に説明します。初心者でも迷わない構成です。",
        "article_content": "TODO。最初に準備を確認し、次に設定画面を開きます。最後に結果を確認してください。手順ごとの目的もあわせて説明します。",
        "sections": [],
        "unresolved_items": [],
    }
    semantic_ids = {
        "QF-COM-001","QF-COM-002","QF-COM-003","QF-HLP-001","QF-HLP-002","QF-HLP-003",
        "QF-JPN-001","QF-JPN-002","QF-ORG-001","QF-ORG-002","QF-EEA-001","QF-EEA-002",
        "QF-INT-003","QF-SEO-003","QF-SEO-004","QF-SIT-001","QF-SIT-002","QF-SIT-003",
        "QF-STR-002","QF-STR-003","QF-FAC-004"
    }
    result = engine.review(request, draft, {
        "main_query": "テスト 方法",
        "model_assisted_checks": {rule_id: "pass" for rule_id in semantic_ids},
    })
    assert result["auto_fix_applied"] is True
    assert "TODO" not in result["final_draft"]["article_content"]
    assert result["final_verdict"] in ("PASS_WITH_MINOR_FIX", "PASS_WITH_WARNING")


def test_numeric_title_body_mismatch_holds_publication():
    engine = build_engine()
    request = {"main_query": "料金", "performance": {}}
    draft = {
        "seo_title": "料金は月300円",
        "meta_description": "料金を説明します。",
        "h1": "料金の説明",
        "introduction": "料金の考え方と条件を説明します。十分な長さの導入文です。",
        "article_content": "料金は利用条件によって異なります。",
        "sections": [],
        "unresolved_items": [],
    }
    result = engine.review(request, draft, {"main_query": "料金"})
    assert result["final_verdict"] == "PASS_WITH_REQUIRED_FIX"
    assert result["publishable"] is False
