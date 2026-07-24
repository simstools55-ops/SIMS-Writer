import json
from pathlib import Path
from jsonschema import Draft202012Validator
from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback, legacy_fields
ROOT=Path(__file__).resolve().parents[1]

def legacy_payload():
 return {"format":"SIMS_FEEDBACK_V2","version":"2.0","site_id":"windinglife55","article_id":"A000055","article_url":"https://windinglife55.com/623.html","diagnosis":{"code":"POSITION_OPPORTUNITY","main_query":"月末 反対","main_query_source":"user_provided","query_coverage":{"captured_impressions":1255,"total_impressions":1799,"coverage_percent":69.76,"confidence_level":"MEDIUM_COVERAGE"},"sample_size_flag":"SUFFICIENT"},"confidence":"medium","risk":"LOW","change_flags":{"seo_title":True,"description":True,"body":False},"new_values":{"article_title":"","seo_title":"月末の反対＝月初","description":"説明","main_query":"月末 反対"},"expected_effect":{"ctr":"改善を検証","clicks":""},"warnings":[],"information":[],"validation":{"status":"PASS","checks":[{"code":"VAL-ENTITY-001","status":"PASS","message":"修正済み"}],"notes":[]},"swls":{"protected_elements":["本文"]}}

def test_real_article_aliases_are_normalized_and_valid():
 o=normalize_feedback(legacy_payload())
 assert o["contract_version"]=="2.1"
 assert not legacy_fields(o)
 assert o["query_coverage"]["coverage_confidence"]=="medium"
 assert "confidence_level" not in o["query_coverage"]
 assert all("implementation_status" in c for c in o["changes"])
 assert o["implementation_status"]=="implemented"
 assert "article_title" not in o["new_values"] and "clicks" not in o["expected_effect"]
 schema=json.loads((ROOT/"contracts/json/SIMS_FEEDBACK_V2.schema.json").read_text(encoding="utf-8"))
 errors=list(Draft202012Validator(schema).iter_errors(o))
 assert not errors, [e.message for e in errors]

def test_no_legacy_fields_in_canonical_output():
 o=normalize_feedback({"diagnosis_code":"QUERY_MIX","change_flags":{"seo_title":True},"article_id":"A","article_url":"https://e.test/a","validation":{}})
 assert not ({"version","diagnosis_code","change_flags"}&set(o))
