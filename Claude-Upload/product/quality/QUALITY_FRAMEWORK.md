# SIMS Writer Quality Framework

Version: 1.2.0  
Status: Production  
Owner: SIMS Writer

## 1. 目的

本書は、SIMS Writerに既に実装されているQuality Dimension、Quality Rule、Quality Gate、Scoring、Warning、Contract、Validationを一つの運用品質体系として定義する。

新しい品質基準は追加しない。Product Specification v1.0、Quality Foundation、Publish Ready Definition、Quality Dimension、各Gate、各Contractおよび実記事回帰で確定した運用ルールを統合する。

## 2. 品質の定義

SIMS Writerにおける品質とは、文章の読みやすさだけではない。次の条件を同時に満たし、利用者が安全に公開判断できる状態をいう。

- 検索意図へ明確に答えている。
- 事実と根拠の関係が追跡できる。
- 既存記事の実績・独自価値を不必要に壊していない。
- 変更範囲が診断と一致している。
- 日本語として自然で、公開先に適合している。
- 出力本文、変更フラグ、JSON、warningが相互に矛盾しない。
- 検証不能事項と人手確認事項が隠されていない。

## 3. Quality Dimensions

Product Specificationで定義済みの次元を正式な評価軸とする。

1. Safety
2. Factuality
3. Search Intent
4. Completeness
5. Helpfulness
6. SEO
7. Structure
8. Readability
9. Japanese Quality
10. EEAT Support
11. Original Value
12. Site Fit
13. Publication Readiness

特定の次元だけが高くても、重大なSafety、Factuality、Contract、Publication Readiness違反を相殺できない。

## 4. 品質レイヤー

### 4.1 Foundation

Quality Foundationは、実記事運用で再発しやすい診断・整合性・出力Contractの最低条件を扱う。

- Improvement Type
- Confidence
- Execution Mode
- Next Action
- Change Flags
- LOW_SAMPLEを含むwarning運用
- Canonical JSON

### 4.2 Rules

Quality Ruleは単一の検証可能な要求である。各RuleはID、次元、重大度、pass/fail/warning条件、auto-fix可否、manual review要否を持つ。

Ruleをプロンプトだけに記述して正本化してはならない。正本は`quality/rules/`とregistryで管理する。

### 4.3 Gates

Quality Gateは工程ごとの通過判定である。

| Gate | 主な確認 |
|---|---|
| Input | 必須入力、識別情報、推定値、Graceful Degradation |
| Planning | Primary Intent、Main Answer、Scope、Preservation、Change Budget |
| Evidence | 中心主張、数値、更新性、出典範囲、検証不能事項 |
| Draft | 完成性、構造、既存価値、変更範囲 |
| SEO | タイトル・本文整合、クエリ自然使用、検索意図、内部リンク |
| Language | 日本語自然性、冗長性、機械的表現、表記整合 |
| Final Publication | 全Contract、全重大Rule、出力間整合、公開可能性 |

Gateは順序どおりに評価し、上流の重大failを下流の文章修正だけで解消したことにしてはならない。

### 4.4 Contracts

Contractは品質結果を機械判読可能に固定する。

- Request Contract
- Source Content Contract
- Knowledge Assembly Contract
- Content Plan Contract
- Pattern Selection Contract
- Content Draft Contract
- Quality Report Contract
- Decision Record / Action Plan Contract
- Publication Package Contract
- Execution Record / Error Contract
- SIMS Feedback JSON Contract

Canonical JSONは一つだけを出力し、本文と異なる変更内容を記録してはならない。

## 5. 品質判定の順序

1. 入力と識別情報を正規化する。
2. Search ConsoleデータをLOW_SAMPLEを含めて診断する。
3. Primary IntentとMain Answerを確定する。
4. 既存価値と保護対象を特定する。
5. Change Budget、Rewrite Level、Rewrite Scopeを決定する。
6. 必要なEvidenceを確認する。
7. Knowledge SetとPattern Setを選択する。
8. Draftを生成する。
9. Quality RuleとGateを実行する。
10. Targeted Refinementで局所修正する。
11. Publication PackageとCanonical JSONの整合を監査する。
12. publish / warning / manual review / no changeを決定する。

## 6. 診断と変更範囲

### 6.1 Preservation first

既存記事改善では、良い部分を特定する前に全面改稿を開始しない。広告、商品リンク、比較表、体験談、独自レビュー、既存結論、検索流入を支える要素を保護候補として扱う。

### 6.2 Change Budget

Change Budgetは、改善効果の期待値ではなく、既存価値を守りながら変更してよい範囲を示す。変更箇所は診断根拠と対応しなければならない。

