from __future__ import annotations

import json
from pathlib import Path

from runtime.sims_writer_runtime.claude import ClaudeOutputValidator

ROOT = Path(__file__).resolve().parents[2]


def valid_output() -> dict:
    return {
        "status": "generated",
        "seo_title": "Discord翻訳をiPhoneで使う方法",
        "meta_description": "DiscordをiPhoneで翻訳する方法と設定時の注意点を解説します。",
        "h1": "Discord翻訳をiPhoneで使う方法",
        "article_content": "# Discord翻訳をiPhoneで使う方法\n\n既存記事を改善した本文です。",
        "change_summary": [
            {"area": "title", "before": "旧タイトル", "after": "新タイトル", "reason": "検索意図を明確化"}
        ],
        "faq": [{"question": "自動翻訳できますか？", "answer": "利用環境に応じた設定が必要です。"}],
        "internal_link_recommendations": [
            {"url": "https://example.com/discord-settings", "title": "Discord設定", "reason": "設定手順を補足"}
        ],
        "separate_article_candidates": [{"query": "discord pc 翻訳", "reason": "端末が異なるため"}],
        "unresolved_items": [],
    }


def request_context() -> dict:
    return {
        "existing_content": "既存本文",
        "supporting_queries": ["discord pc 翻訳"],
        "article_catalog": [
            {"url": "https://example.com/discord-settings", "title": "Discord設定"}
        ],
    }


def test_accepts_grounded_generated_output() -> None:
    report = ClaudeOutputValidator(ROOT).validate_text(json.dumps(valid_output(), ensure_ascii=False), request_context())
    assert report.valid
    assert report.status == "accepted"
    assert len(report.sha256) == 64


def test_rejects_unknown_internal_link_url() -> None:
    output = valid_output()
    output["internal_link_recommendations"][0]["url"] = "https://invented.example/article"
    report = ClaudeOutputValidator(ROOT).validate_text(json.dumps(output, ensure_ascii=False), request_context())
    assert not report.valid
    assert any("unknown_internal_link_url" in error for error in report.errors)


def test_rejects_generated_output_without_existing_content() -> None:
    request = request_context()
    request["existing_content"] = ""
    report = ClaudeOutputValidator(ROOT).validate_text(json.dumps(valid_output(), ensure_ascii=False), request)
    assert not report.valid
    assert "safety:generated_without_existing_content" in report.errors


def test_manual_review_requires_unresolved_items() -> None:
    output = valid_output()
    output.update({
        "status": "manual_review_required",
        "seo_title": None,
        "meta_description": None,
        "h1": None,
        "article_content": None,
        "unresolved_items": [],
    })
    report = ClaudeOutputValidator(ROOT).validate_text(json.dumps(output, ensure_ascii=False), request_context())
    assert not report.valid
    assert any("unresolved_items" in error for error in report.errors)


def test_accepts_fenced_json() -> None:
    text = "```json\n" + json.dumps(valid_output(), ensure_ascii=False) + "\n```"
    report = ClaudeOutputValidator(ROOT).validate_text(text, request_context())
    assert report.valid
