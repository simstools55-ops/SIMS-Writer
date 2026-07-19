#!/usr/bin/env python3
"""Generate SWLS 10-article reports (Markdown, JSON, CSV)."""
from __future__ import annotations
import argparse, csv, json
from collections import Counter, defaultdict
from pathlib import Path

def load_dir(path: Path, suffix: str):
    out={}
    if not path.exists(): return out
    for p in sorted(path.glob(f"*{suffix}")):
        try:
            d=json.loads(p.read_text(encoding="utf-8")); out[d["article_id"]]=d
        except Exception as e:
            raise SystemExit(f"Invalid JSON: {p}: {e}")
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--records',type=Path,required=True); ap.add_argument('--feedback',type=Path,required=True)
    ap.add_argument('--measurements',type=Path,required=True); ap.add_argument('--batch',required=True); ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); a.output.mkdir(parents=True,exist_ok=True)
    records=[r for r in load_dir(a.records,'.learning.json').values() if r.get('batch_key')==a.batch]
    if len(records)!=10: raise SystemExit(f"Batch {a.batch} requires exactly 10 records; found {len(records)}")
    feedback=load_dir(a.feedback,'.feedback.json'); measurements=load_dir(a.measurements,'.measurement.json')
    decisions=Counter(r['decision'] for r in records); diagnoses=Counter(x for r in records for x in r.get('diagnosis',[]))
    warnings=Counter(x for r in records for x in r.get('validation_rules',{}).get('warnings',[])); failures=Counter(x for r in records for x in r.get('validation_rules',{}).get('failed',[]))
    targets=Counter(x for r in records for x in r.get('change_targets',[])); ratings=[]; adoptions=Counter(); tags=Counter(); comments=[]
    for r in records:
        f=feedback.get(r['article_id'])
        if f:
            ratings.append(f['rating']); adoptions[f['adoption']]+=1; tags.update(f.get('tags',[]))
            if f.get('comment'): comments.append({'article_id':r['article_id'],'comment':f['comment']})
    deltas=[]
    for r in records:
        m=measurements.get(r['article_id'])
        if m:
            b,aft=m['before'],m['after']; deltas.append({'article_id':r['article_id'],'ctr_delta':round(aft['ctr_percent']-b['ctr_percent'],4),'position_delta':round(aft['position']-b['position'],4),'click_delta':aft['clicks']-b['clicks'],'impression_delta':aft['impressions']-b['impressions']})
    cand=defaultdict(lambda:{'count':0,'evidence':[],'confidence':Counter()})
    for r in records:
        for c in r.get('learning_candidates',[]):
            key=(c['target'],c['proposal']); cand[key]['count']+=1; cand[key]['evidence'].append(c['evidence']); cand[key]['confidence'][c['confidence']]+=1
    candidates=[{'target':k[0],'proposal':k[1],'occurrences':v['count'],'status':'REVIEW_CANDIDATE' if v['count']>=3 else 'OBSERVE','confidence_counts':dict(v['confidence']),'evidence':v['evidence']} for k,v in sorted(cand.items(),key=lambda kv:(-kv[1]['count'],kv[0]))]
    summary={'format':'SWLS_BATCH_REPORT','version':'1.0-beta','batch_key':a.batch,'article_count':10,'decisions':dict(decisions),'diagnoses':dict(diagnoses),'validation_warnings':dict(warnings),'validation_failures':dict(failures),'change_targets':dict(targets),'user_feedback':{'responses':len(ratings),'average_rating':round(sum(ratings)/len(ratings),2) if ratings else None,'adoption':dict(adoptions),'tags':dict(tags),'comments':comments},'measurements':{'responses':len(deltas),'deltas':deltas},'learning_candidates':candidates}
    base=a.output/f"SWLS_{a.batch}_Report"
    base.with_suffix('.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=[f"# SWLS {a.batch} 運用レポート","",f"対象記事：10件","","## 品質判定"]
    md += [f"- {k}: {v}件" for k,v in sorted(decisions.items())]
    md += ["","## 主なValidation Warning"]+[f"- {k}: {v}件" for k,v in warnings.most_common()] or ['- なし']
    md += ["","## 変更箇所"]+[f"- {k}: {v}件" for k,v in targets.most_common()]
    md += ["","## 利用者評価",f"- 回答数: {len(ratings)}件",f"- 平均評価: {summary['user_feedback']['average_rating']}"]
    md += ["","## 改善候補"]+[f"- [{c['status']}] {c['target']}: {c['proposal']}（{c['occurrences']}件）" for c in candidates]
    md += ["","## 実測データ",f"- 測定済み: {len(deltas)}件"]
    base.with_suffix('.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    with base.with_suffix('.csv').open('w',encoding='utf-8-sig',newline='') as fh:
        w=csv.writer(fh); w.writerow(['article_id','decision','diagnosis','change_targets','warning_rules','user_rating','adoption','ctr_delta','position_delta','comment'])
        dmap={d['article_id']:d for d in deltas}
        for r in records:
            f=feedback.get(r['article_id'],{}); d=dmap.get(r['article_id'],{})
            w.writerow([r['article_id'],r['decision'],'|'.join(r.get('diagnosis',[])),'|'.join(r.get('change_targets',[])),'|'.join(r.get('validation_rules',{}).get('warnings',[])),f.get('rating',''),f.get('adoption',''),d.get('ctr_delta',''),d.get('position_delta',''),f.get('comment','')])
    print(base.with_suffix('.md')); print(base.with_suffix('.json')); print(base.with_suffix('.csv'))
if __name__=='__main__': main()
