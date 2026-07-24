from __future__ import annotations

TERM_LABELS = {
    "IMPROVEMENT_RECOMMENDED": "改善推奨",
    "MINOR_IMPROVEMENT": "軽微な改善",
    "KEEP_CURRENT": "現状維持",
    "POSITION_OPPORTUNITY": "掲載順位を生かしたクリック改善機会",
    "LOW_SAMPLE": "データ不足",
    "QUERY_MIX_EFFECT": "複数の検索意図が混在する影響",
    "Intent Gap": "検索意図とのずれ",
    "Query Coverage": "取得クエリの網羅率",
    "Winner Query Preservation": "好調クエリの保護",
    "Publication QA": "公開前品質確認",
}

def user_facing_term(code: str, first_use: bool = True) -> str:
    label = TERM_LABELS.get(code, code)
    return f"{label}（{code}）" if first_use and label != code else label
