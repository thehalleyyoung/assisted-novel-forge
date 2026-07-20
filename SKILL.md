---
name: assisted-novel-forge
description: >
  End-to-end autonomous or assisted creative writing / novel forge. Remixes buffed
  marketplace skills (worldbuilding, plot, architecture, novel plan, chapters, craft,
  review) behind a shared handoff-pack and verify-gate so agents cannot false-done a
  manuscript. Use for /assisted-novel-forge, "write a novel assisted", "autonomous
  novel draft", competing fiction workflows. Do NOT use for Storybook UI stories,
  agile user stories, or scientific manuscripts.
---

# assisted-novel-forge

## Modes

| Mode | Behavior |
|---|---|
| **assisted** | AskUserQuestion at phase boundaries; never overwrite user canon without confirm |
| **autonomous** | Generate full pipeline with checkpoints on disk; still must `verify_gate.py` PASS |

Route with `scripts/assist_mode_router.py` first — ABSTAIN on Storybook / user-stories / sci manuscripts.

## Phases (wire buffed members)

1. `assist-mode-router` — mode + planner + non-triggers
2. `handoff-pack` init — `brief.json`, `bible.md`, dirs
3. `writing-principles-upgraded` — voice contract → `voice_contract.md`
4. `worldbuilding-upgraded` — `world/`
5. `plot-structure-upgraded` — `plot/`
6. `story-architecture-upgraded` — architecture into pack
7. `novel-creator-upgraded` **or** `novel-writer-upgraded` — novel plan (router chooses)
8. `chapter-writing-upgraded` — outline-then-prose; update continuity
9. `creative-writing-craft-upgraded` — craft pass
10. `story-review-upgraded` — critique → `review/`; optional `creative-writing-upgraded` coach
11. `continuity-bridge` merge — refuse advance if dirty
12. `anti-ai-tells` ensemble — detect/humanize/deslop until `review/ai_tells_report.json` PASS
13. `verify-gate` — **required** before claiming done (also fails on ai_tells FAIL)

## Done rule

Never claim done unless:

```bash
python3 scripts/verify_gate.py --root "$PROJECT" --json
# decision == PASS
```

Chat self-grade is not evidence.

## Slash examples

```text
/assisted-novel-forge assisted: lighthouse door literary novel, 10 chapters
/assisted-novel-forge autonomous --chapters 8: floating market heist
```

## Pipeline runner
`python3 scripts/run_pipeline.py --text "..." --root PROJECT [--mode assisted|autonomous]`

## Integration smoke
Before publish/claim ship: `bash scripts/smoke_all.sh`.

## Buffed members (all-band)

- `ai-writing-detection-upgraded`
- `better-writing-upgraded`
- `chapter-writing-upgraded`
- `character-sim-upgraded`
- `creative-writing-craft-upgraded`
- `creative-writing-muse-upgraded`
- `creative-writing-upgraded`
- `english-humanizer-upgraded`
- `fiction-upgraded`
- `glossary-reference-upgraded`
- `humanize-upgraded`
- `humanize-writing-upgraded`
- `humanizer-cn-upgraded`
- `humanizer-upgraded`
- `inkos-multi-agent-novel-writing-upgraded`
- `jmsktm-story-upgraded`
- `novel-creator-upgraded`
- `novel-outlining-upgraded`
- `novel-writer-upgraded`
- `oblique-worldbuilding-upgraded`
- `oceanswave-creative-writing-upgraded`
- `oh-story-cover-upgraded`
- `oh-story-deslop-upgraded`
- `oh-story-import-upgraded`
- `oh-story-long-analyze-upgraded`
- `oh-story-long-scan-upgraded`
- `oh-story-long-write-upgraded`
- `oh-story-review-upgraded`
- `oh-story-setup-upgraded`
- `oh-story-short-analyze-upgraded`
- `oh-story-short-scan-upgraded`
- `oh-story-short-write-upgraded`
- `plot-structure-upgraded`
- `prose-critique-upgraded`
- `prose-upgraded`
- `revision-upgraded`
- `slopbuster-upgraded`
- `story-architecture-upgraded`
- `story-context-upgraded`
- `story-init-upgraded`
- `story-memory-upgraded`
- `story-review-upgraded`
- `story-sense-upgraded`
- `story-upgraded`
- `webnovel-writing-upgraded`
- `worldbuilding-upgraded`
- `writing-anti-ai-upgraded`
- `writing-humanizer-upgraded`
- `writing-issues-upgraded`
- `writing-principles-upgraded`
- `writing-staffing-upgraded`

## Anti-AI-tells merge (10)

- `humanizerai/agent-skills@humanize`
- `z0gsh1u/oh-my-writing-skill@humanizer-cn`
- `galaxy-dawn/claude-scholar@writing-anti-ai`
- `haowjy/creative-writing-skills@prose-critique`
- `mike-coulbourn/claude-vibes@ai-writing-detection`
- `cowork-os/cowork-os@humanizer`
- `gabelul/slopbuster@slopbuster`
- `kambleakash0/agent-skills@english-humanizer`
- `hairyf/skills@writing-humanizer`
- `lguz/humanize-writing-skill@humanize-writing`

Subskill: `/anti-ai-tells` → `scripts/ai_tells_ensemble.py`.
