from pathlib import Path


def test_v301_assets_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "runtime/seo-critical-auto-repair-v3.0.1.md").exists()
    assert (root / "runtime/publication-finalization-gate-v3.0.1.md").exists()


def test_advisory_failure_does_not_force_revision(tmp_path):
    from runtime.sims_writer_runtime.qa.severity import split_issues
    issues = [{"rule_id": "QF-REA-001", "severity": "minor", "result": "fail"}]
    groups = split_issues(issues)
    assert not groups["seo_critical"]
    assert len(groups["quality_recommendation"]) == 1


def test_critical_issue_is_classified():
    from runtime.sims_writer_runtime.qa.severity import split_issues
    issues = [{"rule_id": "QF-INT-001", "severity": "major", "result": "fail"}]
    assert len(split_issues(issues)["seo_critical"]) == 1


def test_review_policy_allows_three_cycles():
    from runtime.sims_writer_runtime.qa.contracts import QAReviewPolicy
    assert QAReviewPolicy.from_context({}).max_review_cycles == 3
