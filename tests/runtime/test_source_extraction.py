from pathlib import Path

from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator
from runtime.sims_writer_runtime.source.extractor import ArticleSourceExtractor


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_extracts_html_and_removes_non_content_elements():
    html = """<html><head><title>テスト記事</title><style>.x{}</style></head><body>
    <article><h1>テスト記事</h1><p>最初の回答です。</p><h2>手順</h2><p>操作します。</p>
    <script>alert('ignore')</script></article></body></html>"""
    snapshot = ArticleSourceExtractor().extract(html, content_format="auto")
    assert snapshot.status == "available"
    assert snapshot.content_format == "html"
    assert snapshot.title == "テスト記事"
    assert [item["text"] for item in snapshot.headings] == ["テスト記事", "手順"]
    assert "alert" not in snapshot.plain_text
    assert snapshot.content_hash.startswith("sha256:")


def test_extracts_markdown_structure():
    markdown = "# 見出し\n\n本文です。\n\n## 詳細\n\n- 項目1\n- 項目2"
    snapshot = ArticleSourceExtractor().extract(markdown)
    assert snapshot.content_format == "markdown"
    assert snapshot.title == "見出し"
    assert snapshot.headings[1] == {"level": 2, "text": "詳細"}
    assert "項目1" in snapshot.plain_text


def test_missing_existing_content_requires_manual_review():
    request = {
        "schema_version": "1.0",
        "request_id": "REQ-SOURCE-MISSING",
        "request_type": "existing_article_improvement",
        "language": "ja-JP",
        "target_url": "https://example.com/article",
        "main_query": "example query",
        "improvement_goal": ["ctr_improvement"],
        "requested_output": ["publication_package"],
        "source_system": "test",
    }
    result = RuntimeOrchestrator(REPO_ROOT).execute(request)
    source_stage = next(stage for stage in result.stages if stage.name == "source_acquisition")
    assert source_stage.status == "manual_review_required"
    assert result.artifacts["source_snapshot"]["status"] == "missing"


def test_supplied_content_is_connected_to_runtime_snapshot():
    request = {
        "schema_version": "1.0",
        "request_id": "REQ-SOURCE-HTML",
        "request_type": "existing_article_improvement",
        "language": "ja-JP",
        "target_url": "https://example.com/article",
        "current_title": "現在の記事",
        "main_query": "example query",
        "improvement_goal": ["ctr_improvement"],
        "requested_output": ["publication_package"],
        "existing_content": "<article><h1>現在の記事</h1><p>本文がここにあります。本文がここにあります。本文がここにあります。</p></article>",
        "content_format": "html",
        "source_system": "test",
    }
    result = RuntimeOrchestrator(REPO_ROOT).execute(request)
    snapshot = result.artifacts["source_snapshot"]
    assert snapshot["status"] == "available"
    assert snapshot["content_format"] == "html"
    assert snapshot["headings"][0]["level"] == 1
    assert snapshot["original_content"].startswith("<article>")
