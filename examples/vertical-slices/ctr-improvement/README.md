# CTR Improvement Vertical Slice

SBM形式のJSONを、CTR改善のDecision・Pattern・Draft・Quality・Publication Packageまで通す最小実装です。

```bash
python tools/run_ctr_vertical_slice.py examples/vertical-slices/ctr-improvement/sbm-request.json --repo-root . --output /tmp/ctr-result.json
```

外部APIやLLMは不要です。現段階の文章生成は保守的な決定論的実装で、Beta前にModel Adapterと比較検証します。
