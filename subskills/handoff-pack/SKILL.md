---
name: handoff-pack
description: Materialize and validate fiction project handoff packs for assisted-novel-forge. Use when normalizing I/O between world/plot/chapter skills.
---
# handoff-pack
Run `python3 scripts/handoff_pack.py init|validate --root PROJECT`.
Required: brief.json, bible.md, world/, plot/, chapters/, characters/, continuity/ledger.json.

## Commands
`init` and `validate` — see package scripts (copied here for standalone install).

## Failure recovery
If validate FAIL, print reasons and do not continue superskill phases.
