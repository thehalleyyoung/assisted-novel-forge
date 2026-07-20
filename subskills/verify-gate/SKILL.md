---
name: verify-gate
description: Independent false-done gate for novel projects. Scripts decide PASS/FAIL before claiming manuscript done.
---
# verify-gate

## When to Use

- Before claiming a novel project done; independent PASS/FAIL

## When NOT to Use

- Mid-draft brainstorming with no claim of completion

`python3 scripts/verify_gate.py --root PROJECT --min-chapter-words 800 --json`
Fails on missing pack, short chapters, dirty ledger, blocking review, uncovered claims.

Hard gate before done. Exit code 1 on FAIL.
