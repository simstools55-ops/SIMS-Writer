#!/usr/bin/env python3
from pathlib import Path
import json, yaml, sys
root=Path(__file__).resolve().parents[2]
reg=json.loads((root/'quality/registry/quality-rule-registry.json').read_text(encoding='utf-8'))
ids=set(); errors=[]
required={'id','name','dimension','severity','version','status','requirement','pass_condition','fail_condition','auto_fix_eligible'}
for item in reg['rules']:
 p=root/item['path']
 if not p.exists(): errors.append(f'missing: {p}') ; continue
 data=yaml.safe_load(p.read_text(encoding='utf-8'))
 miss=required-set(data)
 if miss: errors.append(f'{data.get("id",p.name)} missing {sorted(miss)}')
 if data.get('id') in ids: errors.append(f'duplicate id: {data.get("id")}')
 ids.add(data.get('id'))
 if data.get('severity') not in {'blocker','critical','major','minor','advisory'}: errors.append(f'invalid severity: {data.get("id")}')
for gp in (root/'quality/gates').glob('*.yaml'):
 g=yaml.safe_load(gp.read_text(encoding='utf-8'))
 for rid in g.get('required_rules',[]):
  if rid not in ids: errors.append(f'{gp.name}: unknown rule {rid}')
if len(ids)!=reg.get('rule_count'): errors.append('registry rule_count mismatch')
if errors:
 print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(ids)} rules and {len(list((root/"quality/gates").glob("*.yaml")))} gates validated')
