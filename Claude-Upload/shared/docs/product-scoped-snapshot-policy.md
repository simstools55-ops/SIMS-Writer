# Product-Scoped Snapshot Policy

## Purpose

SIMS Shared Editorial Knowledge is the complete Single Source of Truth and therefore contains both Writer and Article Creator mappings. Product runtime packages must not copy the complete mapping set into Claude Project Knowledge.

## Required snapshot contents

A product-scoped snapshot contains:

- `knowledge/`: all product-neutral shared knowledge
- `validation/`: shared validation rules
- `docs/`: shared operating documentation
- `mappings/<target-product>/`: only the target product mapping
- version and snapshot metadata

## Forbidden contents

- Writer snapshot: `mappings/article-creator/`
- Article Creator snapshot: `mappings/writer/`
- repository tests, caches, Git metadata, or accidental root-level copies

## Runtime boundary

Shared knowledge does not override product identity. Writer always performs existing-article improvement. Article Creator always performs new-article creation. A mapping for another product must never be loaded as Project Knowledge.

## Release check

Before release, verify that the Claude package contains exactly one product mapping and that the Project Instructions explicitly lock the product identity.
