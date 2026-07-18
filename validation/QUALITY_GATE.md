# Quality Gate v0.2.0

## Gate Decision

1. BLOCKERが1件でもあれば`FAIL`。
2. BLOCKERなし、MAJORが検証不能なら`UNVERIFIABLE`。
3. BLOCKER/MAJORなし、MINORまたはLOW_SAMPLE警告があれば`PASS_WITH_WARNING`。
4. すべて通過すれば`PASS`。

## 再処理

`FAIL`時は全文再生成ではなく、該当箇所だけを修正するTargeted Refinementを優先する。
最大2回で解消しない場合は手動確認へ送る。
