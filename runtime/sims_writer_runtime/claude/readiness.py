from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REQUIRED_SCORE_KEYS = (
    "japanese_quality",
    "factual_grounding",
    "source_preservation",
    "internal_links",
    "output_completeness",
    "beginner_usability",
)


class ClaudeReadinessEvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class EvidenceResult:
    file: str
    evidence_id: str
    article_id: str
    outcome: str
    valid: bool
    average_score: float
    blockers: list[str]
    errors: list[str]


class ClaudeUserTestReadinessEvaluator:
    """Evaluate manually recorded Claude Project real-article UAT evidence."""

    minimum_articles = 3
    minimum_average_score = 4.0

    def evaluate_directory(self, evidence_dir: Path) -> dict[str, Any]:
        evidence_dir = evidence_dir.resolve()
        if not evidence_dir.is_dir():
            raise ClaudeReadinessEvidenceError(f"evidence directory not found: {evidence_dir}")
        paths = sorted(path for path in evidence_dir.glob("*.json") if path.is_file())
        results = [self._evaluate_file(path) for path in paths]
        valid_results = [item for item in results if item.valid]
        article_ids = sorted({item.article_id for item in valid_results if item.article_id})
        completed = [item for item in valid_results if item.outcome == "generated"]
        manual_review = [item for item in valid_results if item.outcome == "manual_review_required"]
        blockers = sorted({blocker for item in valid_results for blocker in item.blockers})
        beginner_setup = any(self._beginner_setup_completed(path) for path in paths)
        score_pass = bool(completed) and all(item.average_score >= self.minimum_average_score for item in completed)
        conditions = {
            "valid_evidence_files": len(valid_results) == len(results) and bool(results),
            "minimum_distinct_articles": len(article_ids) >= self.minimum_articles,
            "generated_quality_threshold": score_pass,
            "manual_review_case_verified": bool(manual_review),
            "no_open_blockers": not blockers,
            "beginner_setup_verified": beginner_setup,
        }
        ready = all(conditions.values())
        return {
            "report_version": "1.0",
            "status": "user_test_ready" if ready else "not_user_test_ready",
            "ready": ready,
            "policy": {
                "minimum_distinct_articles": self.minimum_articles,
                "minimum_average_score": self.minimum_average_score,
                "required_score_keys": list(REQUIRED_SCORE_KEYS),
            },
            "counts": {
                "files": len(results),
                "valid": len(valid_results),
                "invalid": len(results) - len(valid_results),
                "distinct_articles": len(article_ids),
                "generated": len(completed),
                "manual_review_required": len(manual_review),
                "open_blockers": len(blockers),
            },
            "conditions": conditions,
            "open_blockers": blockers,
            "results": [asdict(item) for item in results],
        }

    def _evaluate_file(self, path: Path) -> EvidenceResult:
        errors: list[str] = []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return EvidenceResult(path.name, "", "", "", False, 0.0, [], [f"invalid JSON: {exc}"])
        required = ("evidence_id", "article_id", "outcome", "scores", "blockers", "setup")
        for key in required:
            if key not in data:
                errors.append(f"missing required field: {key}")
        outcome = str(data.get("outcome", ""))
        if outcome not in {"generated", "manual_review_required"}:
            errors.append("outcome must be generated or manual_review_required")
        scores = data.get("scores")
        values: list[float] = []
        if not isinstance(scores, dict):
            errors.append("scores must be an object")
        else:
            for key in REQUIRED_SCORE_KEYS:
                value = scores.get(key)
                if not isinstance(value, (int, float)) or isinstance(value, bool) or not 1 <= float(value) <= 5:
                    errors.append(f"score {key} must be between 1 and 5")
                else:
                    values.append(float(value))
        blockers_raw = data.get("blockers", [])
        if not isinstance(blockers_raw, list) or any(not isinstance(item, str) or not item.strip() for item in blockers_raw):
            errors.append("blockers must be an array of non-empty strings")
            blockers: list[str] = []
        else:
            blockers = [item.strip() for item in blockers_raw]
        setup = data.get("setup")
        if not isinstance(setup, dict) or not isinstance(setup.get("completed"), bool) or setup.get("operator_level") not in {"developer", "beginner"}:
            errors.append("setup must include completed boolean and operator_level developer/beginner")
        if outcome == "manual_review_required" and not data.get("unresolved_items"):
            errors.append("manual_review_required evidence needs unresolved_items")
        average = round(sum(values) / len(values), 2) if len(values) == len(REQUIRED_SCORE_KEYS) else 0.0
        return EvidenceResult(
            file=path.name,
            evidence_id=str(data.get("evidence_id", "")),
            article_id=str(data.get("article_id", "")),
            outcome=outcome,
            valid=not errors,
            average_score=average,
            blockers=blockers,
            errors=errors,
        )

    @staticmethod
    def _beginner_setup_completed(path: Path) -> bool:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
        setup = data.get("setup", {})
        return setup.get("operator_level") == "beginner" and setup.get("completed") is True


def write_readiness_report(report: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "claude-user-test-readiness.json"
    md_path = output_dir / "claude-user-test-readiness.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Claude利用者テスト開始判定",
        "",
        f"- 判定: **{report['status']}**",
        f"- 実記事数: {report['counts']['distinct_articles']}",
        f"- 有効証拠: {report['counts']['valid']}/{report['counts']['files']}",
        f"- 未解決ブロッカー: {report['counts']['open_blockers']}",
        "",
        "## 開始条件",
        "",
    ]
    for key, passed in report["conditions"].items():
        lines.append(f"- {'✅' if passed else '❌'} {key}")
    if report["open_blockers"]:
        lines.extend(["", "## 未解決ブロッカー", ""] + [f"- {item}" for item in report["open_blockers"]])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
