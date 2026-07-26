# Knowledge Confidence Validation

- OFFICIAL/PRIMARYかつcurrentでない仕様変更はPUBLIC_OKへ自動昇格させない。
- MULTIPLE_THIRD_PARTYは検索意図の発見には使えるが、製品仕様断定の公開根拠としてはUSER_DECISION上限。
- verified_atのない変動仕様はfreshness=unknownとする。
- contradictedまたはstaleはINTERNAL_REJECT。
