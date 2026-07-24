from runtime.sims_writer_runtime.adapters.input_adapters import parse_search_console_query_data, normalize_sbm

BLOCK="""==================================================
Search Console Query Data
DataTimestamp : 2026-07-24 10:32 JST
QueryRows : 3
CapturedImp : 62
TotalImp : 70
Coverage : 88.57%
Query|Clicks|Impressions|CTR|Position
alpha|9|26|34.62|2.0
beta|7|31|22.58|2.3
broken|x|5|0.00|2.1
gamma|0|5|0.00|2.1
=================================================="""

def test_high_coverage_and_partial_invalid_rows():
    d=parse_search_console_query_data(BLOCK)
    assert d["present"] and d["coverage_confidence"]=="HIGH_COVERAGE"
    assert len(d["rows"])==3 and len(d["invalid_rows"])==1
    assert d["row_count_matches_declared"] is True

def test_low_and_unknown_coverage():
    low=parse_search_console_query_data(BLOCK.replace("88.57%","28.00%"))
    assert low["coverage_confidence"]=="LOW_COVERAGE"
    assert parse_search_console_query_data("legacy request")["coverage_confidence"]=="COVERAGE_UNKNOWN"

def test_limit_200_rows():
    rows="\n".join(f"q{i}|0|1|0|10" for i in range(250))
    d=parse_search_console_query_data("Search Console Query Data\nQuery|Clicks|Impressions|CTR|Position\n"+rows)
    assert len(d["rows"])==200

def test_sbm_normalizer_accepts_request_text():
    req=normalize_sbm({"MainQuery":"alpha","ImprovementRequest":BLOCK})
    assert req["search_console_query_data"]["rows"][0]["query"]=="alpha"
