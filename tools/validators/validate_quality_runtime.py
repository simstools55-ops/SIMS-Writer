from pathlib import Path
import sys,json,argparse
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime'))
from sims_writer_runtime.quality.engine import QualityValidationEngine
p=argparse.ArgumentParser(); p.add_argument('draft'); p.add_argument('--query',default=''); a=p.parse_args()
d=json.loads(Path(a.draft).read_text(encoding='utf-8'))
print(json.dumps(QualityValidationEngine(ROOT).evaluate(d,{'main_query':a.query}),ensure_ascii=False,indent=2))
