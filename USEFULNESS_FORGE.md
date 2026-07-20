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


## Round 10 — buff-arch-export

**Gap:** Architecture lived only in chat/resources, not pack file

**Addition:** export_architecture.py materializes architecture.md

**Commit:** `44fae70`


## Round 11 — buff-arch-ux

**Gap:** Name collision with software architecture

**Addition:** Non-triggers for software-arch + slash Use example

**Commit:** `cd7bc55`


## Round 12 — buff-arch-validate

**Gap:** No check that architecture.md exists before chapters

**Addition:** validate_arch_present.py gate for superskill phase order

**Commit:** `8315dea`


## Round 13 — buff-nw-outline

**Gap:** EN novel-writer outline not wired to pack

**Addition:** export_outline_to_pack.py

**Commit:** `a1a80d8`


## Round 14 — buff-nw-role

**Gap:** Overlapped novel-creator without role split

**Addition:** Documented assisted default + vs_novel_creator reference

**Commit:** `81ff177`


## Round 15 — buff-nw-check

**Gap:** No outline existence check

**Addition:** check_outline_exists.py + smoke

**Commit:** `ada9232`


## Round 16 — buff-plot-export

**Gap:** Plot models stayed in references only

**Addition:** export_plot_index.py materializes beats.json

**Commit:** `8d88a94`


## Round 17 — buff-plot-coverage

**Gap:** No beat coverage metric

**Addition:** beat_coverage.py FAIL until beats marked done

**Commit:** `4574993`


## Round 18 — buff-plot-nont

**Gap:** Story-points agile collision

**Addition:** Non-triggers + pack_wire

**Commit:** `10ab739`


## Round 19 — buff-world-export

**Gap:** World notes not in pack/ledger

**Addition:** export_world_canon.py

**Commit:** `7738486`


## Round 20 — buff-world-check

**Gap:** Canon facts unused by chapters

**Addition:** world_fact_check.py advisory + Use example

**Commit:** `cbca66e`


## Round 21 — buff-world-nont

**Gap:** Infra 'world' name trap

**Addition:** Non-triggers docs

**Commit:** `dc78b01`


## Round 22 — buff-wp-voice

**Gap:** Principles not persisted for later phases

**Addition:** write_voice_contract.py

**Commit:** `b094984`


## Round 23 — buff-wp-nont

**Gap:** Generic 'principles' over-trigger

**Addition:** Non-triggers + slash Use

**Commit:** `01f8585`


## Round 24 — buff-wp-wire

**Gap:** Unclear phase position

**Addition:** pack_wire + smoke

**Commit:** `2d63f24`


## Round 25 — buff-nc-pack

**Gap:** novel-creator produced EPUB path without shared pack/verify

**Addition:** init_novel_pack.py + hard done-rule in SKILL

**Commit:** `98d2567`


## Round 26 — buff-nc-checkpoint

**Gap:** No resume checkpoints across long autonomous runs

**Addition:** novel_phase_checkpoint.py + Use example

**Commit:** `b6353a4`


## Round 27 — buff-nc-role

**Gap:** Overlap confusion with novel-writer

**Addition:** vs_novel_writer + non-triggers + smoke

**Commit:** `4525b9f`

