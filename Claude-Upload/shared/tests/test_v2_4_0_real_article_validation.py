from pathlib import Path
import json
ROOT=Path(__file__).parents[1]

def test_v240_assets_and_version():
 assert (ROOT/'VERSION').read_text().strip()=='3.5.0'
 for p in [
  'validation/real-article-publication-validation.md',
  'evidence/search-demand-evidence-boundary.md',
  'knowledge/supernatural-health-causation-safety.md',
  'knowledge/food-safety-conditional-claims.md',
  'patterns/low-sample-title-control-pattern.md',
  'patterns/winner-query-protection-pattern.md',
  'knowledge/title-promise-alignment.md',
  'knowledge/internal-link-destination-validation.md']:
  assert (ROOT/p).is_file()

def test_v240_before_and_safety_tokens():
 text=(ROOT/'validation/real-article-publication-validation.md').read_text()
 for token in ['実記事','省略記号','前回提案','完成文全文','new_values']:
  assert token in text
 safety=(ROOT/'knowledge/supernatural-health-causation-safety.md').read_text()
 assert '生霊' in safety and '医療機関' in safety

def test_v240_learning_records_and_fixtures():
 data=json.loads((ROOT/'learning/LEARNING_REGISTRY.json').read_text())
 assert data['shared_version']=='3.5.0'
 assert len([r for r in data['records'] if r['id'].startswith('LR-2026-00')])>=8
 assert len(list((ROOT/'tests/fixtures/v2_4_0').glob('*.md')))==8
