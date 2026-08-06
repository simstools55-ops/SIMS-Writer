# Publication Integrity and Dynamic Information

## Purpose

公開可能な編集結果は、SEO上の妥当性だけでなく、事実の現在性、記事内の横断整合性、利用者が実際に公開する文章とJSONの一致を満たさなければならない。

## Dynamic information

次は変動情報として扱う。

- 価格、割引率、送料、定期条件、在庫、キャンペーン、返金保証
- アプリ・OS・Webサービスの機能、設定経路、UI、提供条件、上限
- プラン、API仕様、対応端末、提供地域、期間、頻度、普及状況

既存本文に記載されていても、PUBLIC_OKへ再掲・要約・FAQ化するときは現在有効な一次情報を再確認する。既存本文にあることは現在性の証明にならない。

## Official source priority

変動情報は、現在有効なOFFICIALまたはPRIMARYで確認できた場合だけPUBLIC_OK候補とする。確認できない場合は具体値・期間・頻度・不存在を断定しない。

## Cross-component consistency

ある主張を削除、弱化、更新した場合、次を横断確認する。

- SEOタイトル、記事タイトル、メタディスクリプション
- 導入文、本文、見出し、FAQ、まとめ
- CTA・ボタンラベル・リンク前後の誘導文
- publication_result、new_valuesを含む最終JSON

同一主張が別箇所に残る場合はPUBLIC_OK禁止。

## Publication synchronization

最終回答のBefore/AfterとContract JSONは、実際に公開する完成文を同一内容で保持する。局所修正後は完全JSONを再生成し、古いafterやchange_summaryを残さない。
