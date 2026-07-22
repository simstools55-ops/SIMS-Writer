# SIMS Platform Guide

Version: 1.1.2  
Status: Production  
Owner: SIMS Writer

## 1. 目的

本書は、SIMS Writerが記事改善を行う際に、公開先プラットフォームの制約をどの段階で受け取り、どの既存契約・Knowledge・Pattern・Quality Ruleへ接続するかを定める実装ガイドである。

本書は新しい品質概念や出力契約を追加しない。既存のProduct Specification、Writing Request Contract、Quality Framework、Publication Package Contractおよび`QF-SIT-003 Platform Format Compliance`を運用可能な形に整理する。

## 2. 適用範囲

対象は次の処理である。

- 既存記事改善
- CTR改善
- 部分修正
- 情報更新
- 公開品質判定
- Claude Projectでの改善回答生成

公開先の例として、はてなブログ、WordPress、Markdown対応CMS、HTML入力型CMSを扱う。ただし、プラットフォーム固有の仕様を推測してはならない。

## 3. 基本原則

1. **内容品質をプラットフォーム都合で劣化させない。** 検索意図、事実性、既存価値の保護を先に確定し、その後に表現形式を適合させる。
2. **入力された制約を優先する。** Writing Requestの`platform`、出力形式、禁止構文、利用可能な装飾情報を正規化して使用する。
3. **不明な仕様を断定しない。** 制約が確認できない場合は、標準Markdownまたはプレーンな構造を用い、warningまたは`unable_to_verify`を残す。
4. **公開先でそのまま利用できる形を目標とする。** 変換作業を利用者へ押し戻さない。
5. **構造と意味を分離する。** 見出し階層、リンク、表、引用、注意書きの意味を維持したまま構文だけを適合させる。

## 4. 入力の扱い

### 4.1 必須ではないが優先して利用する情報

- `platform`
- 希望出力形式（Markdown / HTML / plain text）
- CMS固有の禁止事項
- 利用可能なショートコードまたはブロック
- 既存記事で使用中の記法

### 4.2 入力不足時

プラットフォーム情報がないことだけを理由に処理を停止しない。次の順序でGraceful Degradationを適用する。

1. 既存記事の記法を継承する。
2. 指定出力形式を優先する。
3. どちらも不明な場合は、移植性の高い標準Markdownを使用する。
4. 公開先固有の完全適合を検証できない場合は、その事実をwarningとして残す。

推定したプラットフォーム名を確定値として出力してはならない。

## 5. 実行パイプラインへの接続

| 段階 | 実装責務 |
|---|---|
| Request Normalization | platformと形式制約を正規化し、未指定と推定を区別する |
| Source Content Snapshot | 既存記事の見出し、表、リンク、広告、埋め込み、装飾記法を保護対象として記録する |
| Knowledge Assembly | Shared Editorial KnowledgeとWriter固有Knowledgeを組み立てる。プラットフォーム仕様をShared Knowledgeへ混入させない |
| Content Planning | 内容上必要な構造と、公開先で実現可能な構文を対応づける |
| Pattern Selection | 記事・改善Patternを選択し、構文変換だけを理由に改善範囲を拡大しない |
| Draft Production | 指定形式でBefore/Afterと改善本文を生成する |
| Quality Validation | `QF-SIT-003`を含むSite Fit、Language、Final Publication Gateを実行する |
| Publication Package | そのまま貼り付け可能な本文、変更情報、warningをまとめる |

## 6. 形式別の実装要件

### 6.1 Markdown

- 見出し階層を飛ばさない。
- Before/Afterは製品で合意済みのMarkdown表現を使用する。
- 生HTMLを前提にしない。
- 表が長大になる場合は可読性を優先し、必要に応じて段落または箇条書きへ変換する。

### 6.2 HTML

- 指定がある場合のみHTMLを主形式とする。
- 不要なインラインスタイル、スクリプト、イベント属性を生成しない。
- CMSが除去する可能性の高い構文を、確認なしに必須要素として使わない。
- 見出し、段落、リスト、表、リンクの意味構造を優先する。

### 6.3 プレーンテキスト

- 見出し名と段落境界を明確にする。
- HTMLタグやMarkdown記号を混在させない。
- URLとアンカーテキストの対応を判読できる形にする。

## 7. プラットフォーム適合と既存価値の保護

次の要素は、形式変換時にもPreservation対象として扱う。

- 広告・アフィリエイトリンク
- 商品リンク
- 比較表
- 体験談・独自レビュー
- 注意書き・免責
- 内部リンク
- 画像・埋め込みの位置関係
- 記事固有の結論

適合のために削除または置換が必要な場合は、黙って消さず、変更理由と影響を明示する。

## 8. Quality Gate

公開可能と判定するには、少なくとも次を満たす。

- 指定形式と実出力が一致している。
- 見出し階層、リンク、表、引用が破損していない。
- 未対応構文や公開先で壊れる構文を含まない。
- 既存価値の保護方針と変更フラグが一致している。
- 検証不能なプラットフォーム固有仕様がwarningとして可視化されている。

重大な形式破損は`QF-SIT-003`のfailとし、Final Publication Gateを通過させない。

## 9. Shared Repositoryとの境界

Shared Editorial Knowledgeは、検索意図、証拠、読者不安、FAQ、内部リンク意味論など製品横断の編集知識を保持する。

次はWriter側の責務であり、Shared Repositoryへ正本を置かない。

- CMS別の構文選択
- WriterのBefore/After表示形式
- WriterのPublication Package
- Writer固有のQuality Gate接続
- Writer固有のClaude Project出力制約

Shared Repositoryには、Writerが共通知識をどの段階で利用するかというapplication mappingのみを保持する。

## 10. Claude Projectへの適用

Claude Projectは回答生成前に次の順序で確認する。

1. `CLAUDE_PROJECT_INSTRUCTIONS.md`
2. `product/quality/QUALITY_FRAMEWORK.md`
3. 本書
4. `product/roadmap/WRITER_v1.1.2_IMPROVEMENT_PLAN.md`
5. Knowledge PackおよびShared Knowledge snapshot

プラットフォーム情報が不足していても、回答全体を停止せず、利用可能な形式で完成させる。

## 11. 非対象

- CMSのAPI実装
- テーマやプラグインの自動判定
- 公開操作の自動実行
- 未確認のCMS仕様の追加
- Shared Editorial Knowledgeへのプラットフォーム固有ルール移管
