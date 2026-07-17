from pathlib import Path

from runtime.sims_writer_runtime.claude.uat import ClaudeGoldenUATRunner

ROOT = Path(__file__).resolve().parents[2]


def test_claude_golden_uat_passes_all_cases() -> None:
    report = ClaudeGoldenUATRunner(ROOT).run()
    assert report["status"] == "passed"
    assert report["counts"] == {"total": 6, "passed": 6, "failed": 0}
