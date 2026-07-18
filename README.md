# SIMS Writer

SIMS Writer Product 1.0 Implementation Alpha。Engine中心設計を使わず、Quality / Evidence / Consistency / SEO / Patterns / Contractsを中核に記事改善を行います。

## Version

`0.2.0-alpha.1`

## 処理原則

Quality AuditをSEO改善より先に実行し、Quality Gateで変更範囲を決定します。重大な前提誤りは`stop_and_rewrite`です。利用者向け本文とSIMS Feedback JSON v2.1は、同一Runtime Stateから生成します。

## 主な収録物

- Claude Project Instructions
- Knowledge Pack / SEO Knowledge / Pattern Library
- Quality Gate / Evidence Verification / Consistency Audit
- SIMS Feedback JSON Contract v2.1 / JSON Schema
- reason codes / warning codes / v1互換仕様
- 4種類のProduct 1.0回帰テスト
- セットアップ・テスト手順

## 検証

```bash
python -m pytest -q
python tools/validate_release_v020.py
```

Claudeへの登録方法は `docs/SETUP_AND_TEST.md` と `claude/SETUP_GUIDE.md` を参照してください。
