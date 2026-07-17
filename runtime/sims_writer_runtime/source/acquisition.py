from __future__ import annotations

from dataclasses import replace

from .extractor import ArticleSourceExtractor, SourceSnapshot
from .fetcher import SourceFetchError, UrlSourceFetcher


class ArticleSourceAcquisition:
    """Prefer supplied content; optionally fetch target URL when content is absent."""

    def __init__(self, extractor: ArticleSourceExtractor | None = None, fetcher: UrlSourceFetcher | None = None):
        self.extractor = extractor or ArticleSourceExtractor()
        self.fetcher = fetcher or UrlSourceFetcher()

    def acquire(
        self,
        content: str | None,
        *,
        content_format: str,
        target_url: str | None,
        fallback_title: str,
        fetch_enabled: bool,
    ) -> SourceSnapshot:
        supplied = self.extractor.extract(
            content,
            content_format=content_format,
            target_url=target_url,
            fallback_title=fallback_title,
        )
        if supplied.status != "missing" or not fetch_enabled or not target_url:
            return supplied
        try:
            fetched = self.fetcher.fetch(target_url)
            snapshot = self.extractor.extract(
                fetched.body,
                content_format="html" if fetched.content_type.startswith("text/html") else "plain_text",
                target_url=fetched.final_url,
                fallback_title=fallback_title,
            )
            return replace(
                snapshot,
                source_type="remote_url",
                requested_url=fetched.requested_url,
                final_url=fetched.final_url,
                http_status=fetched.status_code,
                media_type=fetched.content_type,
                byte_count=fetched.byte_count,
            )
        except SourceFetchError as exc:
            return replace(
                supplied,
                source_type="remote_url",
                warnings=[f"URL source acquisition failed: {exc}"],
            )
