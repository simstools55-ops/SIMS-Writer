from runtime.sims_writer_runtime.hotfix_validation import validate_hotfix

BASE={"format":"SIMS_FEEDBACK_V2","version":"2.0","article_id":"A","article_url":"https://e.test/a","warnings":[],"validation":{"result":"PASS","warning_rules":[],"failed_rules":[]}}

def fb(**kw):
    x=dict(BASE); x.update(kw); return x

def test_a000036_main_query_and_language():
    p={"feedback":fb(new_values={"main_query":"ませてる 悪口"}),"query_metrics":[{"query":"ませてるとは","impressions":1171},{"query":"ませてる 悪口","impressions":50}],"rendered_response":"漢字（老成る）として解説"}
    issues=validate_hotfix(p)
    assert "VAL-MAINQUERY-001" in issues
    assert "VAL-LANGUAGE-001" in issues

def test_a000001_attribution_source_and_claim():
    p={"feedback":fb(new_values={"main_query":"ゲッターズ飯田 金運待ち受け"}),"main_query_was_missing":True,"rendered_response":"ゲッターズ飯田さんによると最強候補です。潜在意識に信念が根づきます。"}
    issues=validate_hotfix(p)
    assert {"VAL-MAINQUERY-001","VAL-PERSON-ATTRIBUTION-001","VAL-SOURCE-001","VAL-CLAIM-001"}.issubset(issues)

def test_a000020_warning_consistency():
    p={"feedback":fb(warnings=["LOW_SAMPLE"],validation={"result":"PASS","warning_rules":[],"failed_rules":[]})}
    assert "VAL-VALIDATION-CONSISTENCY-001" in validate_hotfix(p)

def test_a000036_link_requires_real_url():
    p={"feedback":fb(internal_link_evaluation={"added":1,"held":1,"rejected":1}),"proposed_text":"あわせて読みたい：関連記事タイトル"}
    assert "VAL-INTERNAL-LINK-001" in validate_hotfix(p)

def test_a000006_safe_clean_case():
    p={"feedback":fb(new_values={"main_query":"プリン 冷やす時間"}),"query_metrics":[{"query":"プリン 冷やす時間","impressions":17209}],"rendered_response":"数値効果は予測しません。"}
    assert validate_hotfix(p)==[]

def test_attribution_with_source_is_not_source_failure():
    p={"feedback":fb(),"rendered_response":"公式書籍で山田さんによると説明されています。","verifiable_sources":["official-book-isbn"]}
    issues=validate_hotfix(p)
    assert "VAL-PERSON-ATTRIBUTION-001" in issues
    assert "VAL-SOURCE-001" not in issues
