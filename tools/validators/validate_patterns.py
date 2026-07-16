#!/usr/bin/env python3
import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[2]
reg=json.loads((root/'patterns/registry/pattern-registry.json').read_text(encoding='utf-8'))
dec={x['id'] for x in json.loads((root/'decision/registry/decision-registry.json').read_text(encoding='utf-8'))['decisions']}
kn=set()
for p in (root/'knowledge').rglob('*.md'):
    for line in p.read_text(encoding='utf-8').splitlines():
        if line.startswith('id: KN-'): kn.add(line.split(':',1)[1].strip())
qf={x['id'] for x in json.loads((root/'quality/registry/quality-rule-registry.json').read_text(encoding='utf-8'))['rules']}
ids=set(); errors=[]
for item in reg['patterns']:
    if item['id'] in ids: errors.append('duplicate '+item['id'])
    ids.add(item['id'])
    p=root/item['path']
    if not p.exists(): errors.append('missing '+str(p)); continue
    d=json.loads(p.read_text(encoding='utf-8'))
    required=['id','name','category','problem','applicability','non_applicability','required_inputs','method','expected_outputs','quality_criteria','related_decisions','related_knowledge','related_quality_rules','version','status']
    for k in required:
        if k not in d: errors.append(f"{d.get('id')}: missing {k}")
    for x in d.get('related_decisions',[]):
        if x not in dec: errors.append(f"{d['id']}: unknown decision {x}")
    for x in d.get('related_knowledge',[]):
        if x not in kn: errors.append(f"{d['id']}: unknown knowledge {x}")
    for x in d.get('related_quality_rules',[]):
        if x not in qf: errors.append(f"{d['id']}: unknown quality {x}")
sets=json.loads((root/'patterns/registry/pattern-set-registry.json').read_text(encoding='utf-8'))['pattern_sets']
for s in sets:
    d=json.loads((root/s['path']).read_text(encoding='utf-8'))
    for x in d['required_patterns']+d['optional_patterns']:
        if x not in ids: errors.append(f"{d['id']}: unknown pattern {x}")
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f"Pattern validation passed: {len(ids)} patterns, {len(sets)} sets")
