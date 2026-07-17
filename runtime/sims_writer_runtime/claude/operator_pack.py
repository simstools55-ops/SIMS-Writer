from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ClaudeUATOperatorPackError(ValueError):
    pass


class ClaudeUATOperatorPackBuilder:
    """Create a human-readable operator pack from a prepared UAT session."""

    def build(self, session_root: Path, output_dir: Path) -> dict[str, Any]:
        session_root = session_root.resolve()
        manifest_path = session_root / "session-manifest.json"
        if not manifest_path.is_file():
            raise ClaudeUATOperatorPackError(f"session manifest not found: {manifest_path}")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ClaudeUATOperatorPackError(f"invalid session manifest: {exc}") from exc
        records = manifest.get("records")
        if not isinstance(records, list) or not records:
            raise ClaudeUATOperatorPackError("session manifest has no records")

        pack_root = output_dir.resolve() / "claude-uat-operator-pack"
        prompts_dir = pack_root / "prompts"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        items: list[dict[str, Any]] = []
        for index, record in enumerate(records, start=1):
            request_rel = str(record.get("request_file", ""))
            request_path = session_root / request_rel
            if not request_path.is_file():
                raise ClaudeUATOperatorPackError(f"request file missing: {request_rel}")
            try:
                request = json.loads(request_path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ClaudeUATOperatorPackError(f"invalid request JSON {request_rel}: {exc}") from exc
            article_id = str(record.get("article_id") or request.get("article_id") or "").strip()
            if not article_id:
                raise ClaudeUATOperatorPackError(f"article_id missing: {request_rel}")
            response_rel = str(record.get("response_file", ""))
            evidence_rel = str(record.get("evidence_file", ""))
            validation_name = response_rel.replace("responses/", "validation/").replace("-claude-output.json", "-validation.json")
            prompt_name = f"{index:02d}-{article_id}-prompt.md"
            prompt_path = prompts_dir / prompt_name
            prompt_path.write_text(
                self._prompt(article_id, request, response_rel, validation_name, evidence_rel), encoding="utf-8"
            )
            items.append({
                "sequence": index,
                "article_id": article_id,
                "request_file": request_rel,
                "prompt_file": f"prompts/{prompt_name}",
                "response_file": response_rel,
                "validation_file": validation_name,
                "evidence_file": evidence_rel,
                "status": "pending",
            })

        operator_manifest = {
            "operator_pack_version": "1.0",
            "session_id": str(manifest.get("session_id", "")),
            "article_count": len(items),
            "items": items,
        }
        (pack_root / "operator-pack-manifest.json").write_text(
            json.dumps(operator_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (pack_root / "README.md").write_text(self._readme(operator_manifest), encoding="utf-8")
        (pack_root / "SCORING_GUIDE.md").write_text(self._scoring_guide(), encoding="utf-8")
        (pack_root / "PROGRESS_CHECKLIST.md").write_text(self._progress(items), encoding="utf-8")
        return {"pack_root": str(pack_root), "manifest": operator_manifest}

    @staticmethod
    def _prompt(article_id: str, request: dict[str, Any], response_file: str, validation_file: str, evidence_file: str) -> str:
        request_json = json.dumps(request, ensure_ascii=False, indent=2)
        return f"""# Claude実記事UAT: {article_id}

## 保存先

- Claude応答: `{response_file}`
- Runtime検証: `{validation_file}`
- 評価証拠: `{evidence_file}`

## 実行手順

1. 下の依頼JSONをClaude Projectへそのまま送信する。
2. ClaudeのJSON応答を、説明文やMarkdownコードフェンスを加えず保存する。
3. Runtimeの`--validate-claude-output`で検証する。
4. 内容を人が確認してから評価証拠へ点数と所見を記録する。
5. 推測で事実や合格結果を補わない。

## 依頼JSON

```json
{request_json}
```
"""

    @staticmethod
    def _readme(manifest: dict[str, Any]) -> str:
        return f"""# Claude実記事UAT オペレーターパック

- Session ID: `{manifest['session_id']}`
- 対象記事数: {manifest['article_count']}

## 目的

Claude Projectでの実記事UATを、ファイル名の取り違えや記録漏れを防ぎながら実施します。

## 進め方

1. `PROGRESS_CHECKLIST.md`の順番で進める。
2. `prompts/`の各ファイルを開き、記載された依頼JSONをClaude Projectへ送る。
3. 指定された保存先へ応答・検証結果・評価証拠を保存する。
4. 採点は`SCORING_GUIDE.md`に従い、実測後のみ記入する。
5. 全件終了後に`--run-claude-uat-readiness`を実行する。

このパック自体は証拠ではありません。合否はセッション内の実測ファイルから判定されます。
"""

    @staticmethod
    def _scoring_guide() -> str:
        return """# 実記事UAT 採点ガイド

各項目を1〜5点で評価します。

- **5**: そのまま公開判断に使える。重大な修正が不要。
- **4**: 軽微な表現調整だけで使える。
- **3**: 方向性は正しいが、複数箇所の修正が必要。
- **2**: 重要な不足や不正確さがあり、大幅な修正が必要。
- **1**: 利用できない、または安全上受け入れられない。

## 評価項目

- `japanese_quality`: 自然で読みやすい日本語か。
- `factual_grounding`: 入力・本文・提供データに基づいているか。
- `source_preservation`: 元記事の良い部分を壊していないか。
- `internal_links`: 候補が実在し、関連性と挿入意図が妥当か。
- `output_completeness`: 必須出力が欠けていないか。
- `beginner_usability`: 初心者が迷わず適用できるか。

点数だけでなく、`review_notes`へ根拠を記録してください。未解決事項は点数で隠さず`blockers`へ残します。
"""

    @staticmethod
    def _progress(items: list[dict[str, Any]]) -> str:
        lines = ["# UAT進捗チェックリスト", ""]
        for item in items:
            lines.extend([
                f"## {item['sequence']:02d}. {item['article_id']}",
                "",
                f"- [ ] Claudeへ送信（`{item['prompt_file']}`）",
                f"- [ ] 応答保存（`{item['response_file']}`）",
                f"- [ ] Runtime検証（`{item['validation_file']}`）",
                f"- [ ] 人による採点（`{item['evidence_file']}`）",
                "",
            ])
        lines.extend([
            "## セッション全体", "",
            "- [ ] 初心者セットアップ証拠を記入", 
            "- [ ] 未解決ブロッカーを確認", 
            "- [ ] 最終Readiness判定を実行", "",
        ])
        return "\n".join(lines)
