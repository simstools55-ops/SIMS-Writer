# Search Console Query Data Analysis

Version: 1.2.0

## Purpose
最大200件のSearch Console生クエリを、記事改善・内部リンク・別記事候補の判断材料として利用する。生データは保持し、意味解析による統合結果と混同しない。

## Coverage confidence
- `HIGH_COVERAGE`: Coverage 80%以上。主要需要を概ね代表するが完全網羅とは断定しない。
- `MEDIUM_COVERAGE`: 50%以上80%未満。QUERY MIX、CONTENT GAPは推定を含む。
- `LOW_COVERAGE`: 50%未満。記事全体の意図を代表すると断定しない。
- `COVERAGE_UNKNOWN`: 算出不能。取得範囲内のみで判断する。

## Analysis sequence
1. 元クエリと指標を保持する。
2. 表記ゆれを分析上のみ正規化する。
3. 意味の近いクエリをクラスタ化する。
4. 各クラスタを `STRENGTHEN_EXISTING_CONTENT` / `ADD_INTERNAL_LINK` / `CREATE_SEPARATE_ARTICLE` / `MONITOR_ONLY` / `IGNORE_AS_NOISE` に分類する。
5. Coverage、本文一致、需要規模、Evidence Strengthを加味して確信度を調整する。

## Evidence boundary
未取得クエリの内容、ユーザー行動、カニバリ発生を推測で確定しない。Search Console Query Dataだけでは他記事との競合を証明できないため、「可能性」「候補」「確認推奨」と表現する。

## Winner protection
順位・CTRが強い主要クエリとタイトルは保護する。周辺意図にはFAQ、見出し、内部リンク、別記事の順で対応を検討し、タイトル変更は最後の選択肢とする。
