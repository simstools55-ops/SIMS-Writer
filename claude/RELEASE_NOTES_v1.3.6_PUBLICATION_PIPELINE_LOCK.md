# SIMS Writer Claude v1.3.6 — Publication Pipeline Lock

- Removed the conflicting Contract 2.0 instruction.
- Made `publication_qa` and review trace mandatory.
- Prohibited standalone prose/`qa_verdict` PASS substitutions.
- Locked the order Draft → Review → Safe Fix → Re-review → Final Output.
- Added pre-release checks based on four failed operational tests.
