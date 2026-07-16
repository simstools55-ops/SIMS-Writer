from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .validator import PublicationArtifactValidator


class ResultArtifactWriter:
    """Persist one runtime execution as reusable, reviewable artifacts."""

    def write(self, result: Any, output_dir: Path) -> dict[str, str]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        data = result.to_dict() if hasattr(result, "to_dict") else dict(result)
        artifacts = data.get("artifacts", {})
        package = artifacts.get("publication_package", {})
        draft = artifacts.get("content_draft", {})

        files = {
            "runtime_result": output_dir / "runtime-result.json",
            "publication_package": output_dir / "publication-package.json",
            "article_markdown": output_dir / "article.md",
            "improvement_report": output_dir / "improvement-report.md",
            "execution_manifest": output_dir / "execution-manifest.json",
            "artifact_validation": output_dir / "artifact-validation.json",
            "publication_checklist": output_dir / "publication-checklist.md",
        }

        self._write_json(files["runtime_result"], data)
        self._write_json(files["publication_package"], package)
        self._write_json(files["execution_manifest"], {
            "execution_id": data.get("execution_id"),
            "request_id": data.get("request_id"),
            "status": data.get("status"),
            "manifest": data.get("manifest", {}),
            "files": {name: path.name for name, path in files.items() if name not in ("artifact_validation", "publication_checklist")},
        })
        files["article_markdown"].write_text(self._article_markdown(draft, package), encoding="utf-8")
        files["improvement_report"].write_text(self._improvement_report(data), encoding="utf-8")
        validation = PublicationArtifactValidator().validate(output_dir)
        self._write_json(files["artifact_validation"], validation)
        files["publication_checklist"].write_text(self._publication_checklist(validation), encoding="utf-8")
        return {name: str(path) for name, path in files.items()}

    @staticmethod
    def _write_json(path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def _article_markdown(draft: dict[str, Any], package: dict[str, Any]) -> str:
        h1 = draft.get("h1") or package.get("h1") or "改善記事"
        intro = draft.get("introduction") or ""
        sections = draft.get("sections") or []
        faq = draft.get("faq") or []
        conclusion = draft.get("conclusion") or ""
        lines = [f"# {h1}", ""]
        if intro:
            lines.extend([intro, ""])
        if sections:
            for section in sections:
                level = min(max(int(section.get("level", 2)), 2), 6)
                heading = str(section.get("heading") or "本文")
                content = str(section.get("content") or "").strip()
                lines.extend([f"{'#' * level} {heading}", "", content, ""])
        else:
            body = str(package.get("article_content") or draft.get("article_content") or "").strip()
            if body:
                lines.extend([body, ""])
        if faq:
            lines.extend(["## よくある質問", ""])
            for item in faq:
                lines.extend([f"### {item.get('question', '質問')}", "", str(item.get("answer", "")).strip(), ""])
        if conclusion:
            lines.extend(["## まとめ", "", conclusion, ""])
        return "\n".join(lines).rstrip() + "\n"


    @staticmethod
    def _publication_checklist(validation: dict[str, Any]) -> str:
        mark = lambda status: "[x]" if status == "pass" else "[ ]"
        lines = [
            "# SIMS Writer 公開チェックリスト",
            "",
            f"- 成果物検証: `{validation.get('artifact_status', 'unknown')}`",
            f"- 品質判定: `{validation.get('publish_decision', 'unknown')}`",
            f"- 公開準備完了: `{'yes' if validation.get('release_ready') else 'no'}`",
            "",
            "## 自動検証",
            "",
        ]
        for check in validation.get("checks", []):
            suffix = f"（{check.get('file')}）" if check.get("file") else ""
            lines.append(f"- {mark(check.get('status'))} {check.get('message', '')}{suffix}")
        if validation.get("publish_decision") == "publish_ready_with_advisory":
            lines.extend(["", "## 公開前の注意", "", "- [ ] 品質レポートのAdvisoryを確認する"])
        elif not validation.get("release_ready"):
            lines.extend(["", "## 公開停止", "", "- [ ] Fail項目を解消して再生成する"])
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _improvement_report(data: dict[str, Any]) -> str:
        artifacts = data.get("artifacts", {})
        request = artifacts.get("normalized_request", {})
        draft = artifacts.get("content_draft", {})
        before_after = draft.get("before_after", {})
        decision = artifacts.get("decision_action_plan", {})
        quality = artifacts.get("quality_report", {})
        lines = [
            "# SIMS Writer 改善結果レポート",
            "",
            f"- 実行ID: `{data.get('execution_id', '')}`",
            f"- 依頼ID: `{data.get('request_id', '')}`",
            f"- 判定: `{data.get('status', '')}`",
            f"- メインクエリ: {request.get('main_query', '')}",
            "",
            "## 改善方針",
            "",
            f"- アクション: `{decision.get('action', '')}`",
            f"- 対象: {', '.join(decision.get('components', []))}",
            f"- 理由: {decision.get('reason', '')}",
            "",
            "## Before / After",
            "",
        ]
        if before_after:
            for key, value in before_after.items():
                label = re.sub(r"_", " ", key).title()
                if isinstance(value, dict):
                    lines.extend([f"### {label}", "", f"**Before**  ", str(value.get("before", "")), "", f"**After**  ", str(value.get("after", "")), ""])
        else:
            lines.append("Before / Afterデータはありません。")
            lines.append("")
        lines.extend([
            "## SEOメタ情報",
            "",
            f"- SEOタイトル: {draft.get('seo_title', '')}",
            f"- メタディスクリプション: {draft.get('meta_description', '')}",
            "",
            "## 品質判定",
            "",
            f"- 公開推奨: `{quality.get('publish_recommendation', data.get('status', ''))}`",
            f"- Issues: {len(quality.get('issues', []))}",
            "",
        ])
        return "\n".join(lines).rstrip() + "\n"
