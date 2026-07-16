# Pattern Selection Policy

1. Decision Action PlanにactionがあるComponentのみ候補化する。
2. no_change、preserve、deferの対象には生成Patternを適用しない。
3. Safety、Evidence、Primary Intent、改善目的、Sectionの順で優先する。
4. Non-Applicabilityまたは入力不足の場合は選択しない。
5. 選択理由とPattern Versionを記録する。
