from pathlib import Path
from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback
from runtime.sims_writer_runtime.localization import user_facing_term

def test_changes_are_canonical_and_empty_values_removed():
    out=normalize_feedback({"changes":[{"target":"seo_title","implementation_status":"implemented","before":"旧","after":"新","reason":"理由"},{"target":"faq","implementation_status":"not_applicable","before":"","after":""}],"validation":{"checks":[{"code":"VAL-X","status":"PASS","message":""}]}})
    assert out["changes"]==[{"component":"seo_title","implementation_status":"implemented","before":"旧","after":"新","reason":"理由"}]
    assert out["validation"]["checks"][0]["message"]

def test_japanese_first_use_label():
    assert user_facing_term("POSITION_OPPORTUNITY",True)=="掲載順位を生かしたクリック改善機会（POSITION_OPPORTUNITY）"
    assert user_facing_term("POSITION_OPPORTUNITY",False)=="掲載順位を生かしたクリック改善機会"

def test_release_cleaner_exists_and_gitignore_excludes_cache():
    root=Path(__file__).resolve().parents[2]
    assert (root/"tools/release_cleaner.py").exists()
    g=(root/".gitignore").read_text(encoding="utf-8")
    assert ".pytest_cache/" in g and "*.pyc" in g
