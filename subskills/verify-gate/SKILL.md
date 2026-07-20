---
name: verify-gate
description: Independent false-done gate for novel projects. Scripts decide PASS/FAIL before claiming manuscript done.
---
# verify-gate
`python3 scripts/verify_gate.py --root PROJECT --min-chapter-words 800 --json`
Fails on missing pack, short chapters, dirty ledger, blocking review, uncovered claims.
