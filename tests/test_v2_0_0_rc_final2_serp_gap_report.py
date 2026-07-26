from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def test_version_and_contract():
 assert read("VERSION").strip()=="2.0.0-release-candidate.2"
 s=json.loads(read("schemas/SIMS_FEEDBACK_V2.schema.json"))
 assert s["properties"]["contract_version"]["const"]=="4.2"
 assert "serp_gap_report" in s["properties"]["publication_result"]["properties"]
def test_template_has_serp_gap_report():
 t=read("templates/response-template.md")
 assert "SERP比較結果" in t and "現在の記事の強み" in t and "不足していた点" in t
def test_no_competitor_copy_rule():
 t=read("runtime/serp-gap-report-v2.0.md")
 assert "推測値" in t and "Evidence不足" in t
def test_claude_contract42():
 t=read("claude/CLAUDE_PROJECT_INSTRUCTIONS.md")
 assert "Contract 4.2" in t and "publication_result.serp_gap_report" in t
