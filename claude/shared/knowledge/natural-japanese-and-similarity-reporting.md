# Natural Japanese and Similarity Candidate Reporting

Version: 2.0.0

## Natural Japanese Gate
User-facing titles, metadata and explanations must read as natural Japanese after SEO optimization. Do not compress ordinary noun relations merely to preserve keywords.

Examples:
- NG: `LINEアルバム上限は1000枚`
- OK: `LINEアルバムの上限は1000枚`
- NG: `インスタ背景を戻す方法`
- OK: `インスタの背景を戻す方法`

Brand names and established product names are preserved, but surrounding ordinary nouns require natural particles when omission harms readability. Search phrase matching never overrides readable Japanese.

## Similarity candidate wording
When a related or possibly cannibalizing page is detected, separate the system observation from the user's decision.

Required wording model:
- Detection fact: `類似記事候補を検出しました。`
- Decision boundary: `統合・差別化の最終判断は利用者判断です。`

Do not state that duplicate content definitively exists unless content-role and query overlap have been verified. Do not use only vague wording such as `存在する可能性があります`; name it as a detected candidate and explain what the user must decide.
