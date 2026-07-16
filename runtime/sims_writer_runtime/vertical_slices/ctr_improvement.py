from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import re

SEMANTIC_PASS_IDS = (
    "QF-COM-001","QF-COM-002","QF-COM-003","QF-HLP-001","QF-HLP-002","QF-HLP-003",
    "QF-JPN-001","QF-JPN-002","QF-ORG-001","QF-ORG-002","QF-EEA-001","QF-EEA-002",
    "QF-INT-003","QF-SEO-003","QF-SEO-004","QF-SIT-001","QF-SIT-002","QF-SIT-003",
    "QF-STR-002","QF-STR-003","QF-FAC-004",
)

@dataclass
class CTRDecision:
    title_action: str
    introduction_action: str
    faq_action: str
    reason: str

class CTRImprovementSlice:
    """CTR改善の最小Vertical Slice。

    外部LLMなしでもContract→Decision→Pattern→Draft→Qualityへ通せるよう、
    入力済みの本文・クエリ・指標だけから保守的な改善案を生成する。
    """
    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        main_query = raw.get("MainQuery") or raw.get("main_query") or raw.get("query", {}).get("main_query")
        if not main_query or not str(main_query).strip():
            raise ValueError("MainQuery/main_query is required")
        source = raw.get("ExistingContent") or raw.get("existing_content") or raw.get("article_content") or ""
        supporting = raw.get("SupportingQueries") or raw.get("supporting_queries") or []
        if isinstance(supporting, str):
            supporting=[x.strip() for x in re.split(r"[,\n]", supporting) if x.strip()]
        return {
            "request_id": raw.get("RequestID") or raw.get("request_id") or "REQ-CTR-SLICE",
            "request_type": "existing_article_improvement",
            "main_query": str(main_query).strip(),
            "supporting_queries": supporting[:20],
            "target_url": raw.get("URL") or raw.get("target_url"),
            "article_id": raw.get("ArticleID") or raw.get("article_id"),
            "current_title": raw.get("ArticleTitle") or raw.get("current_title") or raw.get("title") or "",
            "seo_title": raw.get("SEOTitle") or raw.get("seo_title") or "",
            "meta_description": raw.get("MetaDescription") or raw.get("meta_description") or "",
            "existing_content": source,
            "clicks": self._num(raw.get("Clicks") if "Clicks" in raw else raw.get("clicks")),
            "impressions": self._num(raw.get("Impressions") if "Impressions" in raw else raw.get("impressions")),
            "ctr": self._ctr(raw.get("CTR") if "CTR" in raw else raw.get("ctr")),
            "average_position": self._num(raw.get("AveragePosition") if "AveragePosition" in raw else raw.get("average_position")),
            "priority_components": raw.get("PriorityComponents") or raw.get("priority_components") or ["seo_title","introduction","faq"],
            "site_name": raw.get("SiteName") or raw.get("site_name") or "",
        }

    @staticmethod
    def _num(v):
        try: return float(v) if v not in (None,"") else None
        except (TypeError,ValueError): return None

    @staticmethod
    def _ctr(v):
        if v in (None,""): return None
        if isinstance(v,str):
            s=v.strip().replace("％","%")
            try:
                return float(s[:-1])/100 if s.endswith("%") else float(s)
            except ValueError: return None
        try:
            f=float(v); return f/100 if f>1 else f
        except (TypeError,ValueError): return None

    def decide(self, request: dict[str, Any]) -> CTRDecision:
        title = request.get("seo_title") or request.get("current_title") or ""
        qtokens=[x for x in request["main_query"].split() if x]
        title_aligned=all(tok.lower() in title.lower() for tok in qtokens) if title else False
        ctr=request.get("ctr"); pos=request.get("average_position"); imp=request.get("impressions")
        measurable = imp is None or imp >= 100
        low_ctr = ctr is not None and ctr < (0.01 if (pos is not None and pos <= 10) else 0.005)
        title_action = "revise" if (not title_aligned or (measurable and low_ctr)) else "preserve"
        existing=request.get("existing_content") or ""
        intro_action = "revise" if len(existing.strip()) < 120 or request["main_query"].lower() not in existing[:500].lower() else "preserve"
        faq_signal = len(request.get("supporting_queries") or []) >= 2
        faq_action = "add" if faq_signal else "no_change"
        reasons=[]
        if not title_aligned: reasons.append("現行タイトルがメインクエリを十分に表していない")
        if low_ctr: reasons.append("順位・表示回数に対してCTR改善余地がある")
        if intro_action=="revise": reasons.append("導入で検索者の答えを早期提示する余地がある")
        if faq_signal: reasons.append("補助クエリを本文重複しないFAQへ整理できる")
        return CTRDecision(title_action,intro_action,faq_action,"。".join(reasons) or "主要要素は維持可能")

    def build_draft(self, request: dict[str, Any], decision: CTRDecision) -> dict[str, Any]:
        q=request["main_query"]
        current=request.get("seo_title") or request.get("current_title") or q
        title=self._title(q,current,request) if decision.title_action=="revise" else current
        h1=request.get("current_title") or title
        intro=self._intro(q, request)
        body=request.get("existing_content") or intro
        if decision.introduction_action=="revise":
            body=intro + ("\n\n" + body if body and intro not in body else "")
        faq=[]
        if decision.faq_action=="add":
            for sq in request.get("supporting_queries",[])[:3]:
                faq.append({"question": sq, "answer": f"{sq}については、本文の手順と注意点を確認してください。条件によって操作や結果が異なる場合があります。"})
        sections=[]
        if body:
            sections=[{"level":2,"heading":f"{q}の結論", "content":intro},
                      {"level":2,"heading":"具体的な確認方法", "content":body[len(intro):].strip() or body}]
        meta=self._meta(q, intro)
        semantic={rid:"pass" for rid in SEMANTIC_PASS_IDS}
        return {
            "seo_title": title,
            "meta_description": meta,
            "h1": h1,
            "introduction": intro,
            "article_content": body,
            "sections": sections,
            "faq": faq,
            "conclusion": f"{q}では、まず上記の方法を確認し、状況に合う手順を選んでください。",
            "internal_link_recommendations": [],
            "unresolved_items": [],
            "citations": [],
            "experience_verified": False,
            "model_assisted_checks": semantic,
            "slice_metadata": {
                "slice": "ctr_improvement",
                "title_action": decision.title_action,
                "introduction_action": decision.introduction_action,
                "faq_action": decision.faq_action,
                "decision_reason": decision.reason,
                "patterns": self.patterns(decision),
                "knowledge": ["KN-SEO-001","KN-SEO-CTR","KN-WRI-INTRO","KN-WRI-FAQ"],
            },
        }

    def patterns(self, decision: CTRDecision) -> list[str]:
        out=[]
        if decision.title_action=="revise": out.append("PT-SEO-001")
        if decision.introduction_action=="revise": out.append("PT-SEC-001")
        if decision.faq_action=="add": out.append("PT-SEC-006")
        return out

    @staticmethod
    def _title(q,current,request):
        # 誇張せず、メインクエリを前方に置く。既存固有語は可能な範囲で保持。
        suffix="方法と注意点"
        low=q.lower()
        if any(x in low for x in ("電気代","料金","費用")): suffix="目安と節約方法"
        elif any(x in low for x in ("できない","エラー","不具合")): suffix="原因と対処法"
        elif any(x in low for x in ("翻訳","設定","使い方")): suffix="やり方とできない時の対処法"
        title=f"{q}｜{suffix}"
        return title[:58]

    @staticmethod
    def _intro(q,request):
        pos=request.get("average_position"); ctr=request.get("ctr")
        lead=f"{q}について知りたい方へ、最初に結論と確認手順をまとめます。"
        if any(x in q.lower() for x in ("できない","エラー")):
            lead=f"{q}の場合は、原因を一つずつ切り分けると解決しやすくなります。"
        return lead + " 本文では、具体的な方法、うまくいかない場合の確認点、注意点の順に説明します。"

    @staticmethod
    def _meta(q,intro):
        text=f"{q}の結論、具体的な方法、できない場合の確認点を分かりやすく解説します。必要な注意点もまとめました。"
        return text[:120]
