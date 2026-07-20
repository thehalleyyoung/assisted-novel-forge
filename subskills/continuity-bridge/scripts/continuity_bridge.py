#!/usr/bin/env python3
"""Merge/diff continuity ledgers; mark dirty on contradictions."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def load(p: Path) -> dict:
    if not p.exists():
        return {"dirty": False, "facts": [], "open_questions": [], "promises": []}
    return json.loads(p.read_text())

def merge(a: dict, b: dict) -> dict:
    facts = {}
    dirty = bool(a.get("dirty") or b.get("dirty"))
    contradictions = []
    for src in (a.get("facts") or []) + (b.get("facts") or []):
        key = src.get("key") or src.get("id")
        if not key:
            continue
        if key in facts and facts[key].get("value") != src.get("value"):
            dirty = True
            contradictions.append({"key": key, "a": facts[key], "b": src})
        else:
            facts[key] = src
    questions = {q.get("id") or q.get("text"): q for q in (a.get("open_questions") or []) + (b.get("open_questions") or [])}
    promises = {p.get("id") or p.get("text"): p for p in (a.get("promises") or []) + (b.get("promises") or [])}
    return {
        "dirty": dirty,
        "facts": list(facts.values()),
        "open_questions": list(questions.values()),
        "promises": list(promises.values()),
        "contradictions": contradictions,
    }

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge")
    m.add_argument("--a", type=Path, required=True)
    m.add_argument("--b", type=Path, required=True)
    m.add_argument("--out", type=Path, required=True)
    m.add_argument("--json", action="store_true")
    s = sub.add_parser("status")
    s.add_argument("--ledger", type=Path, required=True)
    s.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.cmd == "merge":
        out = merge(load(args.a), load(args.b))
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out, indent=2)+"\n")
        print(json.dumps({"decision": "FAIL" if out["dirty"] else "PASS", "n_contradictions": len(out.get("contradictions") or [])}, indent=2))
        return 1 if out["dirty"] else 0
    led = load(args.ledger)
    print(json.dumps({"decision": "FAIL" if led.get("dirty") else "PASS", "dirty": led.get("dirty"), "n_facts": len(led.get("facts") or [])}, indent=2))
    return 1 if led.get("dirty") else 0

if __name__ == "__main__":
    raise SystemExit(main())
