from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .orchestrator import RuntimeOrchestrator
from .export import ResultArtifactWriter


@dataclass(frozen=True)
class BatchItem:
    source: Path
    request_id: str
    output_dir: Path


class BatchInputError(ValueError):
    pass


class BatchProcessor:
    """Execute multiple improvement requests without stopping at the first failure."""

    def __init__(self, repo_root: Path, *, source_fetch_enabled: bool = False):
        self.repo_root = Path(repo_root)
        self.orchestrator = RuntimeOrchestrator(self.repo_root, source_fetch_enabled=source_fetch_enabled)
        self.writer = ResultArtifactWriter()

    def execute_directory(
        self,
        input_dir: Path,
        output_dir: Path,
        input_type: str = "auto",
    ) -> dict[str, Any]:
        input_dir = Path(input_dir).resolve()
        output_dir = Path(output_dir).resolve()
        if not input_dir.is_dir():
            raise BatchInputError(f"batch input directory does not exist: {input_dir}")

        sources = sorted(path for path in input_dir.glob("*.json") if path.is_file())
        if not sources:
            raise BatchInputError(f"no JSON requests found in: {input_dir}")

        output_dir.mkdir(parents=True, exist_ok=True)
        items_dir = output_dir / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        started_at = datetime.now(timezone.utc).isoformat()
        records: list[dict[str, Any]] = []
        used_slugs: set[str] = set()

        for index, source in enumerate(sources, start=1):
            record = self._execute_one(source, items_dir, input_type, index, used_slugs)
            records.append(record)

        completed_at = datetime.now(timezone.utc).isoformat()
        counts = {
            "total": len(records),
            "succeeded": sum(1 for item in records if item["batch_status"] == "succeeded"),
            "manual_review_required": sum(
                1 for item in records if item["batch_status"] == "manual_review_required"
            ),
            "failed": sum(1 for item in records if item["batch_status"] == "failed"),
        }
        summary = {
            "batch_version": "1.0",
            "started_at": started_at,
            "completed_at": completed_at,
            "input_directory": str(input_dir),
            "output_directory": str(output_dir),
            "counts": counts,
            "status": "completed_with_failures" if counts["failed"] else "completed",
            "items": records,
        }
        (output_dir / "batch-summary.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output_dir / "batch-summary.md").write_text(
            self._summary_markdown(summary), encoding="utf-8"
        )
        return summary

    def _execute_one(
        self,
        source: Path,
        items_dir: Path,
        input_type: str,
        index: int,
        used_slugs: set[str],
    ) -> dict[str, Any]:
        request_id = source.stem
        item_output: Path | None = None
        try:
            raw = json.loads(source.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise BatchInputError("request root must be a JSON object")
            request_id = str(raw.get("request_id") or source.stem)
            slug = self._unique_slug(request_id, index, used_slugs)
            item_output = items_dir / slug
            result = self.orchestrator.execute(raw, input_type)
            self.writer.write(result, item_output)
            batch_status = self._batch_status(result)
            return {
                "index": index,
                "source_file": source.name,
                "request_id": result.request_id,
                "execution_id": result.execution_id,
                "runtime_status": result.status,
                "batch_status": batch_status,
                "output_directory": str(item_output.relative_to(items_dir.parent)),
                "error": None,
            }
        except Exception as exc:
            slug = self._unique_slug(request_id, index, used_slugs)
            item_output = item_output or (items_dir / slug)
            item_output.mkdir(parents=True, exist_ok=True)
            error = {
                "category": exc.__class__.__name__,
                "message": str(exc),
            }
            (item_output / "batch-error.json").write_text(
                json.dumps(error, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            return {
                "index": index,
                "source_file": source.name,
                "request_id": request_id,
                "execution_id": None,
                "runtime_status": "failed",
                "batch_status": "failed",
                "output_directory": str(item_output.relative_to(items_dir.parent)),
                "error": error,
            }

    @staticmethod
    def _batch_status(result: Any) -> str:
        runtime_status = str(getattr(result, "status", "failed"))
        if runtime_status == "failed":
            return "failed"
        stages = getattr(result, "stages", [])
        if any(getattr(stage, "status", None) == "manual_review_required" for stage in stages):
            return "manual_review_required"
        if runtime_status in {"manual_review_required", "revision_required", "rejected"}:
            return "manual_review_required"
        return "succeeded"

    @staticmethod
    def _unique_slug(request_id: str, index: int, used_slugs: set[str]) -> str:
        base = re.sub(r"[^A-Za-z0-9._-]+", "-", request_id.strip()).strip("-._")
        base = base[:80] or f"request-{index:04d}"
        candidate = base
        suffix = 2
        while candidate.casefold() in used_slugs:
            candidate = f"{base}-{suffix}"
            suffix += 1
        used_slugs.add(candidate.casefold())
        return candidate

    @staticmethod
    def _summary_markdown(summary: dict[str, Any]) -> str:
        counts = summary["counts"]
        lines = [
            "# SIMS Writer バッチ実行結果",
            "",
            f"- 状態: `{summary['status']}`",
            f"- 合計: {counts['total']}件",
            f"- 成功: {counts['succeeded']}件",
            f"- 要確認: {counts['manual_review_required']}件",
            f"- 失敗: {counts['failed']}件",
            "",
            "## 記事別結果",
            "",
            "| No. | Request ID | 判定 | Runtime | 出力先 |",
            "|---:|---|---|---|---|",
        ]
        for item in summary["items"]:
            lines.append(
                f"| {item['index']} | {item['request_id']} | {item['batch_status']} | "
                f"{item['runtime_status']} | `{item['output_directory']}` |"
            )
        failed = [item for item in summary["items"] if item["error"]]
        if failed:
            lines.extend(["", "## エラー", ""])
            for item in failed:
                lines.append(
                    f"- `{item['source_file']}`: {item['error']['category']} — {item['error']['message']}"
                )
        return "\n".join(lines).rstrip() + "\n"
