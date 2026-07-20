---
name: continuity-bridge
description: >
  Merge continuity ledgers across writing stages for assisted-novel-forge.
  Block superskill advance when dirty=true or contradictions remain.
---

# continuity-bridge

## When to Use

- After world, plot, chapter, or review updates that touch canon facts
- When forge_state shows continuity_dirty pressure

## When NOT to Use

- Pure prose craft with no ledger/canon changes
- Non-fiction project tracking unrelated to the novel pack

## Commands

```bash
python3 scripts/continuity_bridge.py merge --a A.json --b B.json --out continuity/ledger.json
python3 scripts/continuity_bridge.py status --ledger continuity/ledger.json
python3 scripts/assert_clean.py --ledger continuity/ledger.json
```

Dirty ledger or unresolved contradictions block `/assisted-novel-forge` done.
