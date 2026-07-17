from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .acceptance import ClaudeOutputValidator


@dataclass
class ClaudeUATCaseResult:
    case_id: str
    expected: str
    actual: str
    passed: bool
    errors: list[str]
    warnings: list[str]


class ClaudeGoldenUATRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.validator = ClaudeOutputValidator(repo_root)

    def run(self) -> dict[str, Any]:
        cases_dir = self.repo_root / "tests" / "claude" / "uat" / "cases"
        results: list[ClaudeUATCaseResult] = []
        for path in sorted(cases_dir.glob("*.json")):
            case = json.loads(path.read_text(encoding="utf-8"))
            report = self.validator.validate_text(
                json.dumps(case["output"], ensure_ascii=False), case.get("request")
            )
            actual = "accepted" if report.valid else "rejected"
            expected = case["expected"]
            results.append(
                ClaudeUATCaseResult(
                    case_id=case["case_id"], expected=expected, actual=actual,
                    passed=actual == expected, errors=report.errors, warnings=report.warnings,
                )
            )
        passed = sum(item.passed for item in results)
        return {
            "suite": "claude-project-golden-uat",
            "status": "passed" if passed == len(results) and results else "failed",
            "counts": {"total": len(results), "passed": passed, "failed": len(results) - passed},
            "results": [asdict(item) for item in results],
        }
