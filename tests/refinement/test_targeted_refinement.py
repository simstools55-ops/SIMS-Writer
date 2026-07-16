from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime'))
from sims_writer_runtime.quality.engine import QualityValidationEngine
from sims_writer_runtime.refinement.engine import TargetedRefinementEngine


def main():
    q=QualityValidationEngine(ROOT); r=TargetedRefinementEngine(q)
    draft={
      'seo_title':'Wi-Fi 電気代を解説','meta_description':'Wi-Fi 電気代を説明します。','h1':'Wi-Fi 電気代',
      'introduction':'見ていきましょう。TODO Wi-Fi 電気代の答えを説明します。',
      'article_content':'Wi-Fiルーターの電気代を確認する説明です。Wi-Fiルーターの電気代を確認する説明です。Wi-Fiルーターの電気代を確認する説明です。ぜひ参考にしてみてください。',
      'sections':[{'level':2,'heading':'概要','content':'説明'},{'level':4,'heading':'詳細','content':'説明'}],
      'unresolved_items':[]
    }
    first=q.evaluate(draft,{'main_query':'Wi-Fi 電気代'})
    result=r.refine(draft,first,{'main_query':'Wi-Fi 電気代'})
    revised=result['revised_draft']
    assert 'TODO' not in revised['introduction']
    assert '見ていきましょう' not in revised['introduction']
    assert revised['article_content'].count('Wi-Fiルーターの電気代を確認する説明です。')==1
    assert revised['sections'][1]['level']==3
    assert result['revision_records']
    print('targeted refinement tests passed')

if __name__=='__main__': main()
