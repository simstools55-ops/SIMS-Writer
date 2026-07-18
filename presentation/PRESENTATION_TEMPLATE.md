# Presentation Template v2.1

## 改善サマリー

- 改善必要度：
- 検索意図（Primary）：
- 診断：
- 変更箇所：
- 作業時間目安：
- Preservation Score：
- Change Budget：
- Rewrite Level / Scope：
- Risk：

## 改善概要

既存記事の良い部分を何として保護し、どこだけを変更するかを2〜4文で示す。

## 変更対象

変更した要素だけを、Before → After → 期待する効果 → 変更理由の順で出力する。

### 短文のBefore / After

```text
Beforeの内容
```

```text
Afterの内容
```

### 長文のBefore / After

導入文、本文、FAQ群など長い文章は、ページ全体を伸ばさず比較できるよう、次の縦スクロール枠を使う。最大高さは24remを標準とする。横方向へは原則スクロールさせず、改行を保持しながら折り返す。

**Before**

<div style="max-height:24rem; overflow-y:auto; overflow-x:hidden; border:1px solid #d0d7de; border-radius:6px; padding:12px;">
<pre style="white-space:pre-wrap; overflow-wrap:anywhere; margin:0;"><code>（変更前の全文）</code></pre>
</div>

**After**

<div style="max-height:24rem; overflow-y:auto; overflow-x:hidden; border:1px solid #d0d7de; border-radius:6px; padding:12px;">
<pre style="white-space:pre-wrap; overflow-wrap:anywhere; margin:0;"><code>（そのまま貼り付けられる変更後の全文）</code></pre>
</div>

表示環境がHTML styleを無効化する場合だけ、独立した `text` コードブロックへフォールバックする。文章の省略は禁止。

## 内部リンク

採用・保留・不採用を分類する。実際に追加・置換・削除した場合だけ `changes.internal_links` を true にする。

## 保護対象

広告、アフィリエイトリンク、体験談、独自レビュー、比較表、独自画像、CTA、結論など、変更しない要素を明示する。

## 注意事項

LOW_SAMPLE、再測定、事実未確認、手動確認事項がある場合のみ記載する。

## SIMSフィードバックJSON

回答の最後に `SIMS_FEEDBACK_V2.schema.json` に適合するJSONを1件だけ出力する。JSONより後には何も書かない。
