# Internal Link Referral Quality v3.3.1-RC2

Applies to `DOCTOR_REFERRAL_TREATMENT`.

## Input
Prefer `doctor_referral.internal_link_recommendations` when present. Each item may include URL, title, reason, relationship, suggested context, and anchor hint. `candidate_urls` is fallback compatibility input only.

## Writer responsibility
Writer must read the source article and decide the final placement, surrounding sentence, and anchor wording. Doctor/SBM metadata is guidance, not final copy.

## Quality rules
- Do not mechanically append article titles to a related-links list merely because URLs were approved.
- Place each adopted link where the reader naturally needs the adjacent topic whenever a suitable section exists.
- Write one short contextual sentence that explains why the linked article is useful.
- Anchor wording must be natural in the sentence and must not be forced to equal the article title.
- Respect `max_links` / allowed scope. Never add unapproved destinations in Doctor Referral mode.
- If a recommended link is not naturally placeable, do not force it; report it as not performed with a plain reason.
- Human output remains target / Before / After / reason / expected effect.
