# User Output Compactness v2.0

Normal user output contains only:
1. one publication-status sentence;
2. `公開OK` with copy-ready Before/After;
3. `利用者判断` only when a real human decision exists;
4. one internal-link result sentence when needed;
5. one Contract 4.2 JSON block at the end.

## Publication-status sentence

Always begin with exactly one of the following meanings in plain Japanese:

- No user decision: `今回の修正は、そのまま公開できます。`
- User decision exists: `公開OKの修正はそのまま反映できます。利用者判断の項目だけ確認してください。`

Do not begin with improvement codes, diagnosis, rankings, SERP details, or analysis summaries.

## Change explanation

Change reasons are optional. When shown, use one plain-Japanese sentence focused on what becomes clearer, more accurate, or safer for the reader. Do not mention internal SEO terminology, evidence levels, character-count rules, validation, or query-processing details.

## Internal links

When no internal link is adopted, write exactly: `今回は追加できる内部リンクはありません。` Do not append candidate counts, rejection reasons, parentheses, or tables. Candidate-level reasons remain internal.

Do not display improvement codes, query coverage, SERP entities, QA verdicts, detailed competitor evidence, or internal audit information.


## SERP Gap Report

When SERP comparison materially determined the edits, show one compact `SERP比較結果` section before `公開OK`. It may show strengths, confirmed gaps, applied topics, and important topics not adopted. Do not show competitor URLs, raw counts unless actually verified, internal scores, evidence labels, or audit traces. Never claim a topic is a gap merely because competitors mention it; require alignment across query demand, SERP intent, and the article.

## Gold Explainability Gate
- SERP比較件数・掲載数は実測値だけを表示する。未計測なら省略する。
- 各Gapに重要度1〜5と星表記を付ける。重要度は需要、SERP共通性、自記事不足、Evidenceで決める。
- SERP Gap Reportには3〜5行の利用者向けDecision Traceを付ける。
- USER_DECISIONには2〜5行のDecision Traceを付け、なぜ公開OKにしなかったかを平易に示す。
- 生の思考過程、内部スコア、競合URL一覧は表示しない。

## Doctor Referral Human Experience Addendum (v3.3.1-RC1)

`DOCTOR_REFERRAL_TREATMENT`でも通常改善と同じHuman Output品質を必須とする。

- PUBLIC_OK各変更に対象 / Before / After / 理由 / 期待する効果を表示する。
- 新規追加のBeforeは`（該当箇所なし・新規追加）`とする。
- Doctor/SBMのMachine Layer用フィールド名を利用者へ表示しない。
- JSONにBefore/Afterが存在していても、利用者向けMarkdownから省略した場合はHuman Usability GateをFAILとする。

USER_DECISIONを表示する場合は、曖昧な確認依頼ではなくYES/NOまたは明示した選択肢の質問を出す。WriterがSEO的に選べる案を利用者へ丸投げしない。
