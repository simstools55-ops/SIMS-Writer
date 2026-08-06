# Release Final Quality Gates

Version: 2.0.0

The final publication gate runs after Strategy, Evidence, Progressive Editing and UX filtering.

Priority order:

1. Safety / YMYL
2. Fact and evidence
3. Content expectation alignment
4. Semantic naturalness
5. Search intent
6. CTR wording optimization

## Required gates

- `VAL-TITLE-SEMANTIC-001`: reject titles that join a numeric limit to an incompatible action (example: `1000枚を増やす`).
- `VAL-EXPECTATION-001`: every promise in title/meta must be supported by the article.
- `VAL-CONTENT-ALIGNMENT-001`: title, meta, introduction and body must describe the same answer scope.
- `VAL-YMYL-SAFETY-001`: necessary safety advice is not optional because demand is low.
- `VAL-BENEFIT-CLAIM-001`: adequacy and benefit claims require official/primary evidence or safer wording.

A blocking finding cannot be promoted by Editorial Strategy, SERP importance or CTR opportunity.
- `VAL-SCOPE-ALIGNMENT-001`: title/meta must not expand into adjacent intents explicitly excluded from the article scope.
- `VAL-DEVICE-PATH-001`: OS/vendor-dependent setting paths must be qualified or expressed as a settings-search instruction.
- `VAL-INTERNAL-LINK-OVERLAP-001`: every proposed internal link must pass role separation, query-overlap and cannibalization review using the same rule.


A blocking scope, device-path, or overlap finding cannot be promoted by SERP demand or CTR opportunity.

- `VAL-NATURAL-JAPANESE-001`: reject unnatural keyword-compressed Japanese such as `LINEアルバム上限`; prefer natural particles such as `LINEアルバムの上限`.
- `VAL-SIMILARITY-WORDING-001`: state `類似記事候補を検出しました` as the detection fact and leave integration/differentiation as a separate USER_DECISION.
