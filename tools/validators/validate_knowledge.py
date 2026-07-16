#!/usr/bin/env python3
from pathlib import Path
import yaml, sys
root=Path(__file__).resolve().parents[2]
kr=yaml.safe_load((root/'knowledge/registry/knowledge-registry.yaml').read_text(encoding='utf-8'))['knowledge']
sr={x['id'] for x in yaml.safe_load((root/'knowledge/registry/source-registry.yaml').read_text(encoding='utf-8'))['sources']}
ids=set(); errors=[]
for rec in kr:
    if rec['id'] in ids: errors.append(f"duplicate knowledge id: {rec['id']}")
    ids.add(rec['id'])
    p=root/rec['path']
    if not p.exists(): errors.append(f"missing file: {rec['path']}"); continue
    parts=p.read_text(encoding='utf-8').split('---',2)
    if len(parts)<3: errors.append(f"missing frontmatter: {p}"); continue
    d=yaml.safe_load(parts[1])
    for key in ['id','title','category','knowledge_type','version','status','confidence','source_ids','applicability','reviewed_at','next_review_at']:
        if key not in d: errors.append(f"{d.get('id',p.name)} missing {key}")
    for sid in d.get('source_ids',[]):
        if sid not in sr: errors.append(f"{d['id']} unknown source {sid}")
sets=yaml.safe_load((root/'knowledge/registry/knowledge-set-registry.yaml').read_text(encoding='utf-8'))['knowledge_sets']
for rec in sets:
    p=root/rec['path']; d=yaml.safe_load(p.read_text(encoding='utf-8'))
    for kid in d.get('required_items',[])+d.get('optional_items',[]):
        if kid not in ids: errors.append(f"{d['id']} unknown knowledge {kid}")
if errors:
    print('KNOWLEDGE VALIDATION FAILED')
    print('\n'.join(errors)); sys.exit(1)
print(f"KNOWLEDGE VALIDATION PASSED: {len(ids)} items, {len(sets)} sets, {len(sr)} sources")