### 6.3 Rewrite Level / Scope

局所修正で解決できる場合は局所修正を優先する。全面改稿は、検索意図の重大な不一致、構造破綻、事実性リスク、記事統合など、既存ルールが認める場合に限る。

### 6.4 LOW_SAMPLE

表示回数やクリック数が少ない場合、CTRや順位だけで強い結論を出さない。LOW_SAMPLEは改善停止理由ではなく、confidenceと期待表現を抑制する信号として扱う。

## 7. Evidence Quality

- 中心主張を優先して検証する。
- 更新性の高い情報は時点を確認する。
- 数値には根拠または計算基準を持たせる。
- 事実、推定、編集上の意見を分離する。
- 確認できない事項を「確認済み」と表現しない。
- 効果や順位上昇を根拠なく予測しない。
- Shared Editorial KnowledgeのEvidence Strength Wordingを適用する。

## 8. Search Intent・SEO品質

- Primary Intentを先に確定する。
- Main Answerを導入または早い段階で明示する。
- SEOタイトルの約束と本文内容を一致させる。
- Main Queryは純粋なクエリとして保持する。
- Secondary Queryへ過剰適合しない。
- 別記事意図は無理に本文へ統合しない。
- 内部リンクは「採用・保留・不採用」を意味的関連性で分類する。
- FAQは本文の残余疑問に答え、新しい価値がない場合は増やさない。

## 9. 日本語・表示品質

- 自然な日本語を定型的な丁寧語より優先する。
- 一つの節に一つの目的を持たせる。
- 過剰な箇条書き、同義反復、機械的な結論を避ける。
- Before/Afterは合意済みMarkdown形式を使用する。
- 公開先形式は`SIMS_PLATFORM_GUIDE.md`と`QF-SIT-003`へ従う。
- 内部思考、英語の作業文、未完成メモを利用者出力へ混入させない。

## 10. ConfidenceとExecution Mode

### Confidence

- `high`: 必須入力が揃い、重大warning、推定、未解決矛盾がない。
- `medium`: warning、未確認事項、保留判断、更新性の高い情報がある。
- `low`: 主要入力欠損、重大矛盾未解決、改善案を確定できない。

重大warningがある状態で`high`を使用しない。

### Execution Mode

- `standard`: 標準入力が利用可能。
- `graceful_degradation`: 主要入力の一部を推定または限定判断で補う。

Graceful Degradationでは`estimated_fields`を空にしない。

## 11. Warning・Manual Review・Blocking

- warningは処理を継続できる不確実性を表す。
- informationは通常の保留、推定、現状維持理由を表す。
- manual reviewは人手確認が不可欠な場合だけに使用する。
- blocking ruleに該当する場合は公開可能と判定しない。
- warning、information、errorを同じ意味で使用しない。

## 12. 出力整合性

最終監査では次を一致させる。

- 改善サマリー
- Before/After
- 改善後本文
- 変更箇所一覧
- `changes`フラグ
- Improvement Type
- Rewrite Level / Scope
- Next Action
- Confidence / warnings / information
- Canonical SIMS Feedback JSON

評価しただけ、候補に挙げただけ、保留しただけの項目を`changes=true`にしない。

## 13. Release Quality

リリース候補は次を満たす必要がある。

- Registryと実ファイルが一致する。
- JSON Schemaとサンプルが検証を通過する。
- Golden UATと実記事回帰が合格する。
- Shared snapshotのVERSIONとmanifestが一致する。
- Writer本体とClaude Projectの必須資産が同期する。
- 重大回帰、Contract違反、文字化けがない。
- README、CHANGELOG、VERSION、Release Notesが一致する。

## 14. 責務境界

- Shared Repository: 製品横断の編集Knowledgeの正本。
- SIMS Writer: 診断、変更範囲、品質ルール、Gate、Contract、Publication Packageの正本。
- Claude Project: Writerの確定資産を実行時に参照する配布形態。独自の品質基準を追加しない。

## 15. Sprint 1完了条件

- 本書が`product/quality/QUALITY_FRAMEWORK.md`に存在する。
- Platform GuideおよびImprovement Planと相互参照される。
- Shared mappingに責務境界が反映される。
- Claude Projectへ同一内容が同梱される。
- 文書存在・同期・version整合の回帰テストが合格する。


## Search Console Query Intelligence v1.2.0
- 最大200件の生クエリを解析し、Coverageで信頼度を調整する。
- QUERY MIX、CONTENT GAP、別記事・内部リンク・カニバリ候補は本文との照合とEvidence Boundaryに従う。
- Winnerクエリとタイトルを保護する。
