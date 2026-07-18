from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from runtime.sims_writer_runtime.quality.foundation import QualityFoundationValidator


def test_low_rank_is_not_ctr_only():
    report=QualityFoundationValidator().evaluate(
        {"performance":{"average_position":41.0,"ctr":0.2,"impressions":3000}},
        {"seo_title":"60歳の履歴書の書き方", "article_content":"60歳の履歴書の書き方を解説します。"}
    )
    assert "RC_POSITION_TOO_LOW_FOR_CTR_ONLY" in report["reason_codes"]


def test_title_numeric_mismatch_blocks():
    report=QualityFoundationValidator().evaluate(
        {"performance":{"average_position":10.0,"ctr":0.2,"impressions":2773}},
        {"seo_title":"プリンを冷やす時間は2〜3時間", "article_content":"寒天プリンは1時間、焼きプリンは3〜4時間が目安です。"}
    )
    assert report["status"] == "fail"
    assert "WC_TITLE_BODY_MISMATCH" in report["warning_codes"]


def test_feedback_contract_mismatches():
    draft={
        "seo_title":"改善後タイトル", "article_content":"本文",
        "sims_feedback":{
            "changes":{"seo_title":True,"description":False},
            "new_values":{"seo_title":""},
            "execution_mode":"graceful_degradation",
            "estimated_fields":[],
            "next_action":"monitor",
            "confidence":"high",
            "warnings":["確認が必要"]
        }
    }
    report=QualityFoundationValidator().evaluate({},draft)
    codes=set(report["warning_codes"])
    assert {"WC_NEW_VALUE_MISMATCH","WC_EXECUTION_MODE_MISMATCH","WC_NEXT_ACTION_MISMATCH","WC_CONFIDENCE_WARNING_MISMATCH"} <= codes


def test_valid_title_number_passes():
    report=QualityFoundationValidator().evaluate({}, {
        "seo_title":"冷蔵庫で2〜3時間冷やす方法",
        "article_content":"冷蔵庫で2〜3時間冷やすのが目安です。"
    })
    assert "WC_TITLE_BODY_MISMATCH" not in report["warning_codes"]
