---
name: forge-composer
description: >
  Composition brain for assisted-novel-forge. Diagnoses manuscript pressures,
  prescribes a *minimal* adversarial member set (detect≠scrub, voice-bound),
  and runs closed forge loops. Use when the user wants the remix to be more than
  a skill checklist — /forge-composer or inside /assisted-novel-forge.
---

# forge-composer

## Why this exists

Fifty marketplace skills in a row is *less* than the sum of their parts (noise, false-done, voice erasure).
This subskill makes the system **superadditive** by:

1. **Shared state** — `forge_state.json` pressures every lane can raise/lower
2. **Minimal prescription** — only members that reduce the *dominant* pressures
3. **Adversarial tells** — detector family ≠ scrubber family
4. **Voice coupling** — humanizers bound by `voice_contract.md`
5. **Closed loop** — diagnose → brief → remeasure until compound pressure drops

## Commands

```bash
python3 scripts/compose.py --root PROJECT --write
python3 scripts/forge_loop.py --root PROJECT --dry
python3 scripts/forge_state.py compound --root PROJECT
```

## Use (after install)

```text
/forge-composer diagnose ./novel_project and prescribe the next five moves only
```
