from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(p): return (ROOT/p).read_text(encoding="utf-8")
def test_version_contract42():
 assert read("VERSION").strip()=="3.0.2"
 s=json.loads(read("schemas/SIMS_FEEDBACK_V2.schema.json"))
 assert s["properties"]["contract_version"]["const"]=="4.2"
 assert "decision_trace" in s["$defs"]["userDecisionChange"]["required"]
def test_serp_quant_and_importance():
 s=json.loads(read("schemas/SIMS_FEEDBACK_V2.schema.json"))
 item=s["$defs"]["serpGapItem"]
 assert "importance" in item["required"] and "importance_label" in item["required"]
 assert "observed_count" in item["properties"] and "compared_count" in item["properties"]
 report=s["$defs"]["serpGapReport"]
 assert "compared_pages" in report["required"] and "decision_trace" in report["required"]
def test_templates():
 t=read("templates/response-template.md")
 assert "比較範囲" in t and "重要度" in t and "判断の流れ" in t and "Contract 4.2" in t
def test_no_fabricated_counts():
 t=read("runtime/serp-gap-report-v2.0.md")
 assert "実際に個別確認" in t and "推測値" in t and "Evidence不足" in t
