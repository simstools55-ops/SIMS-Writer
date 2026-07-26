# Natural Japanese and Similarity Reporting Validation

Version: 2.0.0

- `VAL-NATURAL-JAPANESE-001`: reject unnatural compressed noun chains in titles, metadata and user-facing reasons. Regenerate with natural particles and readable syntax.
- `VAL-SIMILARITY-WORDING-001`: when a similarity candidate is detected, require both the detection fact and a separate user-decision boundary for consolidation or differentiation.

These gates run after semantic, expectation and scope validation and before final UX output. They do not change Contract 4.2.
