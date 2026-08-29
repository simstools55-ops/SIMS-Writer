# SIMS Writer v3.3.2-RC4

## User Decision Self-Resolution Hotfix

- Writer now resolves evidence-rankable editorial alternatives internally instead of delegating SEO judgment to the user.
- Generic `requires_user_confirmation` no longer creates USER_DECISION without an owner-only reason.
- Weak evidence is repaired/researched or internally rejected rather than becoming user research homework.
- Genuine USER_DECISION items now carry a concrete question, YES/NO or named options, and blocking state.
- Added A900008 regression: unsupported `体験談` promise is removed consistently from SEO title/H1 rather than offered as an unresolved choice.
- Shared dependency updated to 3.5.1.
