# Release Final Quality Gate

Before producing `公開OK`, run these checks in order:

1. `VAL-YMYL-SAFETY`: safety advice required by potential harm cannot be omitted or moved to optional solely because search demand is weak.
2. `VAL-BENEFIT-CLAIM`: do not publish unsupported claims such as `10分で十分`, guaranteed improvement, or named health benefits.
3. `VAL-EXPECTATION`: every promise in title/meta must exist in the article.
4. `VAL-TITLE-SEMANTIC`: reject unnatural combinations such as `1000枚を増やす`; regenerate the title.
5. `VAL-CONTENT-ALIGNMENT`: title, meta, introduction and body must share the same answer scope.

These gates override SERP importance, Editorial Strategy and CTR opportunity. A blocking item must be corrected, moved to 利用者判断, or hidden as an internal reject.
6. `VAL-SCOPE-ALIGNMENT`: reject title/meta wording that expands into adjacent symptoms or intents the article does not cover.
7. `VAL-DEVICE-PATH`: exact Android/vendor setting paths require verified OS/device scope; otherwise use feature-name search guidance and note that paths vary.
8. `VAL-INTERNAL-LINK-OVERLAP`: apply role-separation and cannibalization review to every accepted internal link, not only later candidates.

These gates override SERP demand and CTR optimization.
