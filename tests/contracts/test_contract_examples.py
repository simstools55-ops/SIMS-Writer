#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver
ROOT=Path(__file__).resolve().parents[2]
reg=json.loads((ROOT/'contracts/registry/contract-registry.json').read_text(encoding='utf-8'))
failed=0
for c in reg['contracts']:
    schema_path=ROOT/c['schema']; schema=json.loads(schema_path.read_text(encoding='utf-8'))
    common=json.loads((ROOT/'schemas/common/common.schema.json').read_text(encoding='utf-8'))
    resolver=RefResolver(base_uri=schema_path.parent.as_uri()+'/',referrer=schema,store={'https://sims-writer.local/schemas/common/common.schema.json':common})
    v=Draft202012Validator(schema,resolver=resolver)
    valid=json.loads((schema_path.parent/'examples/valid.json').read_text(encoding='utf-8'))
    invalid=json.loads((schema_path.parent/'examples/invalid.json').read_text(encoding='utf-8'))
    if list(v.iter_errors(valid)):
        print('VALID FAILED',c['id']); failed+=1
    if not list(v.iter_errors(invalid)):
        print('INVALID PASSED',c['id']); failed+=1
print(f'contracts={len(reg["contracts"])} failed={failed}')
raise SystemExit(1 if failed else 0)
