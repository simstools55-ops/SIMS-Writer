# Validation Report

Version: 0.15.0-alpha.1
Status: RC3 Publish Quality Alpha

## Automated checks

- Pytest regression suite excluding standalone contract runner: 19 passed
- Contract schema examples: 15 passed, 0 failed
- RC3 Publish Quality tests: 6 passed
- RC2 Strict Contract regression retained

## RC3 scope

- Three-level improvement necessity judgment
- Search-intent classification
- Comparison article consistency validation
- Expected-effect requirement for changed items
- Unchanged-reason rule
- Estimated editing time

## Known boundary

- `partial` remains the Product 1.0 primary mode.
- `full` and `publish` remain beta.
- Comparison consistency validation requires structured comparison data; Claude Instructions provide the human-output gate.
