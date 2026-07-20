---
name: anti-ai-tells
description: >
  Ensemble subskill that runs anti-AI-tell / humanize members (detect, scrub, deslop,
  humanize) on novel pack chapters before verify-gate. Use with /assisted-novel-forge
  or /anti-ai-tells on a project root.
---

# anti-ai-tells

## Members (merged)

1. `ai-writing-detection-upgraded` — detect
2. `writing-anti-ai-upgraded` — anti-AI writing protocol
3. `prose-critique-upgraded` — fiction antipatterns
4. `slopbuster-upgraded` — slop bust
5. `humanize-upgraded` — humanize
6. `humanizer-upgraded` — humanizer
7. `humanize-writing-upgraded` — humanize writing
8. `english-humanizer-upgraded` — English humanizer
9. `writing-humanizer-upgraded` — writing humanizer
10. `humanizer-cn-upgraded` — CN humanizer (when brief language=zh)

Also coordinates existing pack members: `better-writing-upgraded`, `oh-story-deslop-upgraded`, `revision-upgraded`.

## Procedure

```bash
python3 scripts/ai_tells_ensemble.py --root PROJECT [--lang en|zh] --json
```

Writes `review/ai_tells_report.json`. If `decision!=PASS`, superskill must rewrite and re-run — do not claim done.

## Use (after install)

```text
/anti-ai-tells scrub PROJECT chapters until tells below threshold
```
