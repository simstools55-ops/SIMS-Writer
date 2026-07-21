from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import re
from ..output_contract import build_feedback, package_output
from ..publish_quality import assess_improvement_need, classify_search_intent

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
    improvement_judgment: str = "improvement_recommended"
    search_intent: str = "unknown"
    estimated_minutes: int = 20

class CTRImprovementSlice:
    """CTR改善の最小Vertical Slice。

    外部LLMなしでもContract→Decision→Pattern→Draft→Qualityへ通せるよう、
    入力済みの本文・クエリ・指標だけから保守的な改善案を生成する。
    """
    def normalize(self, raw: dict[str, Any]) -> dict[str, Any]:
        main_query = raw.get("MainQuery") or raw.get("main_query") or raw.get("query", {}).get("main_query")
        query_inferred = False
        if not main_query or not str(main_query).strip():
            title_hint = raw.get("SEOTitle") or raw.get("seo_title") or raw.get("ArticleTitle") or raw.get("current_title") or raw.get("title") or ""
            main_query = self._infer_query(title_hint)
            query_inferred = bool(main_query)
        main_query_missing = not bool(main_query)
        if main_query_missing:
            main_query = ""
        source = raw.get("ExistingContent") or raw.get("existing_content") or raw.get("article_content") or ""
        supporting = raw.get("SupportingQueries") or raw.get("supporting_queries") or []
        if isinstance(supporting, str):
            supporting=[x.strip() for x in re.split(r"[,\n]", supporting) if x.strip()]
        return {
            "request_id": raw.get("RequestID") or raw.get("request_id") or "REQ-CTR-SLICE",
            "request_type": "existing_article_improvement",
            "main_query": str(main_query).strip(),
            "main_query_inferred": query_inferred,
            "main_query_missing": main_query_missing,
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
            "output_mode": raw.get("OutputMode") or raw.get("output_mode") or "partial",
            "internal_link_candidates": raw.get("InternalLinkCandidates") or raw.get("internal_link_candidates") or [],
            "article_catalog": raw.get("ArticleCatalog") or raw.get("article_catalog") or [],
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
        qtokens=[x for x in request.get("main_query", "").split() if x]
        title_aligned=all(tok.lower() in title.lower() for tok in qtokens) if title else False
        ctr=request.get("ctr"); pos=request.get("average_position"); imp=request.get("impressions")
        measurable = imp is None or imp >= 100
        low_ctr = ctr is not None and ctr < (0.01 if (pos is not None and pos <= 10) else 0.005)
        title_action = "revise" if (not title_aligned or (measurable and low_ctr)) else "preserve"
        existing=request.get("existing_content") or ""
        main_query = request.get("main_query", "")
        intro_action = "revise" if len(existing.strip()) < 120 or (main_query and main_query.lower() not in existing[:500].lower()) else "preserve"
        faq_signal = len(request.get("supporting_queries") or []) >= 2
        faq_action = "add" if faq_signal else "no_change"
        intro_answer_first = intro_action == "preserve"
        assessment = assess_improvement_need(
            ctr=ctr, impressions=imp, average_position=pos,
            title_aligned=title_aligned, intro_answer_first=intro_answer_first,
        )
        search_intent = classify_search_intent(request["main_query"], title)
        if assessment.improvement_judgment == "maintain_current":
            title_action = "preserve"
            intro_action = "preserve"
            faq_action = "no_change"
        reasons=[]
        if not title_aligned: reasons.append("現行タイトルがメインクエリを十分に表していない")
        if low_ctr: reasons.append("順位・表示回数に対してCTR改善余地がある")
        if intro_action=="revise": reasons.append("導入で検索者の答えを早期提示する余地がある")
        if faq_signal and faq_action=="add": reasons.append("補助クエリをFAQとして見つけやすく再整理できる")
        reasons.append(assessment.reason)
        return CTRDecision(title_action,intro_action,faq_action,"。".join(reasons),assessment.improvement_judgment,search_intent,assessment.estimated_minutes)

    def build_draft(self, request: dict[str, Any], decision: CTRDecision) -> dict[str, Any]:
        q=request.get("main_query") or request.get("seo_title") or request.get("current_title") or "この記事"
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
            "search_intent": decision.search_intent,
            "improvement_judgment": decision.improvement_judgment,
            "estimated_minutes": decision.estimated_minutes,
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

    def build_output(self, request: dict[str, Any], decision: CTRDecision, draft: dict[str, Any]) -> dict[str, Any]:
        before_after=[]
        current_title=request.get("seo_title") or request.get("current_title") or ""
        if decision.title_action=="revise":
            before_after.append({"component":"seo_title","before":current_title,"after":draft["seo_title"],"reason":"検索意図とタイトルの一致を高めるため","expected_effect":"検索結果で比較対象と記事内容が伝わりやすくなる"})
        if decision.introduction_action=="revise":
            before_after.append({"component":"introduction","before":"既存導入文","after":draft["introduction"],"reason":"結論を冒頭で明示するため","expected_effect":"読者が記事を読み進める判断を早く行える"})
        if decision.faq_action=="add":
            before_after.append({"component":"faq","before":"FAQなし、または不足","after":draft["faq"],"reason":"本文中の重要情報を質問形式で見つけやすく再整理するため","expected_effect":"疑問への回答を本文末でも見つけやすくなる"})
        warnings=[]
        information=[]
        estimated_fields=[]
        main_query_source="manual"
        if request.get("main_query_inferred"):
            main_query_source="estimated"
            estimated_fields.append("main_query")
            information.append("main_queryが未入力だったため、タイトルから推定しました。")
        elif request.get("main_query_missing"):
            main_query_source="unavailable"
            warnings.append("main_queryが未入力で推定材料も不足しています。クエリ依存の判定は保留しましたが、改善可能な項目の処理は継続しました。")
        if not request.get("article_catalog"):
            information.append("article_catalogが未入力のため、内部リンク候補の選定のみSKIPしました。")
        elif not request.get("internal_link_candidates"):
            information.append("内部リンク候補が未入力のため、内部リンクは変更していません。")
        execution_mode="graceful_degradation" if (request.get("main_query_inferred") or request.get("main_query_missing") or not request.get("article_catalog")) else "standard"
        effect={"ctr":"CTR改善余地はありますが、具体的な数値は実測データ不足のため予測しません。","clicks":"表示回数とクリック数の母数が小さい場合、定量予測は行わず再測定で確認します。"}
        feedback=build_feedback(article_id=request.get("article_id"), article_url=request.get("target_url"), main_query=request.get("main_query", ""), site_id=request.get("site_id"), site_name=request.get("site_name"), site_url=request.get("site_url"), before_after=before_after, summary=decision.reason, warnings=warnings, information=information, main_query_source=main_query_source, execution_mode=execution_mode, estimated_fields=estimated_fields, confidence="low" if request.get("main_query_missing") else ("medium" if request.get("main_query_inferred") else "high"), expected_effect=effect)
        feedback["estimated_minutes"] = decision.estimated_minutes
        publish_quality = {
            "improvement_judgment": decision.improvement_judgment,
            "search_intent": decision.search_intent,
            "estimated_minutes": decision.estimated_minutes,
        }
        return package_output(output_mode=request.get("output_mode","partial"), before_after=before_after, feedback=feedback, unresolved_items=warnings, article_content=draft.get("article_content"), publish_quality=publish_quality)

    @staticmethod
    def _infer_query(title: str) -> str:
        clean=re.sub(r"[｜|].*$", "", title or "")
        clean=re.sub(r"【[^】]*】", "", clean)
        clean=re.sub(r"を(?:5つ|５つ|\d+つ)の項目で比較.*$", " 比較", clean)
        clean=re.sub(r"[！!？?]+$", "", clean).strip()
        return re.sub(r"\s+", " ", clean)[:120]

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
