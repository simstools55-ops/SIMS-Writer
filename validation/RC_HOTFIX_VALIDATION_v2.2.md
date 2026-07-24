# RC Hotfix Validation v2.2

| Code | Rule | Failure behavior |
|---|---|---|
| VAL-JSON-001 | Output must be SIMS_FEEDBACK_V2 v2.0 with all required fields | FAIL and regenerate |
| VAL-ID-001 | article_id and article_url match the input record | FAIL / manual_review |
| VAL-ANSWER-001 | Title, introduction, body, FAQ, and conclusion do not conflict | FAIL |
| VAL-TITLE-PROMISE-001 | Body fulfills the title's concrete promise | FAIL |
| VAL-MAINQUERY-001 | Main query is not replaced by a small secondary query without evidence | warning or FAIL |
| VAL-RANK-001 | Rank alone is not used to assert backlink, expertise, or content deficits | warning |
| VAL-SERP-001 | No guaranteed snippet/rich-result/voice-search/CTR claim | warning |
| VAL-SOURCE-001 | Named-person or official attribution has a verifiable source | FAIL |
| VAL-PRIVACY-001 | Privacy-redaction guidance explains opaque masking and final verification | FAIL |
| VAL-REDACTION-001 | Blur, mosaic, opaque masking, and object removal are not treated as equivalent | warning |
| VAL-FREE-001 | Free, freemium, trial, subscription, and paid are distinguished | FAIL |
| VAL-APP-FRESHNESS-001 | App name, availability, price, and free scope are current or qualified | warning |
| VAL-FOOD-001 | Experience-based timing is not presented as a food-safety standard | warning or FAIL |
| VAL-LANGUAGE-001 | Uncommon spelling or disputed etymology is not presented as standard fact | warning |
| VAL-EARNINGS-001 | Earnings, demand, and popularity claims have evidence | FAIL |
| VAL-PRESENTATION-001 | Before/After contains no raw HTML and wraps using Markdown blockquotes | FAIL and rerender |

LOW_SAMPLE and INPUT_INCOMPLETE must appear in warnings and reduce effect confidence.
