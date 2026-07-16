#!/usr/bin/env python3
"""Validate a JSON file against a SIMS Writer contract schema."""
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

def main():
    if len(sys.argv)!=3:
        print("Usage: validate_contract.py <schema.json> <data.json>")
        return 2
    schema_path=Path(sys.argv[1]).resolve(); data_path=Path(sys.argv[2]).resolve()
    schema=json.loads(schema_path.read_text(encoding="utf-8")); data=json.loads(data_path.read_text(encoding="utf-8"))
    common_path=Path(__file__).resolve().parents[2]/'schemas/common/common.schema.json'
    common=json.loads(common_path.read_text(encoding='utf-8'))
    resolver=RefResolver(base_uri=schema_path.parent.as_uri()+"/", referrer=schema, store={'https://sims-writer.local/schemas/common/common.schema.json': common})
    errors=sorted(Draft202012Validator(schema,resolver=resolver).iter_errors(data), key=lambda e:list(e.path))
    if errors:
        for e in errors: print(f"FAIL {'.'.join(map(str,e.path)) or '<root>'}: {e.message}")
        return 1
    print("PASS")
    return 0
if __name__=='__main__': raise SystemExit(main())
