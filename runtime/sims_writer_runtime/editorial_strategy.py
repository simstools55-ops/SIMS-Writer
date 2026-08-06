from __future__ import annotations
from copy import deepcopy
from typing import Any

STRATEGY_CTR = "CTR_PRESENTATION"
STRATEGY_SERP_GAP = "SERP_GAP_COMPLETION"
STRATEGY_INTENT_REALIGN = "SEARCH_INTENT_REALIGNMENT"
STRATEGY_CONTENT_DEPTH = "CONTENT_DEPTH_AND_EVIDENCE"
STRATEGY_PRESERVE = "PRESERVE_AND_MONITOR"
STRATEGY_SEPARATE = "SEPARATE_INTENT_ARTICLE"


def select_editorial_strategy(context: dict[str, Any]) -> dict[str, Any]:
    """Convert observed problem -> likely cause -> bounded editing strategy.

    This is internal-only. It never exposes scores or diagnostic codes to users.
    """
    c=deepcopy(context or {})
    rank=float(c.get("average_position") or 999)
    impressions=int(c.get("impressions") or 0)
    ctr=float(c.get("ctr") or 0)
    intent_match=str(c.get("intent_match") or "unknown").lower()
    gap_count=int(c.get("supported_gap_count") or 0)
    separate=bool(c.get("separate_intent"))
    content_complete=bool(c.get("content_complete"))

    if separate:
        strategy=STRATEGY_SEPARATE; cause="副次検索意図が現在の記事の主題から独立している"
    elif intent_match == "mismatch":
        strategy=STRATEGY_INTENT_REALIGN; cause="記事の中心回答と現在の検索意図が一致していない"
    elif rank <= 3 and impressions >= 100 and ctr < 0.02:
        strategy=STRATEGY_CTR; cause="上位表示されているが検索結果上の訴求が弱い"
    elif rank > 3 and gap_count > 0:
        strategy=STRATEGY_SERP_GAP; cause="上位結果と比較して根拠のある重要回答が不足している"
    elif rank > 10 and not content_complete:
        strategy=STRATEGY_CONTENT_DEPTH; cause="順位改善に必要な回答の具体性または根拠が不足している"
    else:
        strategy=STRATEGY_PRESERVE; cause="大きな欠落が確認できず、既存資産の保全が優先される"

    labels={
      STRATEGY_CTR:"検索結果で内容が伝わりやすくなるよう整えました。",
      STRATEGY_SERP_GAP:"検索意図に対して不足していた回答を補う方針で編集しました。",
      STRATEGY_INTENT_REALIGN:"検索意図と記事の中心回答をそろえる方針で編集しました。",
      STRATEGY_CONTENT_DEPTH:"順位改善に必要な説明と根拠を補う方針で編集しました。",
      STRATEGY_PRESERVE:"良い部分を残し、必要な箇所だけを整えました。",
      STRATEGY_SEPARATE:"現在の記事を守り、別記事に分けるべき疑問は混在させませんでした。",
    }
    return {
      "primary_problem": _problem(rank, impressions, ctr),
      "primary_cause": cause,
      "strategy": strategy,
      "user_strategy_message": labels[strategy],
      "allowed_components": _allowed(strategy),
      "reason_trace": {
        "average_position": rank, "impressions": impressions, "ctr": ctr,
        "intent_match": intent_match, "supported_gap_count": gap_count,
      }
    }


def attach_strategy(changes:list[dict[str,Any]], strategy:dict[str,Any])->list[dict[str,Any]]:
    out=[]
    allowed=set(strategy.get("allowed_components") or [])
    for raw in changes:
        item=deepcopy(raw)
        item["editorial_strategy"]=strategy.get("strategy")
        if allowed and item.get("component") not in allowed and not item.get("change_basis") in {"mechanical","accuracy","consistency","usability"}:
            item["internal_reject"]=True
            item["strategy_rejection_reason"]="選択された編集戦略の範囲外"
        out.append(item)
    return out


def _problem(rank:float, impressions:int, ctr:float)->str:
    if rank>10: return "SEARCH_VISIBILITY"
    if rank>3: return "RANKING_OPPORTUNITY"
    if impressions>=100 and ctr<0.02: return "CTR_OPPORTUNITY"
    return "PRESERVATION_PRIORITY"

def _allowed(strategy:str)->list[str]:
    return {
      STRATEGY_CTR:["seo_title","meta_description","introduction"],
      STRATEGY_SERP_GAP:["seo_title","meta_description","introduction","headings","faq","body","images"],
      STRATEGY_INTENT_REALIGN:["seo_title","meta_description","introduction","headings","body","faq"],
      STRATEGY_CONTENT_DEPTH:["introduction","headings","body","faq","images"],
      STRATEGY_PRESERVE:["seo_title","meta_description","introduction"],
      STRATEGY_SEPARATE:[],
    }.get(strategy,[])
