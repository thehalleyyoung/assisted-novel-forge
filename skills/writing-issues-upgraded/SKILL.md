---
name: writing-issues-upgraded
type: mode-shift
description: >
  Review work after prose exists: editorial review, craft critique, continuity/voice review, copyediting, proofreading, and synthesis of reader-sim signal. Load when diagnosing a draft rather than rewriting it.
model-invocable: true
---

# Story Review

Analytical review of existing prose. This skill is for diagnosis, not
rewriting. Keep `/reader-sim` separate when the task needs a felt first-time
reader experience rather than analytical critique.

Choose the review level before reading. Start big before small unless the
caller explicitly asks for a late-stage pass. The edit levels move from
structural to surface, and each assumes the levels above it are stable:

- **Editorial review** — holistic third-party book-editor pass. What kind of
  revision does this draft need, and in what order?
- **Developmental edit** — structure, promise, causality, pacing, character
  arc. Is the draft the right shape?
- **Line edit** — voice, rhythm, clarity, texture. Does the prose move well?
- **Copyedit** — grammar, usage, punctuation, consistency. Is it correct?
- **Proofreading** — final surface pass. What slipped through?

Each level has a dedicated resource with method and checklist:

- `resources/editorial-review.md`
- `resources/developmental-edit.md`
- `resources/line-edit.md`
- `resources/copyedit.md`
- `resources/proofreading.md`

For adversarial craft critique (as opposed to editorial review), load:

- `resources/prose-critique.md` — methodology and focus-area routing.
- `resources/prose-critique/` — deep resources per focus area (structure,
  character, voice, prose, continuity).

When review incorporates reader-sim data:

- `resources/reader-sim-signal.md` — how to interpret and synthesize
  reader-sim output alongside analytical critique.


## Remix (assisted-novel-forge all-band)
Upstream `haowjy/creative-writing-skills@writing-issues` (installs≈264).
Writes/reads the shared handoff pack when orchestrated by `/assisted-novel-forge`.
**Done authority:** package `verify_gate.py` — do not self-grade done.
## Non-triggers
Not Storybook UI stories, agile user stories, or scientific manuscripts.
