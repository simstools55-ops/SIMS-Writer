# Release Notes — v0.2.3 Validation Hotfix

This release follows the five-article v0.2.2 RC regression: A000063, A000006, A000036, A000020, and A000001.

## Fixed

- Made main-query evidence checks executable.
- Added language-claim verification for uncommon spellings and unsupported generalizations.
- Added named-person attribution and source checks.
- Added unsupported strong-claim detection.
- Added real internal-link implementation verification.
- Added consistency checks between narrative warnings and `SIMS_FEEDBACK_V2.validation`.

## Release gate

The hotfix regression suite contains targeted reproductions for all five articles. No additional broad article test is required before the next RC decision; run the included automated suite and one Claude smoke test.
