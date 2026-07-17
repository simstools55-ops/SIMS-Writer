from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.publish_quality import (
    assess_improvement_need,
    classify_search_intent,
    validate_before_after_editorial,
    validate_comparison_article,
)
from runtime.sims_writer_runtime.vertical_slices.ctr_improvement import CTRImprovementSlice


def test_search_intent_classifies_comparison():
    assert classify_search_intent("商品A 商品B 比較") == "comparison"


def test_strong_article_can_be_maintained():
    result = assess_improvement_need(
        ctr=0.05, impressions=500, average_position=3.2,
        title_aligned=True, intro_answer_first=True,
    )
    assert result.improvement_judgment == "maintain_current"
    assert result.estimated_minutes == 0


def test_high_rank_low_ctr_is_minor_improvement():
    result = assess_improvement_need(
        ctr=0.013, impressions=75, average_position=4.6,
        title_aligned=True, intro_answer_first=False,
    )
    assert result.improvement_judgment == "minor_improvement"
    assert result.estimated_minutes == 10


def test_before_after_requires_expected_effect():
    issues = validate_before_after_editorial([
        {"component": "seo_title", "before": "旧", "after": "新", "reason": "改善"}
    ])
    assert any("expected_effect" in issue for issue in issues)


def test_comparison_validator_requires_editorial_elements():
    issues = validate_comparison_article({"search_intent": "comparison"})
    assert len(issues) == 4


def test_ctr_slice_exposes_rc3_publish_quality():
    raw = {
        "ArticleID": "A000008",
        "ArticleTitle": "商品Aと商品Bを5つの項目で比較！",
        "SEOTitle": "商品Aと商品Bを5つの項目で比較！",
        "MainQuery": "商品A 商品B 比較",
        "ExistingContent": "結論から言うと商品Bがおすすめです。" * 20,
        "Clicks": 1, "Impressions": 75, "CTR": "1.3%", "AveragePosition": 4.6,
    }
    s = CTRImprovementSlice()
    req = s.normalize(raw)
    dec = s.decide(req)
    draft = s.build_draft(req, dec)
    package = s.build_output(req, dec, draft)
    assert dec.search_intent == "comparison"
    assert dec.improvement_judgment in {"minor_improvement", "improvement_recommended"}
    assert package["publish_quality"]["estimated_minutes"] in {10, 20}
    assert all("expected_effect" in item for item in package["user_output"])
