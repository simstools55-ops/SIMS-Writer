from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ArtifactCheck:
    check_id: str
    status: str
    message: str
    file: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class PublicationArtifactValidator:
    """Validate persisted publication artifacts and produce reproducible checksums."""

    REQUIRED_FILES = (
        "runtime-result.json",
        "publication-package.json",
        "article.md",
        "improvement-report.md",
        "execution-manifest.json",
    )

    def validate(self, output_dir: Path) -> dict[str, Any]:
        output_dir = Path(output_dir)
        checks: list[ArtifactCheck] = []
        checksums: dict[str, dict[str, Any]] = {}

        for name in self.REQUIRED_FILES:
            path = output_dir / name
            if not path.is_file():
                checks.append(ArtifactCheck("ART-FILE-001", "fail", "必須成果物がありません", name))
                continue
            raw = path.read_bytes()
            checksums[name] = {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
            checks.append(ArtifactCheck("ART-FILE-001", "pass", "必須成果物を確認しました", name))
            if len(raw) == 0:
                checks.append(ArtifactCheck("ART-FILE-002", "fail", "成果物が空です", name))
            else:
                checks.append(ArtifactCheck("ART-FILE-002", "pass", "成果物は空ではありません", name))

        json_payloads: dict[str, Any] = {}
        for name in ("runtime-result.json", "publication-package.json", "execution-manifest.json"):
            path = output_dir / name
            if not path.is_file():
                continue
            try:
                json_payloads[name] = json.loads(path.read_text(encoding="utf-8"))
                checks.append(ArtifactCheck("ART-JSON-001", "pass", "UTF-8 JSONとして読み込めます", name))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                checks.append(ArtifactCheck("ART-JSON-001", "fail", f"JSONを読み込めません: {exc}", name))

        runtime = json_payloads.get("runtime-result.json", {})
        package = json_payloads.get("publication-package.json", {})
        manifest = json_payloads.get("execution-manifest.json", {})
        execution_ids = {value for value in (
            runtime.get("execution_id"), manifest.get("execution_id")
        ) if value}
        request_ids = {value for value in (
            runtime.get("request_id"), manifest.get("request_id")
        ) if value}
        checks.append(ArtifactCheck(
            "ART-ID-001", "pass" if len(execution_ids) == 1 else "fail",
            "実行IDが成果物間で一致しています" if len(execution_ids) == 1 else "実行IDが一致しません",
        ))
        checks.append(ArtifactCheck(
            "ART-ID-002", "pass" if len(request_ids) == 1 else "fail",
            "依頼IDが成果物間で一致しています" if len(request_ids) == 1 else "依頼IDが一致しません",
        ))

        required_package = ("publish_decision", "article_content", "seo_title", "meta_description", "h1", "quality_summary")
        missing = [key for key in required_package if not package.get(key)]
        checks.append(ArtifactCheck(
            "ART-PKG-001", "pass" if not missing else "fail",
            "公開パッケージの必須項目を確認しました" if not missing else f"公開パッケージの不足項目: {', '.join(missing)}",
            "publication-package.json",
        ))

        article = output_dir / "article.md"
        article_text = article.read_text(encoding="utf-8") if article.is_file() else ""
        article_ok = article_text.startswith("# ") and len(article_text.strip()) >= 80
        checks.append(ArtifactCheck(
            "ART-MD-001", "pass" if article_ok else "fail",
            "記事MarkdownにH1と本文があります" if article_ok else "記事MarkdownのH1または本文が不足しています",
            "article.md",
        ))

        publish_decision = package.get("publish_decision") or runtime.get("status") or "unknown"
        failures = [c.to_dict() for c in checks if c.status == "fail"]
        artifact_status = "valid" if not failures else "invalid"
        release_ready = artifact_status == "valid" and publish_decision in ("publish_ready", "publish_ready_with_advisory")
        return {
            "validation_version": "1.0.0",
            "artifact_status": artifact_status,
            "publish_decision": publish_decision,
            "release_ready": release_ready,
            "summary": {
                "pass": sum(c.status == "pass" for c in checks),
                "fail": len(failures),
                "checks": len(checks),
            },
            "checks": [c.to_dict() for c in checks],
            "failures": failures,
            "checksums": checksums,
        }
