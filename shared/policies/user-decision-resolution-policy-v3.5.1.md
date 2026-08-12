# User Decision Resolution Policy v3.5.1

## Purpose

SIMS Writer must finish editorial judgment itself whenever the available evidence and article context are sufficient. The user is not the SEO repair engine. `USER_DECISION` is reserved for facts, experiences, rights, contracts, irreversible site actions, or owner intent that only the user can determine.

## Autonomous-resolution rule

Before emitting `USER_DECISION`, Writer must compare the viable alternatives and select the best safe option when the difference can be resolved from the article body, Search Console, verified SERP, authoritative evidence, preservation rules, and change risk. Do not present `A or B; choose one` when Writer can rank the alternatives itself.

Typical examples that Writer must resolve itself:

- title/H1/meta promise alignment;
- whether an unsupported promise should be removed rather than inventing new content;
- wording choice between two evidence-supported alternatives;
- whether a low-value optional addition should be omitted;
- internal-link anchor wording when the destination and placement are already known;
- factual or freshness uncertainty that can be researched from authoritative sources. If authoritative verification still fails, omit/reject the unsupported claim rather than asking the user to research it.

## Genuine user-owned decisions

`USER_DECISION` is allowed only when at least one owner-only condition remains, including:

- whether a first-person experience actually happened;
- whether the user owns or has permission to publish a photo, quote, testimonial, dataset, or other protected material;
- private business facts, contracts, sponsorship terms, affiliate relationships, or brand policy unavailable to Writer;
- irreversible/high-impact site actions such as deletion, noindex, redirect, canonical changes, or article merge when owner intent is required;
- a strategic business preference for which no evidence-based ranking is possible.

Weak evidence alone is not a user decision. Unsupported factual additions are `INTERNAL_REJECT` or are repaired into a supportable form.

## Required interaction when a user decision remains

Writer must not finish with an ambiguous request such as `please confirm`. It must ask a concrete question and define the acceptable answer, normally `YES / NO` or a short set of named options. The item is `blocking: true` when the answer is required to finalize the requested edit. After receiving the answer, Writer must finalize the copy and regenerate the complete SBM result JSON; the user must not hand-edit JSON.

## Cross-component consistency

Before final output, compare SEO title, article title/H1, meta description, introduction, headings, FAQ, and body promises. When the same evidence supports the same conclusion across components, apply the same editorial judgment unless a component-specific preservation rule prevents it. Do not remove an unsupported promise from the SEO title while leaving the same unsupported promise in H1 as an unresolved user choice.

### Canonical example

If SEO title and H1 both promise a `体験談`, but the article contains no first-person experience, Writer should normally remove `体験談` from both promises. It should not ask the user whether to remove the word or invent a new experience section. Only if the user may possess a real unpublished experience that Writer cannot know, and publication of that experience is material to the requested strategy, may Writer ask the user a direct factual question.
