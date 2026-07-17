from __future__ import annotations

import json
from pathlib import Path

from runtime.sims_writer_runtime.batch import BatchProcessor

ROOT = Path(__file__).resolve().parents[2]


def _request(request_id: str, *, with_content: bool = True) -> dict:
    request = {
        "request_id": request_id,
        "request_type": "existing_article_improvement",
        "language": "ja",
        "target_url": f"https://example.com/{request_id.lower()}",
        "current_title": "DiscordをiPhoneで翻訳する方法",
        "main_query": "discord 翻訳 iphone",
        "supporting_queries": ["discord 自動翻訳 iphone"],
        "improvement_goal": ["seo_title", "introduction", "faq"],
        "requested_output": ["before_after", "change_reason"],
        "performance": {"clicks": 20, "impressions": 1200, "ctr": 0.016, "average_position": 7.0},
        "source_system": "generic_json",
        "schema_version": "1.0",
    }
    if with_content:
        request.update({
            "existing_content": "<article><h1>DiscordをiPhoneで翻訳する方法</h1><p>翻訳方法を説明します。</p></article>",
            "content_format": "html",
        })
    return request


def test_batch_processes_multiple_requests_and_writes_summary(tmp_path):
    input_dir = tmp_path / "requests"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "01.json").write_text(json.dumps(_request("REQ-BATCH-001"), ensure_ascii=False), encoding="utf-8")
    (input_dir / "02.json").write_text(json.dumps(_request("REQ-BATCH-002", with_content=False), ensure_ascii=False), encoding="utf-8")

    summary = BatchProcessor(ROOT).execute_directory(input_dir, output_dir)

    assert summary["counts"] == {"total": 2, "succeeded": 1, "manual_review_required": 1, "failed": 0}
    assert (output_dir / "batch-summary.json").exists()
    assert (output_dir / "batch-summary.md").exists()
    assert (output_dir / "items" / "REQ-BATCH-001" / "article.md").exists()
    assert (output_dir / "items" / "REQ-BATCH-002" / "runtime-result.json").exists()


def test_batch_continues_after_invalid_json_and_avoids_duplicate_output_names(tmp_path):
    input_dir = tmp_path / "requests"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    (input_dir / "01.json").write_text(json.dumps(_request("REQ/DUP"), ensure_ascii=False), encoding="utf-8")
    (input_dir / "02.json").write_text(json.dumps(_request("REQ/DUP"), ensure_ascii=False), encoding="utf-8")
    (input_dir / "03.json").write_text("{broken", encoding="utf-8")

    summary = BatchProcessor(ROOT).execute_directory(input_dir, output_dir)

    assert summary["counts"]["total"] == 3
    assert summary["counts"]["succeeded"] == 2
    assert summary["counts"]["failed"] == 1
    assert (output_dir / "items" / "REQ-DUP" / "article.md").exists()
    assert (output_dir / "items" / "REQ-DUP-2" / "article.md").exists()
    failed = [item for item in summary["items"] if item["batch_status"] == "failed"][0]
    assert (output_dir / failed["output_directory"] / "batch-error.json").exists()
