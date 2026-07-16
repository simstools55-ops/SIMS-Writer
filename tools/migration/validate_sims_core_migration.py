from pathlib import Path
import sys, yaml
ROOT=Path(__file__).resolve().parents[2]
inv=yaml.safe_load((ROOT/'migrations/sims-core/migration-inventory.yaml').read_text(encoding='utf-8'))
reg=yaml.safe_load((ROOT/'knowledge/lessons-learned/sims-core/registry.yaml').read_text(encoding='utf-8'))
errors=[]
ids=[]
for a in inv.get('assets',[]):
    ids.append(a.get('id'))
    if a.get('classification') not in {'keep','adapt','archive','remove'}: errors.append(f"invalid classification: {a.get('id')}")
    if not a.get('reason'): errors.append(f"missing reason: {a.get('id')}")
if len(ids)!=len(set(ids)): errors.append('duplicate asset id')
lesson_ids=[]
for l in reg.get('lessons',[]):
    lesson_ids.append(l.get('id'))
    p=ROOT/l.get('path','')
    if not p.exists(): errors.append(f'missing lesson file: {p}')
if len(lesson_ids)!=len(set(lesson_ids)): errors.append('duplicate lesson id')
print(f"SIMS-Core assets: {len(ids)}")
print(f"Lessons learned: {len(lesson_ids)}")
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('SIMS-Core migration validation: PASS')
