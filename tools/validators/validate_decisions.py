#!/usr/bin/env python3
from pathlib import Path
import json, sys
try:
 import yaml
except ImportError:
 print("PyYAML is required", file=sys.stderr); sys.exit(2)
root=Path(__file__).resolve().parents[2]
reg=json.loads((root/'decision/registry/decision-registry.json').read_text(encoding='utf-8'))
errors=[]; ids=set()
required={'id','name','category','version','status','problem','applicability','non_applicability','required_inputs','evaluation_method','allowed_results','required_evidence','confidence_policy','related_knowledge','related_quality_rules','output_contract','reviewed_at','next_review_at','owner'}
for e in reg['decisions']:
 p=root/e['path']
 if not p.exists(): errors.append(f"missing: {e['path']}"); continue
 d=yaml.safe_load(p.read_text(encoding='utf-8'))
 miss=required-set(d)
 if miss: errors.append(f"{d.get('id')}: missing {sorted(miss)}")
 if d.get('id') in ids: errors.append(f"duplicate id: {d.get('id')}")
 ids.add(d.get('id'))
 if d.get('id')!=e['id']: errors.append(f"registry mismatch: {e['id']}")
 if d.get('output_contract')!='CT-DEC-002': errors.append(f"{d.get('id')}: invalid output contract")
print(f"Decision definitions: {len(ids)}")
if errors:
 print("\n".join(errors)); sys.exit(1)
print("Decision validation: PASS")
