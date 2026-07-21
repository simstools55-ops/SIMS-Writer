from runtime.sims_writer_runtime.editorial_signals import build_editorial_signals, detect_intent_gap, detect_hidden_anxiety, evaluate_internal_links
from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator
from runtime.sims_writer_runtime.adapters.fixture_model import FixtureTransport
from runtime.sims_writer_runtime.adapters.structured_model import StructuredModelAdapter
from pathlib import Path


def test_intent_gap_is_advisory_and_local():
    result=detect_intent_gap({"main_query":"月額料金","seo_title":"買い切り教材の価格","existing_content":"一度購入すれば利用できます"})
    assert result["level"] in {"MEDIUM","HIGH"}
    assert "最小範囲" in result["resolution"]


def test_hidden_anxiety_requires_query_evidence_and_unanswered_content():
    result=detect_hidden_anxiety({"main_query":"サービス 解約","supporting_queries":["返金できる"],"existing_content":"料金を説明します"})
    assert result["detected"] is True
    assert {x["category"] for x in result["items"]} == {"billing"}
    answered=detect_hidden_anxiety({"main_query":"サービス 解約","existing_content":"解約方法と返金条件を説明します"})
    assert answered["detected"] is False


def test_serp_entities_and_preservation_guard_are_emitted():
    signals=build_editorial_signals({"main_query":"iPhone トラッカーとは","seo_title":"iPhoneで「トラッカーが検出されました」と表示される理由","existing_content":"通知の意味を説明"})
    entities=[x.lower() for x in signals["serp_entity_preservation"]["protected_entities"]]
    assert "iphone" in entities
    assert "preservation" in signals["preservation_guard"]


def test_internal_links_reject_string_only_unrelated_candidate():
    result=evaluate_internal_links({"main_query":"トラッカーとは iPhone","target_url":"https://a.example/current","article_catalog":[
        {"article_id":"A1","title":"トラックボールマウスの選び方","url":"https://a.example/ball"},
        {"article_id":"A2","title":"iPhoneの不明なトラッカー通知を止める方法","main_query":"iPhone トラッカー 通知","url":"https://a.example/tracker"},
    ]})
    decisions={x["article_id"]:x["decision"] for x in result["evaluated"]}
    assert decisions["A1"] == "reject"
    assert decisions["A2"] in {"adopt","hold"}


def test_orchestrator_connects_shared_signals():
    raw={"request_id":"REQ-SHARED","main_query":"iPhone トラッカーとは","seo_title":"トラッカーとは","existing_content":"通知の意味","article_catalog":[]}
    result=RuntimeOrchestrator(Path(__file__).resolve().parents[2], adapter=StructuredModelAdapter(FixtureTransport(), "fixture-model")).execute(raw)
    assert "editorial_signals" in result.artifacts
    assert result.artifacts["knowledge_assembly"]["selected"] == ["shared-editorial-knowledge@1.0.0"]
    assert result.artifacts["decision_action_plan"]["editorial_signals"] == result.artifacts["editorial_signals"]
