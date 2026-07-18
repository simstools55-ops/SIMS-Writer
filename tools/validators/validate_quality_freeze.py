import json
from pathlib import Path

def validate_semantics(data: dict) -> list[str]:
    errors=[]
    budget=data.get('change_budget_percent')
    actual=data.get('validation',{}).get('estimated_change_percent')
    if isinstance(budget,int) and isinstance(actual,int) and actual>budget:
        errors.append('VAL-BUDGET-001')
    if data.get('validation',{}).get('status')=='FAIL' and data.get('decision') not in {'REVIEW_REQUIRED','BLOCK'}:
        errors.append('VAL-CONTRACT-001: FAIL decision mismatch')
    if 'LOW_SAMPLE' in data.get('diagnosis',[]) and data.get('confidence')=='high':
        errors.append('VAL-SAMPLE-001: LOW_SAMPLE cannot be high confidence')
    flags=data.get('change_flags',{})
    targets={c.get('target') for c in data.get('changes',[])}
    mapping={'seo_title':'seo_title','meta_description':'meta_description','introduction':'introduction','heading':'headings','body':'body','faq':'faq','internal_link':'internal_links','conclusion':'conclusion'}
    expected={k:False for k in flags}
    for t in targets:
        if t in mapping and mapping[t] in expected: expected[mapping[t]]=True
    for k,v in expected.items():
        if flags.get(k)!=v: errors.append(f'VAL-FLAG-001:{k}')
    return errors
