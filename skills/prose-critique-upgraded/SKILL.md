---
name: prose-critique-upgraded
description: Prose critique / anti-pattern detection for fiction (from haowjy creative-writing-skills).
---
# prose-critique
Use resources/ for antipatterns, voice, structure. Emit findings to review/ai_tells_report.json in remix.


## Remix — anti-AI-tells lane (assisted-novel-forge)

Upstream `haowjy/creative-writing-skills@prose-critique` (installs≈387).

Part of the **anti-AI-tells ensemble** run after craft / before verify-gate:
1. Detect tells (`ai-writing-detection` / lexicon scorers)
2. Humanize / deslop / rewrite
3. Re-score; refuse done while score above threshold

Writes `review/ai_tells_report.json` when orchestrated. Done authority remains `verify_gate.py`.
