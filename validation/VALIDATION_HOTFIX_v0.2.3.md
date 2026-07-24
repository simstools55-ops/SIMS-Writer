# SIMS Writer v0.2.3 Validation Hotfix

## Purpose

Five-article RC regression exposed validation rules that were documented but not executable. This hotfix makes them testable and requires the final JSON validation result to reflect detected warnings.

## Executable rules

- `VAL-MAINQUERY-001`: prevents a small secondary query from replacing a substantially larger aligned query and flags inferred main queries.
- `VAL-LANGUAGE-001`: flags uncommon spelling, etymology, or broad language assertions without a verified language source.
- `VAL-PERSON-ATTRIBUTION-001`: detects named-person attribution such as “Xによると”, “Xが語る”, and “Xの方法に基づく”.
- `VAL-SOURCE-001`: requires a verifiable source for named-person attribution.
- `VAL-ANSWER-001`: preserves one canonical answer across title, introduction, body, FAQ, and conclusion.
- `VAL-CLAIM-001`: flags unsupported “最強”, psychological-effect, attraction, and safety-line claims.
- `VAL-INTERNAL-LINK-001`: an added link must include an actual URL or link markup.
- `VAL-VALIDATION-CONSISTENCY-001`: warnings and detected rules must agree with the V2 validation object.

## Gate policy

Named-person attribution without a source is a blocking defect. Main-query inference, language claims, unsupported effect claims, and missing link implementations require `PASS_WITH_WARNING` or correction before output.
