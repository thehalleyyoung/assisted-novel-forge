# Upgrade forge

Remix forge for assisted-novel-forge (50 rounds).

## Round 1 — buff-chapter-verify

**Gap:** Incumbent chapter skill has no independent word/continuity check

**Addition:** Added chapter_verify.py + SKILL done-rule + short-chapter eval fixture

**Commit:** `484d198`


## Round 2 — buff-chapter-handoff

**Gap:** Chapter skill did not write machine-readable handoff artifacts

**Addition:** Added export_handoff_chapter.py + handoff_contract.md + slash Use example

**Commit:** `95e4157`


## Round 3 — buff-chapter-smoke

**Gap:** No smoke eval proving false-done catch

**Addition:** Added evals/run_smoke.py + non-triggers + UPGRADE_PLAN

**Commit:** `bbac5f1`


## Round 4 — buff-review-blocking

**Gap:** Review skills rubber-stamp without machine-readable blocking state

**Addition:** Added review_blocking.py writing review/blocking.json for verify-gate

**Commit:** `85153b7`


## Round 5 — buff-review-claims

**Gap:** Critique findings evaporated between turns

**Addition:** Added review_to_claims.py continuity claims export + Use slash example

**Commit:** `bd3100b`


## Round 6 — buff-review-wire

**Gap:** No explicit wire into superskill verify path

**Addition:** Documented remix_wire + non-triggers + smoke stub

**Commit:** `3a3694d`


## Round 7 — buff-craft-report

**Gap:** Craft advice stayed chatty with no artifact

**Addition:** craft_pass_report.py emits rewrite/pass JSON; telltale fixture

**Commit:** `5000fcd`


## Round 8 — buff-craft-targets

**Gap:** No revision_targets.json for chapter rewrite loop

**Addition:** write_revision_targets.py + README slash example

**Commit:** `c6dadd0`


## Round 9 — buff-craft-nont

**Gap:** Over-trigger risk on non-fiction marketing

**Addition:** Non-triggers + pack_io reference

**Commit:** `8432bc3`

