# Release Notes — v0.2.3 Validation Hotfix

This release follows the five-article v0.2.2 RC regression: A900063, A900006, A900036, A900020, and A900001.

## Fixed

- Made main-query evidence checks executable.
- Added language-claim verification for uncommon spellings and unsupported generalizations.
- Added named-person attribution and source checks.
- Added unsupported strong-claim detection.
- Added real internal-link implementation verification.
- Added consistency checks between narrative warnings and `SIMS_FEEDBACK_V2.validation`.

## Release gate

The hotfix regression suite contains targeted reproductions for all five articles. No additional broad article test is required before the next RC decision; run the included automated suite and one Claude smoke test.
