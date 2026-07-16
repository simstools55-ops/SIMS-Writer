#!/usr/bin/env python3
from pathlib import Path
import json, sys
from jsonschema import Draft202012Validator, FormatChecker
root=Path(__file__).resolve().parents[2]
items=[('decision/context','context','decision-context'),('decision/record','record','decision-record'),('decision/action-plan','action-plan','decision-action-plan')]
for path,schema_name,example_name in items:
 schema=json.loads((root/f'contracts/{path}/{schema_name}.schema.json').read_text(encoding='utf-8'))
 v=Draft202012Validator(schema,format_checker=FormatChecker())
 valid=json.loads((root/f'examples/decisions/{example_name}.valid.json').read_text(encoding='utf-8'))
 invalid=json.loads((root/f'examples/decisions/{example_name}.invalid.json').read_text(encoding='utf-8'))
 assert not list(v.iter_errors(valid)), example_name
 assert list(v.iter_errors(invalid)), example_name+' invalid not rejected'
print('Decision contract tests: PASS')
