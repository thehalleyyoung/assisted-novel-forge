---
name: assisted-novel-forge
description: >
  Superadditive novel forge: composes all-band fiction skills + anti-AI-tells library
  through shared forge_state, pressure-driven minimal plans, voice-bound adversarial
  scrubbing, and a compound done-gate. Use for /assisted-novel-forge, assisted or
  autonomous novels that must not false-done or sound like a skill checklist.
  Do NOT use for Storybook UI stories, agile user stories, or scientific manuscripts.
---

# assisted-novel-forge

**Not a megaphone for 50 skills.** A composition engine that makes fiction + anti-AI-tells lanes *interfere constructively*.

## Emergence thesis

| If you only… | You get… |
|---|---|
| Chain every member | Noise, voice erasure, false-done |
| **Compose pressures** | Few moves that actually change the manuscript |

Couplings that create surplus value:

1. **Voice → humanizers** — `voice_contract.md` binds every scrub/deslop
2. **Tells → continuity** — tell families raise `ai_tells` pressure in `forge_state.json`
3. **Beats → chapters** — open beats prescribe chapter work before craft
4. **Detect ≠ scrub** — adversarial pairs from different skill families
5. **Compound done-gate** — `verify_gate` fails while compound_pressure is high

## Modes

| Mode | Behavior |
|---|---|
| **assisted** | AskUserQuestion at prescription boundaries; never overwrite canon without confirm |
| **autonomous** | Apply forge_brief members with checkpoints; still need verify PASS |

## Operating loop (the smart path)

```bash
python3 scripts/handoff_pack.py init --root "$PROJECT" --title "…" --mode assisted
python3 scripts/forge_state.py init --root "$PROJECT" --mode assisted
# … members write world/plot/chapters/voice_contract via forge_brief …
python3 scripts/compose.py --root "$PROJECT" --write          # diagnose + minimal plan
python3 scripts/forge_loop.py --root "$PROJECT" --dry         # emit review/forge_brief.md
# agent runs ONLY prescribed members, respecting voice_constraints + adversarial pairs
python3 scripts/ai_tells_ensemble.py --root "$PROJECT" --voice-aware
python3 scripts/verify_gate.py --root "$PROJECT" --json       # compound + tells + pack
```

Or slash:

```text
/assisted-novel-forge assisted: lighthouse door literary novel, 10 chapters
/forge-composer diagnose ./novel_project
/anti-ai-tells adversarial scrub on ./novel_project under voice_contract
```

## Done rule

Never claim done unless:

```bash
python3 scripts/verify_gate.py --root "$PROJECT" --json
# decision == PASS  (implies pack + prose + ai_tells + voice + compound_pressure)
```

Chat self-grade is not evidence. A long member list is not evidence.

## Router

`scripts/assist_mode_router.py` — ABSTAIN on wrong-sense; then **prefer forge-composer** over fixed phase lists.

## Libraries (cite, don't dump)

- **Fiction all-band** — see `skills/*-upgraded` and `UPSTREAM.md`
- **Anti-AI-tells (10)** — library for adversarial pairs; orchestrated by `/anti-ai-tells` + compose
- **Subskills** — `handoff-pack`, `continuity-bridge`, `verify-gate`, `assist-mode-router`, `anti-ai-tells`, `forge-composer`

## Integration smoke

```bash
bash scripts/smoke_all.sh
```
