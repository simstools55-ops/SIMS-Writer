from pathlib import Path

from runtime.sims_writer_runtime.quality.engine import QualityValidationEngine
from runtime.sims_writer_runtime.quality.foundation import QualityFoundationValidator
from runtime.sims_writer_runtime.refinement.engine import TargetedRefinementEngine
from runtime.sims_writer_runtime.qa import PublicationQAEngine


def engine():
    root = Path(__file__).resolve().parents[2]
    q = QualityValidationEngine(root)
    return PublicationQAEngine(q, QualityFoundationValidator(), TargetedRefinementEngine(q))


def context():
    semantic_ids = {
        "QF-COM-001","QF-COM-002","QF-COM-003","QF-HLP-001","QF-HLP-002","QF-HLP-003",
        "QF-JPN-001","QF-JPN-002","QF-ORG-001","QF-ORG-002","QF-EEA-001","QF-EEA-002",
        "QF-INT-003","QF-SEO-003","QF-SEO-004","QF-SIT-001","QF-SIT-002","QF-SIT-003",
        "QF-STR-002","QF-STR-003","QF-FAC-004"
    }
    return {"main_query": "テスト 方法", "model_assisted_checks": {x: "pass" for x in semantic_ids}}


def draft():
    return {
        "seo_title": "テスト方法を解説", "meta_description": "テスト方法を説明します。",
        "h1": "失敗しない確認手順", "introduction": "最初に結論を示し、その後で必要な確認手順を順番に説明します。初心者でも迷わない構成です。",
        "article_content": "TODO。最初に準備を確認し、次に設定画面を開きます。最後に結果を確認してください。手順ごとの目的もあわせて説明します。",
        "sections": [], "unresolved_items": []}


def test_trace_and_common_contract_are_emitted():
    result = engine().review({"main_query": "テスト 方法", "performance": {}}, draft(), context())
    assert result["qa_contract"] == "SIMS_EDITORIAL_QA_V1"
    assert result["review_cycles_used"] == 1
    assert "article_content" in result["review_trace"][0]["changed_fields"]
    assert result["release_action"] == "publish_corrected_version"


def test_protected_field_is_not_changed():
    class TitleRefinement:
        def refine(self, current, report, context):
            changed = dict(current); changed["seo_title"] = "変更禁止タイトル"
            return {"revised_draft": changed, "revision_records": [{"round":1,"routes":[{"recovery_type":"placeholder_elimination"}]}], "quality_report": report}
    root = Path(__file__).resolve().parents[2]
    q = QualityValidationEngine(root)
    e = PublicationQAEngine(q, QualityFoundationValidator(), TitleRefinement())
    ctx = context(); ctx["qa_policy"] = {"protected_fields": ["seo_title"]}
    result = e.review({"main_query":"テスト 方法","performance":{}}, draft(), ctx)
    assert result["final_draft"]["seo_title"] == "テスト方法を解説"
    assert result["auto_fix_applied"] is False


def test_auto_fix_can_be_disabled():
    ctx = context(); ctx["qa_policy"] = {"allow_auto_fix": False}
    result = engine().review({"main_query":"テスト 方法","performance":{}}, draft(), ctx)
    assert result["auto_fix_applied"] is False
    assert "TODO" in result["final_draft"]["article_content"]
