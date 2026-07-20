---
name: story-memory-upgraded
type: reference
description: >
  Creative-writing domain knowledge for durable story state. Load when
  preserving or retrieving project memory — fact extraction, context scoping,
  reference writing, artifact layout, and issue tracking. If you are @kb-lead,
  load this for the fiction-specific categories and conventions your general
  methodology doesn't cover.
model-invocable: true
---

# Story Memory

Knowledge that must survive the current pass: canon facts, context handoffs,
vocab/reference material, project layout, and persistent issues.

Load the resource needed:

- `resources/story-context.md` — what context to pass into handoffs for writers, critics, brainstormers, and knowledge agents.
- `resources/fact-extraction.md` — extract durable facts from chapters: character state, timeline, reveals, terminology.
- `resources/story-reference-writing.md` — wiki pages, vocab, decisions, summaries, issue logs.
- `resources/writing-artifacts.md` — where work and kb artifacts live.
- `resources/writing-issues.md` — persistent writing issue tracking across chapters.


## Remix (assisted-novel-forge all-band)
Upstream `haowjy/creative-writing-skills@story-memory` (installs≈200).
Writes/reads the shared handoff pack when orchestrated by `/assisted-novel-forge`.
**Done authority:** package `verify_gate.py` — do not self-grade done.
## Non-triggers
Not Storybook UI stories, agile user stories, or scientific manuscripts.
