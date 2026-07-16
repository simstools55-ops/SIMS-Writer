from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime'))
from sims_writer_runtime.quality.engine import QualityValidationEngine

def main():
    e=QualityValidationEngine(ROOT)
    good={'seo_title':'Wi-Fiルーターの電気代を解説','meta_description':'Wi-Fiルーターの電気代と確認方法を解説します。','h1':'Wi-Fiルーターの電気代','introduction':'Wi-Fiルーターの電気代は、消費電力から確認できます。この記事では計算方法を説明します。','article_content':'Wi-Fiルーターの電気代は消費電力を確認して計算します。手順を順番に説明します。','sections':[{'level':2,'heading':'確認方法','content':'消費電力を確認します。'}],'unresolved_items':[]}
    r=e.evaluate(good,{'main_query':'Wi-Fi 電気代'})
    assert r['rules_evaluated']==42, r['rules_evaluated']
    assert len(r['gate_results'])==7, len(r['gate_results'])
    bad=dict(good); bad['article_content']='TODO 後で追加'; bad['unresolved_items']=['price']
    rb=e.evaluate(bad,{'main_query':'Wi-Fi 電気代'})
    assert any(x['rule_id']=='QF-PUB-001' and x['result']=='fail' for x in rb['checks'])
    assert rb['publish_recommendation']=='revision_required'
    print('quality runtime tests passed: 42 rules / 7 gates')
if __name__=='__main__': main()
