#!/usr/bin/env python3
"""Verify chapter artifacts against handoff pack expectations."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
def wc(t): return len(re.findall(r"\b\w+\b", t))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--chapter", type=Path, required=True); ap.add_argument("--min-words", type=int, default=800)
    ap.add_argument("--json", action="store_true"); args=ap.parse_args()
    reasons=[]
    if not args.chapter.exists(): reasons.append("missing chapter file")
    else:
        n=wc(args.chapter.read_text(encoding="utf-8", errors="ignore"))
        if n < args.min_words: reasons.append(f"words={n}<{args.min_words}")
    led=args.root/"continuity/ledger.json"
    if led.exists() and json.loads(led.read_text()).get("dirty"): reasons.append("ledger dirty")
    out={"decision":"PASS" if not reasons else "FAIL","reasons":reasons}
    print(json.dumps(out, indent=2)); return 0 if out["decision"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
