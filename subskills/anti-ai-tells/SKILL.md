---
name: anti-ai-tells
description: >
  Voice-bound, adversarial anti-AI-tells lane for assisted-novel-forge. Detect and
  scrub with different skill families; never humanize away voice_contract. Prefer
  /forge-composer to decide *whether* and *which* members to run.
---

# anti-ai-tells

## When to Use

- Fiction prose needs detect≠scrub AI-tell cleanup under voice_contract

## When NOT to Use

- Non-fiction marketing copy or code-comment slop outside the novel pack


## Superadditive protocol (not "run all 10")

1. `ai_tells_ensemble.py --voice-aware` → families + adversarial_pair
2. Run **only** `adversarial_pair.detect` then `adversarial_pair.scrub`
3. Re-score with a *different* detector than the scrubber
4. `compose.py --write` so pressures update the whole forge

The 10 upgraded members are a *library*; the ensemble + forge-composer pick a pair.

## Members library

detect: ai-writing-detection, writing-anti-ai, prose-critique  
scrub: slopbuster, oh-story-deslop, humanize*, writing-humanizer, better-writing  
zh: humanizer-cn

## Use

```text
/anti-ai-tells adversarial scrub on PROJECT under voice_contract
```
