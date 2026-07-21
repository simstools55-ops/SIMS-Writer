#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[2]


def validate_contract_examples() -> tuple[int, list[str]]:
    reg = json.loads((ROOT / 'contracts/registry/contract-registry.json').read_text(encoding='utf-8'))
    failures: list[str] = []
    common = json.loads((ROOT / 'schemas/common/common.schema.json').read_text(encoding='utf-8'))
    for contract in reg['contracts']:
        schema_path = ROOT / contract['schema']
        schema = json.loads(schema_path.read_text(encoding='utf-8'))
        resolver = RefResolver(
            base_uri=schema_path.parent.as_uri() + '/',
            referrer=schema,
            store={'https://sims-writer.local/schemas/common/common.schema.json': common},
        )
        validator = Draft202012Validator(schema, resolver=resolver)
        valid = json.loads((schema_path.parent / 'examples/valid.json').read_text(encoding='utf-8'))
        invalid = json.loads((schema_path.parent / 'examples/invalid.json').read_text(encoding='utf-8'))
        if list(validator.iter_errors(valid)):
            failures.append(f"VALID FAILED {contract['id']}")
        if not list(validator.iter_errors(invalid)):
            failures.append(f"INVALID PASSED {contract['id']}")
    return len(reg['contracts']), failures


def test_contract_examples() -> None:
    count, failures = validate_contract_examples()
    assert not failures, f"contracts={count}; " + '; '.join(failures)


if __name__ == '__main__':
    count, failures = validate_contract_examples()
    print(f'contracts={count} failed={len(failures)}')
    for failure in failures:
        print(failure)
    raise SystemExit(1 if failures else 0)
