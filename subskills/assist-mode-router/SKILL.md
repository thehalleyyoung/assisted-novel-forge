---
name: assist-mode-router
description: Route autonomous vs assisted creative writing; abstain on Storybook/user-story/sci manuscript misfires.
---
# assist-mode-router

## When to Use

- First step of /assisted-novel-forge to choose assisted vs autonomous and ABSTAIN wrong-sense

## When NOT to Use

- Already inside a prescribed forge_brief mid-loop

`python3 scripts/assist_mode_router.py --text "..." [--mode assisted|autonomous]`
Returns ROUTE with planner+phases or ABSTAIN.

First call in superskill. ABSTAIN exits 2.

## Planner selection
webnovel/xianxia → novel-creator; literary/workshop → novel-writer; else mode-based.
