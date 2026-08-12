# A000008 User Decision Self-Resolution Regression

## Input condition

SEO title and H1 both contain `体験談`, while the supplied article body contains no first-person experience. Writer is otherwise allowed to edit the title layer.

## Required result

Writer must not return `H1から体験談を外す / 体験談セクションを追加する` as a user choice. It must compare the options and normally select the lower-risk evidence-aligned repair: remove the unsupported `体験談` promise from SEO title and H1.

## Pass criteria

- H1 correction is included in `public_ok_changes`.
- `user_decision_changes` is empty unless a genuine user-only fact is explicitly required.
- Human output explains the chosen repair, not two alternatives.
- Final JSON matches the displayed completed copy.
