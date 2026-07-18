# セットアップ・テスト

## Claude Project
1. `claude/CLAUDE_PROJECT_INSTRUCTIONS.md`をProject Instructionsへ登録。
2. `claude/knowledge/`配下と`claude/templates/`配下をProject Knowledgeへ追加。
3. `claude/TEST_CHECKLIST.md`で初回確認。

## Repository test
```bash
python -m pytest -q
python tools/validate_release_v020.py
```
