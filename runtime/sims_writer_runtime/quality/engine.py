from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json, re
try:
    import yaml
except ImportError:
    yaml = None

PLACEHOLDERS = ("TODO", "TBD", "要確認", "後で追加", "{{", "}}", "[PLACEHOLDER]")
AI_PHRASES = ("いかがでしたでしょうか", "見ていきましょう", "ぜひ参考にしてみてください", "重要なポイントとなります")
HIGH_RISK = ("医療", "治療", "投資", "法律", "診断", "薬", "保証します")
DANGER = ("レジストリ", "初期化", "削除", "感電", "分解", "データ消失")

@dataclass
class CheckResult:
    rule_id: str
    dimension: str
    severity: str
    result: str
    component: str
    description: str
    evidence: list[str]
    required_action: str | None = None
    auto_fix_eligible: bool = False
    def to_dict(self): return asdict(self)

class QualityValidationEngine:
    """42 canonical rulesを読み込み、決定論的検査と明示的な検証不能判定を行う。"""
    def __init__(self, repo_root: Path):
        self.repo_root=Path(repo_root)
        self.rules=self._load_rules()
        self.gates=self._load_gates()

    def _load_rules(self):
        rows=[]
        for p in sorted((self.repo_root/'quality/rules').rglob('*.yaml')):
            rows.append(yaml.safe_load(p.read_text(encoding='utf-8')))
        return rows

    def _load_gates(self):
        rows=[]
        for p in sorted((self.repo_root/'quality/gates').glob('*.yaml')):
            rows.append(yaml.safe_load(p.read_text(encoding='utf-8')))
        return rows

    @staticmethod
    def _text(draft):
        parts=[draft.get(k) or '' for k in ('seo_title','meta_description','h1','introduction','article_content','conclusion')]
        for s in draft.get('sections') or []:
            if isinstance(s,dict): parts += [str(s.get('heading','')),str(s.get('content',''))]
            else: parts.append(str(s))
        return '\n'.join(parts).strip()

    def evaluate(self, draft:dict[str,Any], context:dict[str,Any]|None=None)->dict[str,Any]:
        context=context or {}; text=self._text(draft); main_query=str(context.get('main_query') or '').strip()
        checks=[self._evaluate_rule(r,draft,text,main_query,context) for r in self.rules]
        issues=[c.to_dict() for c in checks if c.result in ('fail','warning','unable_to_verify')]
        gate_results=[]
        by_id={c.rule_id:c for c in checks}
        for gate in self.gates:
            ids=gate.get('required_rules') or gate.get('rules') or []
            rel=[by_id[i] for i in ids if i in by_id]
            blocker=any(c.result=='fail' and c.severity in ('blocker','critical') for c in rel)
            fail=any(c.result=='fail' for c in rel)
            unable=any(c.result=='unable_to_verify' and c.severity in ('blocker','critical') for c in rel)
            status='fail' if blocker or unable else ('warning' if fail or any(c.result in ('warning','unable_to_verify') for c in rel) else 'pass')
            gate_results.append({'gate_id':gate.get('id'),'name':gate.get('name'),'status':status,'evaluated_rules':[c.rule_id for c in rel]})
        blockers=[i for i in issues if i['result']=='fail' and i['severity']=='blocker']
        critical=[i for i in issues if i['result']=='fail' and i['severity']=='critical']
        unver_major=[i for i in issues if i['result']=='unable_to_verify' and i['severity'] in ('blocker','critical')]
        failures=[i for i in issues if i['result']=='fail']
        if blockers or critical or unver_major: decision='revision_required'
        elif failures: decision='revision_required'
        elif any(i['result'] in ('warning','unable_to_verify') for i in issues): decision='publish_ready_with_advisory'
        else: decision='publish_ready'
        dim={}
        for c in checks:
            dim.setdefault(c.dimension,[]).append(c)
        scores={k: round(5*sum(1 if x.result=='pass' else .7 if x.result=='warning' else .4 if x.result=='unable_to_verify' else 0 for x in v)/len(v),2) for k,v in dim.items()}
        return {'framework_version':'1.0.0','rules_evaluated':len(checks),'checks':[c.to_dict() for c in checks],
                'issues':issues,'gate_results':gate_results,'dimension_scores':scores,
                'summary':{'pass':sum(c.result=='pass' for c in checks),'fail':sum(c.result=='fail' for c in checks),'warning':sum(c.result=='warning' for c in checks),'unable_to_verify':sum(c.result=='unable_to_verify' for c in checks)},
                'blockers':blockers,'critical_issues':critical,'publish_recommendation':decision}

    def _r(self,r,result,component,desc,evidence=None,action=None):
        return CheckResult(r['id'],r['dimension'],r['severity'],result,component,desc,evidence or [],action,bool(r.get('auto_fix_eligible')))

    def _evaluate_rule(self,r,d,t,q,c):
        rid=r['id']; low=t.lower(); title=str(d.get('seo_title') or ''); h1=str(d.get('h1') or ''); meta=str(d.get('meta_description') or '')
        sections=d.get('sections') or []; unresolved=d.get('unresolved_items') or []
        # publication / structural deterministic
        if rid=='QF-PUB-001':
            hits=[x for x in PLACEHOLDERS if x in t]; return self._r(r,'fail' if hits else 'pass','article','プレースホルダー検査',hits,'プレースホルダーを解消する' if hits else None)
        if rid=='QF-PUB-002':
            miss=[k for k,v in [('seo_title',title),('meta_description',meta),('h1',h1),('article_content',d.get('article_content'))] if not v]; return self._r(r,'fail' if miss else 'pass','metadata','必須公開要素の検査',miss,'不足項目を作成する' if miss else None)
        if rid=='QF-PUB-003': return self._r(r,'fail' if unresolved else 'pass','article','未解決項目の検査',[str(x) for x in unresolved], '未解決項目を処理する' if unresolved else None)
        if rid=='QF-PUB-004': return self._r(r,'fail' if unresolved or not t else 'pass','article','追加編集要否の構造検査',[])
        if rid=='QF-STR-001':
            levels=[int(s.get('level',2)) for s in sections if isinstance(s,dict) and str(s.get('level',2)).isdigit()]; bad=any(b-a>1 for a,b in zip(levels,levels[1:])); return self._r(r,'fail' if bad else 'pass','headings','見出し階層検査',[str(levels)])
        if rid=='QF-REA-002':
            paras=[p for p in re.split(r'\n\s*\n',t) if p]; longest=max(map(len,paras),default=0); return self._r(r,'warning' if longest>500 else 'pass','article','段落長検査',[f'longest={longest}'])
        if rid=='QF-REA-001':
            sent=[x for x in re.split(r'[。！？]',t) if x.strip()]; longest=max(map(len,sent),default=0); return self._r(r,'warning' if longest>140 else 'pass','article','文長検査',[f'longest={longest}'])
        if rid=='QF-JPN-003':
            hits=[x for x in AI_PHRASES if x in t]; return self._r(r,'warning' if hits else 'pass','article','定型的AI表現検査',hits)
        if rid=='QF-SEO-001':
            ok=bool(title and (not q or any(tok.lower() in title.lower() for tok in q.split()))); return self._r(r,'pass' if ok else 'fail','seo_title','タイトルと検索意図の整合',[q,title])
        if rid=='QF-SEO-002':
            count=sum(low.count(tok.lower()) for tok in q.split()) if q else 0; density=count/max(len(t)/100,1); return self._r(r,'warning' if density>4 else 'pass','article','クエリ反復検査',[f'count={count}',f'density={density:.2f}'])
        if rid=='QF-INT-001':
            ok=bool(t and (not q or any(tok.lower() in low for tok in q.split()))); return self._r(r,'pass' if ok else 'fail','article','Primary Intent回答検査',[q])
        if rid=='QF-INT-002':
            intro=str(d.get('introduction') or d.get('article_content') or '')[:500]; return self._r(r,'pass' if len(intro.strip())>=30 else 'fail','introduction','Main Answer明示の近似検査',[f'intro_length={len(intro)}'])
        if rid=='QF-FAC-003':
            return self._r(r,'warning' if title and h1 and title.strip()==h1.strip() else 'pass','article','内部整合の基礎検査',[])
        if rid=='QF-FAC-001':
            volatile=bool(re.search(r'20\d{2}|最新|料金|価格|現在',t)); sources=d.get('citations') or c.get('sources') or []; return self._r(r,'unable_to_verify' if volatile and not sources else 'pass','article','時点依存情報の根拠検査',[f'volatile={volatile}',f'sources={len(sources)}'])
        if rid=='QF-FAC-002':
            nums=re.findall(r'\d+(?:\.\d+)?(?:円|%|％|GB|MB|回|年|月|日)',t); sources=d.get('citations') or c.get('sources') or []; return self._r(r,'unable_to_verify' if nums and not sources else 'pass','article','数値主張の根拠検査',nums[:10])
        if rid=='QF-SAF-002':
            hits=[x for x in HIGH_RISK if x in t]; return self._r(r,'unable_to_verify' if hits else 'pass','article','高リスク主張検査',hits)
        if rid=='QF-SAF-003':
            dangerous=any(x in t for x in ('初期化','削除','レジストリ')); warning=any(x in t for x in ('バックアップ','注意','失われ'))
            return self._r(r,'fail' if dangerous and not warning else 'pass','article','データ損失警告検査',[f'dangerous={dangerous}',f'warning={warning}'])
        if rid=='QF-SAF-001':
            return self._r(r,'unable_to_verify' if any(x in t for x in DANGER) else 'pass','article','危険手順の文脈検査',[])
        if rid=='QF-ORG-003':
            fabricated=bool(re.search(r'私が(?:実際に|使って|試して)',t)) and not c.get('experience_verified'); return self._r(r,'fail' if fabricated else 'pass','article','体験主張の真正性検査',[])
        if rid=='QF-EEA-003':
            false=any(x in t for x in ('専門家として断言','必ず治る','絶対に儲かる')); return self._r(r,'fail' if false else 'pass','article','虚偽専門性検査',[])
        if rid=='QF-REA-003':
            sents=[x.strip() for x in re.split(r'[。！？]',t) if len(x.strip())>15]; dup=len(sents)-len(set(sents)); return self._r(r,'warning' if dup>1 else 'pass','article','重複文検査',[f'duplicates={dup}'])
        # Rules requiring semantic/editorial judgment: execute and expose inability rather than fabricate a pass.
        semantic={'QF-COM-001','QF-COM-002','QF-COM-003','QF-HLP-001','QF-HLP-002','QF-HLP-003','QF-JPN-001','QF-JPN-002','QF-ORG-001','QF-ORG-002','QF-EEA-001','QF-EEA-002','QF-INT-003','QF-SEO-003','QF-SEO-004','QF-SIT-001','QF-SIT-002','QF-SIT-003','QF-STR-002','QF-STR-003','QF-FAC-004'}
        if rid in semantic:
            evidence=(c.get('model_assisted_checks') or {}).get(rid)
            if evidence in ('pass','fail','warning'): return self._r(r,evidence,'article','モデル支援評価',[])
            return self._r(r,'unable_to_verify','article','文脈評価用のModel-Assisted Reviewer結果が未提供',[], 'Model-Assisted Reviewerまたは人間レビューを実行する')
        return self._r(r,'unable_to_verify','article','評価器未定義',[])
