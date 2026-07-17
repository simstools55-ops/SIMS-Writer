# Validation Report

Version: 0.14.3-alpha.1

## Result

- RC2 output contract tests: passed
- CTR vertical slice tests: passed
- Golden UAT tests: passed
- Runtime core tests: passed
- Quality runtime tests: passed
- Total selected regression tests: 9 passed

## Added checks

- Forbidden greeting / acknowledgment / honorific preface
- SEO title recommended maximum 40 characters; hard maximum 45
- Meta description recommended maximum 120 characters; hard maximum 140
- Exactly one fenced `json` block
- JSON block must be the final response element
- `partial` positioned as the Product 1.0 primary mode
- `full` and `publish` positioned as beta modes until embedded article assets can be preserved reliably


## 0.14.3-alpha.1 Strict Contract Compliance

- Output Contract regression: 12 passed
- Contract schemas: 15 passed
- Decision assets and contracts: passed
- User JSON contract exact key/order/type validation: passed
- Claude fixed legacy schema conflict: removed
