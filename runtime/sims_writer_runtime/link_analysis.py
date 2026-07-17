from __future__ import annotations

import re
from typing import Any


class LinkOpportunityAnalyzer:
    """Select grounded internal-link candidates and separate low-relevance queries.

    The analyzer uses only the supplied article catalog and query set. It never
    claims that a destination page exists unless it is present in the catalog.
    """

    STOPWORDS = {"の", "を", "に", "は", "が", "と", "で", "へ", "や", "から", "まで", "する", "できる", "方法", "設定"}

    def analyze(
        self,
        main_query: str,
        supporting_queries: list[str] | None,
        article_catalog: list[dict[str, Any]] | None,
        *,
        current_url: str | None = None,
    ) -> dict[str, Any]:
        main_tokens = self._tokens(main_query)
        support = self._unique(supporting_queries or [])[:20]
        catalog = article_catalog or []

        scored: list[dict[str, Any]] = []
        for article in catalog:
            url = str(article.get("url") or article.get("target_url") or "").strip()
            if not url or (current_url and url.rstrip("/") == current_url.rstrip("/")):
                continue
            title = str(article.get("title") or article.get("h1") or "").strip()
            query = str(article.get("main_query") or "").strip()
            haystack = self._tokens(" ".join([title, query, " ".join(article.get("queries") or [])]))
            overlap = sorted(main_tokens & haystack)
            support_hits = [q for q in support if self._tokens(q) & haystack]
            score = len(overlap) * 3 + min(len(support_hits), 3)
            if not overlap or score <= 0:
                continue
            scored.append({
                "article_id": article.get("article_id"),
                "url": url,
                "title": title,
                "main_query": query,
                "relevance_score": score,
                "matched_tokens": overlap,
                "matched_queries": support_hits[:5],
                "reason": self._reason(overlap, support_hits),
            })
        scored.sort(key=lambda item: (-item["relevance_score"], item.get("title") or item["url"]))
        internal_links = scored[:8]

        separate: list[dict[str, Any]] = []
        for query in support:
            query_tokens = self._tokens(query)
            overlap_ratio = len(main_tokens & query_tokens) / max(len(main_tokens), 1)
            matched_internal = any(query in item.get("matched_queries", []) for item in internal_links)
            if overlap_ratio < 0.34 and not matched_internal:
                separate.append({
                    "query": query,
                    "reason": "メインクエリとの共通語が少なく、現在の記事へ混在させる根拠が弱い",
                    "relationship": "low_relevance_to_main_query",
                    "recommended_action": "別記事候補として蓄積し、SERP確認後に判断",
                })

        return {
            "analysis_basis": "supplied_article_catalog_and_queries_only",
            "catalog_count": len(catalog),
            "internal_link_candidates": internal_links,
            "separate_article_queries": separate,
            "candidate_count": len(internal_links),
            "separate_query_count": len(separate),
        }

    @classmethod
    def _tokens(cls, value: str) -> set[str]:
        normalized = str(value).lower().replace("　", " ")
        raw = re.findall(r"[a-z0-9]+|[ぁ-んァ-ヶ一-龠ー]{2,}", normalized)
        tokens: set[str] = set()
        for token in raw:
            tokens.update(part for part in re.split(r"[・/\s_-]+", token) if len(part) >= 2 and part not in cls.STOPWORDS)
        return tokens

    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            text = str(value).strip()
            key = text.lower()
            if text and key not in seen:
                result.append(text)
                seen.add(key)
        return result

    @staticmethod
    def _reason(overlap: list[str], support_hits: list[str]) -> str:
        parts: list[str] = []
        if overlap:
            parts.append("主要語一致: " + "、".join(overlap))
        if support_hits:
            parts.append(f"補助クエリ一致: {len(support_hits)}件")
        return " / ".join(parts) or "入力データ上の関連性"
