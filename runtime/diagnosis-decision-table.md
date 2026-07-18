# Search Diagnosis Decision Table v1.0

## 1. 基本閾値

閾値は絶対判定ではなく、初期判定の目安として使用する。

### サンプル量

| 状態 | 目安 | 扱い |
|---|---:|---|
| 極小 | 表示49以下 | 原則LOW_SAMPLE |
| 小 | 表示50〜199 | 慎重判定 |
| 中 | 表示200〜999 | 通常判定可能 |
| 大 | 表示1,000以上 | 高信頼判定候補 |

クリック数が0〜2件の場合は、表示回数が多くてもCTR原因の断定を弱める。

### 順位帯別CTRの初期目安

| 順位帯 | 低い可能性 | 標準域の目安 | 良好の可能性 |
|---|---:|---:|---:|
| 1〜3位 | 5%未満 | 5〜20% | 20%以上 |
| 3.1〜5位 | 3%未満 | 3〜10% | 10%以上 |
| 5.1〜10位 | 1.5%未満 | 1.5〜6% | 6%以上 |
| 10.1〜20位 | 1%未満 | 1〜3% | 3%以上 |
| 20位以下 | CTR単独評価を避ける | ― | ― |

クエリの種類、SERP機能、ブランド性、季節性によって大きく変動するため、数値だけで最終診断しない。

## 2. 優先判定表

| 条件 | Primary Diagnosis | 原則対応 |
|---|---|---|
| 入力値に重大矛盾 | DATA_INCONSISTENT | 再取得・確認 |
| 表示49以下 | LOW_SAMPLE | monitor |
| 順位20位以下 | LOW_VISIBILITY | 内容・意図・競合確認 |
| 順位10.1〜20位 | POSITION_GAP | 検索意図・本文強化 |
| 順位10位以内かつCTR低位 | CTR_OPPORTUNITY | タイトル・導入・スニペット確認 |
| 順位5位以内かつCTR標準以上 | HEALTHY | 原則維持 |
| 上位クエリの意図が分散 | INTENT_FRAGMENTATION | 記事焦点を確認 |
| main_queryと記事内容が不一致 | INTENT_MISMATCH | 構成再設計 |
| 前期間比で継続悪化 | TREND_DECLINE | 変化要因確認 |
| 時期依存が強い | SEASONAL_VARIATION | 季節調整・monitor |
| S/Aランクで良好値 | PROTECT_WINNER | 変更最小化 |
| Dランクかつ低順位・低CTR | REBUILD_CANDIDATE | 全体再設計候補 |

## 3. 複合条件

### CTR低下＋低順位

```text
順位18位、CTR0.4%
```

Primary：POSITION_GAP  
Secondary：CTR_OPPORTUNITY

タイトルだけを主改善にしない。

### 高順位＋低CTR

```text
順位3.5位、表示2,000、CTR1.2%
```

Primary：CTR_OPPORTUNITY

検索意図とタイトル表現の一致、競合スニペット、記事タイトルを確認する。

### 低表示＋高CTR

```text
表示40、CTR12%
```

Primary：LOW_SAMPLE  
Secondary：HEALTHY_SIGNAL

過剰修正しない。

### 主クエリだけ高CTR

記事全体CTRが低くても、main_queryのCTRが高い場合は、タイトル問題と断定しない。

Primary候補：

- QUERY_MIX_EFFECT
- INTENT_FRAGMENTATION
- LOW_RELEVANCE_QUERY_EXPOSURE

### S/A記事の短期変動

過去比較データがない場合、TREND_DECLINEと断定しない。

Primary：PROTECT_WINNERまたはMONITOR
