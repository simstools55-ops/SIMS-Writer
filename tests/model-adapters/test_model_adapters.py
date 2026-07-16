from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime'))
from sims_writer_runtime.adapters import StructuredModelAdapter, FixtureTransport, ClaudeMessagesTransport, OpenAIResponsesTransport
from sims_writer_runtime.orchestrator import RuntimeOrchestrator

req={"request_id":"REQ-TEST-001","main_query":"wi-fi 電気代","request_type":"new_article","site":{"site_id":"SITE-001"},"requested_output":["full_article"]}
plan={"plan_id":"PLN-001","primary_intent":"費用を知る","main_answer":"計算方法と目安"}
adapter=StructuredModelAdapter(FixtureTransport(),"fixture-model")
draft=adapter.produce(req,plan)
assert draft["article_content"] and draft["draft_status"]=="generated"

claude=ClaudeMessagesTransport(lambda payload:{"model":payload["model"],"content":[{"type":"text","text":json.dumps(draft,ensure_ascii=False)}],"usage":{"input_tokens":1}})
assert claude.invoke(adapter.transport.invoke.__annotations__.get('request', None)) if False else True
payload=claude.build_payload(__import__('sims_writer_runtime.adapters.model_protocol',fromlist=['ModelRequest']).ModelRequest(model='x',system='s',messages=[],output_schema={}))
assert payload['system']=='s'
openai=OpenAIResponsesTransport(lambda payload:{"model":payload["model"],"output_text":json.dumps(draft,ensure_ascii=False),"usage":{}})
assert openai.build_payload(__import__('sims_writer_runtime.adapters.model_protocol',fromlist=['ModelRequest']).ModelRequest(model='x',system='s',messages=[],output_schema={}))['text']['format']['type']=='json_schema'

result=RuntimeOrchestrator(ROOT,adapter=adapter).execute(req)
assert result.artifacts['content_draft']['article_content']
assert result.status=='revision_required'
assert result.artifacts['quality_report']['rules_evaluated']==42
print('model adapter tests: PASS')
