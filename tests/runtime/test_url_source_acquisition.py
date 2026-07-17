from pathlib import Path

import pytest

from runtime.sims_writer_runtime.orchestrator import RuntimeOrchestrator
from runtime.sims_writer_runtime.source import FetchedSource, SourceFetchError, UrlSourceFetcher


REPO_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_URL = "https://93.184.216.34/article"


def _request(url: str = PUBLIC_URL) -> dict:
    return {
        "schema_version": "1.0",
        "request_id": "REQ-URL-FETCH",
        "request_type": "existing_article_improvement",
        "language": "ja-JP",
        "target_url": url,
        "current_title": "取得前タイトル",
        "main_query": "URL 本文 取得",
        "improvement_goal": ["ctr_improvement"],
        "requested_output": ["publication_package"],
        "source_system": "test",
    }


def test_fetches_remote_html_when_enabled():
    html = """<html><head><title>取得記事</title></head><body><article>
    <h1>取得記事</h1><p>これはURLから取得した記事本文です。十分な長さを確保するため、説明を追加します。</p>
    <h2>確認方法</h2><p>本文取得後に見出しと文章を解析し、安全な改善提案へ接続します。</p>
    </article></body></html>"""

    def transport(url: str, timeout: float, max_bytes: int) -> FetchedSource:
        return FetchedSource(url, url, 200, "text/html", "utf-8", html, len(html.encode()))

    fetcher = UrlSourceFetcher(transport=transport)
    result = RuntimeOrchestrator(
        REPO_ROOT, source_fetch_enabled=True, source_fetcher=fetcher
    ).execute(_request())
    snapshot = result.artifacts["source_snapshot"]
    source_stage = next(stage for stage in result.stages if stage.name == "source_acquisition")

    assert snapshot["status"] == "available"
    assert snapshot["source_type"] == "remote_url"
    assert snapshot["http_status"] == 200
    assert snapshot["title"] == "取得記事"
    assert "URLから取得した記事本文" in snapshot["normalized_text"]
    assert source_stage.status in {"passed", "passed_with_warning"}


def test_fetch_failure_remains_manual_review_required():
    def transport(url: str, timeout: float, max_bytes: int) -> FetchedSource:
        raise SourceFetchError("simulated timeout")

    result = RuntimeOrchestrator(
        REPO_ROOT,
        source_fetch_enabled=True,
        source_fetcher=UrlSourceFetcher(transport=transport),
    ).execute(_request())
    snapshot = result.artifacts["source_snapshot"]
    source_stage = next(stage for stage in result.stages if stage.name == "source_acquisition")

    assert snapshot["status"] == "missing"
    assert source_stage.status == "manual_review_required"
    assert "simulated timeout" in snapshot["warnings"][0]


def test_private_network_url_is_rejected_before_transport():
    called = False

    def transport(url: str, timeout: float, max_bytes: int) -> FetchedSource:
        nonlocal called
        called = True
        raise AssertionError("transport must not be called")

    fetcher = UrlSourceFetcher(transport=transport)
    with pytest.raises(SourceFetchError, match="not allowed"):
        fetcher.fetch("http://127.0.0.1/private")
    assert called is False


def test_fetch_is_opt_in_and_does_not_change_default_behavior():
    called = False

    def transport(url: str, timeout: float, max_bytes: int) -> FetchedSource:
        nonlocal called
        called = True
        raise AssertionError("transport must not be called")

    result = RuntimeOrchestrator(
        REPO_ROOT,
        source_fetch_enabled=False,
        source_fetcher=UrlSourceFetcher(transport=transport),
    ).execute(_request())
    assert result.artifacts["source_snapshot"]["status"] == "missing"
    assert called is False
