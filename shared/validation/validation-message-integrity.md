# Validation Message Integrity v1.3.9

## Mandatory rule

Every object in `validation.checks[]` MUST contain a non-empty, concrete `message`. This applies to `PASS`, `PASS_WITH_WARNING`, `WARNING`, `FAIL`, and every future status.

A message must state **what was checked and what was found**. Merely repeating the status or code is insufficient.

Forbidden examples:

```json
{"code":"VAL-FACT-001","status":"PASS","message":"<空文字は禁止>"}
```

```json
{"code":"VAL-FACT-001","status":"PASS","message":"<汎用文だけでは不可>"}
```

Required example:

```json
{"code":"VAL-FACT-001","status":"PASS","message":"数値・日付・仕様・事実関係に矛盾や未確認の追加がないことを確認"}
```

## Final gate

- Missing or blank `message` is `VAL-CONTRACT-006` and blocks final output until repaired.
- Generic placeholder messages are replaced with a rule-specific message.
- Unknown validation codes receive a concrete fallback that includes code, status, and the actual checked finding; if the finding cannot be stated, the check becomes `UNVERIFIABLE` rather than `PASS`.
- A prose PASS statement never substitutes for `validation.checks[].message`.
