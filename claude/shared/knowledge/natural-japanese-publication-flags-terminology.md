# Natural Japanese, Publication Flags, and Terminology Consistency

Version: 2.0.1

## Natural Japanese
User-facing titles and metadata must not preserve unnatural keyword-style noun chains. Restore particles and spacing when readability requires them.

Examples:
- NG: `LINEアルバム上限`
- OK: `LINEアルバムの上限`
- NG: `Windows11設定`
- OK: `Windows 11の設定`

## Publication flags
Public copy-ready edits and pending user decisions are independent states.

- `publishable_public_ok_changes=true`: the PUBLIC_OK subset can be applied immediately.
- `has_user_decision_changes=true`: at least one separate proposal requires user confirmation.

A pending decision must never make already approved edits appear unpublishable.

## Title semantic alignment
When an article says a system limit cannot be changed, the title must not claim that the limit or capacity itself can be increased. Use `対処法`, `整理`, `分散保存`, or `代替手段` according to the actual content.

## Terminology consistency
Use one canonical label and unit per concept. Do not describe mixed photo/video content only with the photo unit `枚`; use a neutral unit such as `コンテンツ` and state separate media limits when needed.
