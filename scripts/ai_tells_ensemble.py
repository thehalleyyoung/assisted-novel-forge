#!/usr/bin/env python3
"""Deterministic anti-AI-tells gate for assisted-novel-forge packs."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

# Common surface AI tells (lexicon) — cheap black-box proxy before member rewrites
TELLS = [
    r"\bmoreover\b", r"\bfurthermore\b", r"\btapestry\b", r"\bdelve\b",
    r"\bunderscore[sd]?\b", r"\blandscape of\b", r"\brobust\b", r"\bseamless\b",
    r"\bin the realm of\b", r"\ba testament to\b", r"\bit'?s important to note\b",
    r"\bin conclusion\b", r"\bvibrant\b", r"\bnestled\b", r"\bembark on a journey\b",
    r"\bshallow of\b", r"\bplays a crucial role\b", r"\bunlock the potential\b",
    r"\bas an ai\b", r"\bi hope this helps\b",
]

MEMBERS = [
    "ai-writing-detection-upgraded",
    "writing-anti-ai-upgraded",
    "prose-critique-upgraded",
    "slopbuster-upgraded",
    "humanize-upgraded",
    "humanizer-upgraded",
    "humanize-writing-upgraded",
    "english-humanizer-upgraded",
    "writing-humanizer-upgraded",
    "humanizer-cn-upgraded",
]

def score_text(text: str) -> list[dict]:
    low = text.lower()
    hits=[]
    for pat in TELLS:
        for m in re.finditer(pat, low, flags=re.I):
            hits.append({"pattern": pat, "span": [m.start(), m.end()], "match": m.group(0)})
    return hits

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--max-hits", type=int, default=3, help="FAIL if total lexicon hits > this")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--json", action="store_true")
    args=ap.parse_args()
    chapters=sorted((args.root/"chapters").glob("*.md")) if (args.root/"chapters").exists() else []
    chapters=[p for p in chapters if p.name!="_index.md"]
    per=[]
    total=0
    for ch in chapters:
        text=ch.read_text(encoding="utf-8", errors="ignore")
        hits=score_text(text)
        total+=len(hits)
        per.append({"chapter": ch.name, "n_hits": len(hits), "hits": hits[:20]})
    members=list(MEMBERS)
    if args.lang.startswith("zh"):
        # prefer CN humanizer first
        members=["humanizer-cn-upgraded"]+[m for m in members if m!="humanizer-cn-upgraded"]
    decision="PASS" if total<=args.max_hits else "FAIL"
    report={
        "decision": decision,
        "total_hits": total,
        "max_hits": args.max_hits,
        "chapters": per,
        "ensemble_members": members,
        "procedure": "On FAIL: run detect → writing-anti-ai / prose-critique → humanize/slopbuster/deslop → re-score until PASS",
        "also_use": ["better-writing-upgraded", "oh-story-deslop-upgraded", "revision-upgraded"],
    }
    outdir=args.root/"review"; outdir.mkdir(parents=True, exist_ok=True)
    (outdir/"ai_tells_report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
    return 0 if decision=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
