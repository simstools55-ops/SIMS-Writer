from runtime.sims_writer_runtime.schema_normalizer import normalize_feedback
def test_aliases_are_normalized():
 o=normalize_feedback({"diagnosis_code":"QUERY_MIX","change_flags":{"seo_title":True},"validation":{},"warnings":[""],"information":None})
 assert o["contract_version"]=="2.1" and "diagnosis_code" not in o and "change_flags" not in o
 assert o["diagnosis"]["code"]=="QUERY_MIX" and o["changes"][0]["status"]=="implemented"
 assert set(o["query_coverage"])=={"confidence","primary","secondary","adjacent","separate_article"}
