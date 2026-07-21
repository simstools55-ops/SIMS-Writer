from pathlib import Path
import json

from runtime.sims_writer_runtime.adapters.input_adapters import normalize_sbm, normalize_generic
from runtime.sims_writer_runtime.output_contract import build_feedback

ROOT = Path(__file__).resolve().parents[1]

def test_sbm_531_identity_passthrough():
    req = normalize_sbm({
        "SiteID":"SITE-001", "SiteName":"Example", "SiteURL":"https://example.com",
        "ArticleID":"A000001", "ArticleURL":"https://example.com/a", "URL":"https://legacy.invalid/a",
        "MainQuery":"test"
    })
    assert req["site_id"] == "SITE-001"
    assert req["site_name"] == "Example"
    assert req["site_url"] == "https://example.com"
    assert req["article_id"] == "A000001"
    assert req["target_url"] == "https://example.com/a"

def test_legacy_sbm_url_remains_supported():
    req = normalize_sbm({"ArticleID":"A1", "URL":"https://legacy.example/a", "MainQuery":"q"})
    assert req["target_url"] == "https://legacy.example/a"
    assert req["site_id"] is None

def test_generic_identity_passthrough():
    req = normalize_generic({"site":{"site_id":"S2","site_name":"N","site_url":"https://s.example"},"ArticleID":"A2","ArticleURL":"https://s.example/a","main_query":"q"})
    assert req["site_id"] == "S2" and req["article_id"] == "A2"

def test_feedback_optional_identity_is_transparent():
    fb = build_feedback(article_id="A1", article_url="https://e/a", main_query="q", before_after=[], summary="s", warnings=[], site_id="S1", site_name="N", site_url="https://e")
    assert fb["site_id"] == "S1" and fb["article_id"] == "A1"

def test_feedback_legacy_shape_has_no_empty_site_fields():
    fb = build_feedback(article_id="A1", article_url="https://e/a", main_query="q", before_after=[], summary="s", warnings=[])
    assert "site_id" not in fb and "site_name" not in fb and "site_url" not in fb

def test_shared_editorial_assets_exist():
    required = ["Intent-Analysis.md","Hidden-Anxiety.md","Evidence-Transparency.md","SERP-Entity-Preservation.md","Internal-Link-Semantics.md","Decision-Support.md","Writer-Application-Mapping.md"]
    assert all((ROOT / "shared" / name).exists() for name in required)

def test_feedback_and_swls_schemas_accept_optional_identity():
    for rel in ["schemas/SIMS_FEEDBACK_V2.schema.json","learning/schemas/SWLS_LEARNING_RECORD.schema.json"]:
        schema=json.loads((ROOT/rel).read_text(encoding="utf-8"))
        for key in ("site_id","site_name","site_url"):
            assert key in schema["properties"]
            assert key not in schema.get("required",[])
