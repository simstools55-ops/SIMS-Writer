from pathlib import Path
import json

def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))

def build_manifest(repo_root: Path) -> dict:
    def count_registry(rel: str, key: str) -> int:
        path = repo_root / rel
        if not path.exists(): return 0
        obj = _load_json(path)
        value = obj.get(key, []) if isinstance(obj, dict) else []
        return len(value)
    version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    return {
        "runtime_version": version,
        "asset_lock": {
            "contracts": count_registry("contracts/registry/contract-registry.json", "contracts"),
            "quality_rules": count_registry("quality/registry/quality-rule-registry.json", "rules"),
            "quality_gates": count_registry("quality/registry/quality-gate-registry.json", "gates"),
            "decisions": count_registry("decision/registry/decision-registry.json", "decisions"),
            "patterns": count_registry("patterns/registry/pattern-registry.json", "patterns"),
            "pattern_sets": count_registry("patterns/registry/pattern-set-registry.json", "pattern_sets"),
        },
    }
