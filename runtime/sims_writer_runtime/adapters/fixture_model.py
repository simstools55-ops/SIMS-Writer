from __future__ import annotations
import json
from .model_protocol import ModelRequest, ModelResponse

class FixtureTransport:
    provider="fixture"
    def invoke(self, request: ModelRequest) -> ModelResponse:
        body={
          "seo_title":"Wi-Fiルーターの電気代はいくら？月額と節電方法を解説",
          "meta_description":"Wi-Fiルーターの電気代の目安、計算方法、つけっぱなし時の年間費用、無理なくできる節電方法を解説します。",
          "h1":"Wi-Fiルーターの電気代はいくら？年間費用と節電方法",
          "article_content":"Wi-Fiルーターの電気代は、消費電力と電気料金単価から計算できます。実際の金額は機種や契約単価で変わるため、銘板や仕様表を確認してください。",
          "faq":[],"internal_link_recommendations":[],"unresolved_items":[]
        }
        return ModelResponse(text=json.dumps(body,ensure_ascii=False),model=request.model,provider=self.provider,usage={"input_units":1,"output_units":1})
