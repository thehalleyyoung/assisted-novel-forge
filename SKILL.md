---
name: assisted-novel-forge
description: >
  Write, continue, or finish a novel with competing fiction workflows plus an
  anti-AI-tells scrub that cannot self-grade done. Use when the user asks to write
  a novel, draft/continue chapters, scrub AI writing tells from fiction prose,
  humanize manuscript voice, or check whether a novel project is really done.
  Prefer /assisted-novel-forge, /forge-composer, or /anti-ai-tells. Do NOT use for
  Storybook UI stories, agile user stories, SEO blogs, or scientific manuscripts.
---

# assisted-novel-forge

Compose fiction + anti-AI-tells member skills through shared pressures. Do not run the full marketplace checklist — prescribe a minimal set, bind rewrites to voice, and refuse done until `verify_gate.py` PASS.

## When to Use

- User wants a full novel, chapter continuation, or manuscript finish from a premise
- User wants assisted (ask-as-you-go) or autonomous (checkpointed) novel drafting
- User wants AI-tell detection/humanize/deslop on fiction without flattening voice
- User asks whether a novel project is actually done (needs an independent gate)

## When NOT to Use

- Storybook / React component “stories”
- Agile user stories / acceptance criteria
- Scientific manuscripts or SEO blog keyword work
- One-shot marketing copy with no fiction project pack

## Operating loop

1. Route with `scripts/assist_mode_router.py` (ABSTAIN on wrong-sense).
2. Init pack + state:
   ```bash
   python3 scripts/handoff_pack.py init --root "$PROJECT" --title "…" --mode assisted
   python3 scripts/forge_state.py init --root "$PROJECT" --mode assisted
   ```
3. Seed only core lanes (principles → world → plot → architecture → planner → chapters) as needed.
4. Diagnose and prescribe a **minimal** plan (do not walk all members):
   ```bash
   python3 scripts/compose.py --root "$PROJECT" --write
   python3 scripts/forge_loop.py --root "$PROJECT" --dry
   ```
5. Apply **only** members listed in `review/forge_brief.md`. Honor `voice_constraints`. For AI tells, use the adversarial detect≠scrub pair — never detect with the scrubber.
6. Rescore tells, then gate:
   ```bash
   python3 scripts/ai_tells_ensemble.py --root "$PROJECT" --voice-aware
   python3 scripts/verify_gate.py --root "$PROJECT" --json
   ```

## Slash examples

```text
/assisted-novel-forge assisted: lighthouse door literary novel, 10 chapters
/assisted-novel-forge autonomous --chapters 8: floating market heist
/forge-composer diagnose ./novel_project
/anti-ai-tells adversarial scrub on ./novel_project under voice_contract
```

## Done rule

Never claim done unless:

```bash
python3 scripts/verify_gate.py --root "$PROJECT" --json
# decision == PASS
```

PASS requires pack validity, chapter length, voice_contract, ai_tells report, continuity, and `compound_pressure` under threshold. Chat self-grade and long member lists are not evidence.

## Couplings (why compose beats a list)

1. Voice → humanizers — `voice_contract.md` binds every scrub/deslop
2. Tells → pressures — tell families raise `ai_tells` in `forge_state.json`
3. Beats → chapters — open beats prescribe chapter work before craft
4. Detect ≠ scrub — adversarial pairs from different skill families
5. Compound done-gate — `verify_gate` fails while compound_pressure is high

Details: `references/emergence.md`, `references/pipeline.md`, `references/phase_contract.md`, `references/non_triggers.md`.

## Libraries

- Fiction all-band members — `skills/*-upgraded` (see `UPSTREAM.md`)
- Anti-AI-tells library (10) — orchestrated by `/anti-ai-tells` + compose, not “run all”
- Subskills — `handoff-pack`, `continuity-bridge`, `verify-gate`, `assist-mode-router`, `anti-ai-tells`, `forge-composer`

## Integration smoke

```bash
bash scripts/smoke_all.sh
```
