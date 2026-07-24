#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
SUITE=ROOT/'tests/regression/official-v1'

def main():
    manifest=json.loads((SUITE/'manifest.json').read_text(encoding='utf-8'))
    rows=[]; failed=0
    for item in manifest['cases']:
        spec=json.loads((SUITE/item['case_spec']).read_text(encoding='utf-8'))
        case_dir=(SUITE/item['case_spec']).parent
        missing=[n for n in ('input.md','original_output.md') if not (case_dir/n).exists()]
        if missing:
            status='SKIP'; detail='missing: '+', '.join(missing)
        elif not spec.get('required_findings'):
            status='FAIL'; detail='required_findings is empty'; failed+=1
        else:
            status='READY'; detail=f"expected {spec['expected_initial_verdict']} -> {spec['expected_final_verdict']}"
        rows.append((spec['case_id'],status,detail))
    for row in rows: print(f"{row[0]}	{row[1]}	{row[2]}")
    print(f"SUMMARY total={len(rows)} ready={sum(r[1]=='READY' for r in rows)} skip={sum(r[1]=='SKIP' for r in rows)} fail={failed}")
    return 1 if failed else 0
if __name__=='__main__': sys.exit(main())
