from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Any


@dataclass(frozen=True)
class QueryIntent:
    query: str
    intent: str
    intent_label: str
    modifiers: list[str]
    topic_tokens: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SearchIntentAnalyzer:
    """Deterministic, evidence-bound search-intent analysis.

    The analyzer uses only the supplied main/supporting queries. It does not
    claim SERP observation or external research.
    """

    INTENT_RULES = (
        ("troubleshooting", "トラブル解決", ("できない", "表示されない", "つながらない", "動かない", "エラー", "原因", "直し方", "対処")),
        ("cost", "費用・料金確認", ("電気代", "料金", "費用", "価格", "いくら", "月額", "年間", "コスト")),
        ("how_to", "方法・設定", ("方法", "やり方", "使い方", "設定", "手順", "変更", "解除", "翻訳")),
        ("comparison", "比較・選択", ("比較", "違い", "どっち", "おすすめ", "選び方", "メリット", "デメリット")),
        ("definition", "意味・基礎理解", ("とは", "意味", "読み方", "なぜ", "仕組み")),
    )

    MODIFIERS = (
        "iphone", "android", "windows11", "windows 11", "mac", "スマホ", "pc",
        "無料", "有料", "つけっぱなし", "年間", "月", "2026", "初心者",
        "できない", "原因", "設定", "方法", "比較", "おすすめ",
    )

    def analyze(self, main_query: str, supporting_queries: list[str] | None = None) -> dict[str, Any]:
        supporting = self._unique(supporting_queries or [])[:20]
        primary = self._classify(main_query)
        analyzed_supporting = [self._classify(query) for query in supporting]
        clusters: dict[str, list[str]] = {}
        for item in analyzed_supporting:
            clusters.setdefault(item.intent, []).append(item.query)

        faq_candidates = self._faq_candidates(supporting, main_query)
        heading_recommendations = self._heading_recommendations(primary, clusters)
        coverage = [primary.intent] + [key for key in clusters if key != primary.intent]
        return {
            "analysis_basis": "supplied_queries_only",
            "primary": primary.to_dict(),
            "supporting": [item.to_dict() for item in analyzed_supporting],
            "intent_clusters": clusters,
            "intent_coverage": coverage,
            "faq_candidates": faq_candidates,
            "heading_recommendations": heading_recommendations,
            "query_count": 1 + len(supporting),
        }

    def _classify(self, query: str) -> QueryIntent:
        normalized = self._normalize(query)
        intent = "informational"
        label = "情報確認"
        for candidate, candidate_label, signals in self.INTENT_RULES:
            if any(signal in normalized for signal in signals):
                intent, label = candidate, candidate_label
                break
        modifiers = [item for item in self.MODIFIERS if item in normalized]
        tokens = [token for token in re.split(r"[\s　/・,_｜|]+", normalized) if token]
        topic_tokens = [token for token in tokens if token not in modifiers]
        return QueryIntent(query=query.strip(), intent=intent, intent_label=label, modifiers=modifiers, topic_tokens=topic_tokens)

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\s+", " ", str(value).strip().lower())

    @classmethod
    def _unique(cls, values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            text = str(value).strip()
            key = cls._normalize(text)
            if text and key not in seen:
                result.append(text)
                seen.add(key)
        return result

    @classmethod
    def _faq_candidates(cls, supporting: list[str], main_query: str) -> list[str]:
        main = cls._normalize(main_query)
        candidates: list[str] = []
        for query in supporting:
            normalized = cls._normalize(query)
            if normalized == main:
                continue
            # Keep concrete long-tail queries and phrase them as questions.
            question = query.strip()
            if not question.endswith(("?", "？")):
                question += "？"
            candidates.append(question)
        return candidates[:5]

    @staticmethod
    def _heading_recommendations(primary: QueryIntent, clusters: dict[str, list[str]]) -> list[str]:
        headings: list[str] = []
        if primary.intent == "cost":
            headings.extend(["費用の結論と目安", "計算方法と条件別の違い", "費用を抑える方法"])
        elif primary.intent == "troubleshooting":
            headings.extend(["最初に確認すること", "主な原因", "原因別の対処法"])
        elif primary.intent == "how_to":
            headings.extend(["結論と事前確認", "具体的な設定手順", "うまくいかない場合の確認点"])
        elif primary.intent == "comparison":
            headings.extend(["違いの結論", "項目別の比較", "目的別の選び方"])
        elif primary.intent == "definition":
            headings.extend(["意味を簡単に説明", "使われる場面", "よくある疑問"])
        else:
            headings.extend(["結論", "詳しい説明", "注意点"])
        if "troubleshooting" in clusters and primary.intent != "troubleshooting":
            headings.append("できない場合の確認点")
        return headings[:4]
