from runtime.sims_writer_runtime.editorial_signals import (
    build_editorial_signals, detect_intent_gap, detect_hidden_anxiety,
    evaluate_internal_links, evolve_faq, evaluate_conditional_editorial_opinion,
)
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
    assert result.artifacts["knowledge_assembly"]["selected"] == ["shared-editorial-knowledge@1.1.0"]
    assert result.artifacts["decision_action_plan"]["editorial_signals"] == result.artifacts["editorial_signals"]


def test_faq_evolution_adds_only_residual_decision_question():
    result=evolve_faq({
        "main_query":"サービス 料金",
        "supporting_queries":["サービス 解約 方法"],
        "existing_content":"料金プランを説明します",
        "existing_faq":[],
    })
    assert result["needed"] is True
    assert any(c["action"] == "add" for c in result["candidates"])
    answered=evolve_faq({
        "main_query":"サービス 解約 方法",
        "existing_content":"サービスの解約方法を手順付きで説明します",
    })
    assert answered["needed"] is False


def test_conditional_editorial_opinion_requires_missing_decision_support():
    result=evaluate_conditional_editorial_opinion({
        "main_query":"A B 比較 おすすめ",
        "existing_content":"Aは安く、Bは機能が多いです",
        "source_evidence":[{"type":"official"}],
    })
    assert result["applicable"] is True
    existing=evaluate_conditional_editorial_opinion({
        "main_query":"A B 比較 おすすめ",
        "existing_content":"価格を重視するならAがおすすめです",
        "source_evidence":[{"type":"official"}],
    })
    assert existing["applicable"] is False


def test_all_seven_editorial_capabilities_are_emitted():
    signals=build_editorial_signals({"main_query":"A B 比較 おすすめ", "existing_content":"AとBの違い", "source_evidence":[{"type":"official"}]})
    required={
        "intent_gap", "hidden_anxiety", "serp_entity_preservation",
        "internal_link_semantics", "faq_evolution",
        "conditional_editorial_opinion", "evidence_transparency",
    }
    assert required <= set(signals)
