from __future__ import annotations

TERM_LABELS = {
    "IMPROVEMENT_RECOMMENDED": "改善推奨",
    "MINOR_IMPROVEMENT": "軽微な改善",
    "KEEP_CURRENT": "現状維持",
    "POSITION_OPPORTUNITY": "掲載順位を生かしたクリック改善機会",
    "LOW_SAMPLE": "データ不足",
    "LOW_COVERAGE": "取得範囲が限定的",
    "INPUT_INCOMPLETE": "入力情報不足",
    "QUERY_MIX_EFFECT": "複数の検索意図が混在する影響",
    "Intent Gap": "検索意図とのずれ",
    "Query Coverage": "取得クエリの網羅率",
    "Winner Query Preservation": "成果が出ている主要クエリの保護",
    "PROTECT_WINNER": "成果が出ている要素の保護",
    "Publication QA": "公開前品質確認",
    "Change Budget": "変更量の上限",
    "Preservation Score": "既存内容の維持率",
    "Internal Link Semantics": "内部リンクの意味的関連性",
    "FAQ Evolution": "FAQの重複整理",
    "SERP Entity Preservation": "検索結果で守るべき主要語",
    "graceful_degradation": "情報不足時の保守的処理",
    "monitor": "経過観察",
}

def user_facing_term(code: str, first_use: bool = True) -> str:
    label = TERM_LABELS.get(code, code)
    return f"{label}（{code}）" if first_use and label != code else label
