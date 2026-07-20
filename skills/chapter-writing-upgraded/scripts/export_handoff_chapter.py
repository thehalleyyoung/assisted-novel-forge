#!/usr/bin/env python3
"""Update chapters/_index.md and continuity stubs after a chapter draft."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--chapter", type=Path, required=True); ap.add_argument("--title", default="")
    args=ap.parse_args(); idx=args.root/"chapters/_index.md"; idx.parent.mkdir(parents=True, exist_ok=True)
    line=f"- `{args.chapter.name}` {args.title}\n"
    prev=idx.read_text() if idx.exists() else "# Chapters\n\n"
    if args.chapter.name not in prev: idx.write_text(prev.rstrip()+"\n"+line)
    led_p=args.root/"continuity/ledger.json"; led=json.loads(led_p.read_text()) if led_p.exists() else {"dirty":False,"facts":[],"open_questions":[],"promises":[]}
    led.setdefault("facts", []).append({"key":f"chapter:{args.chapter.stem}","value":"drafted"})
    led_p.parent.mkdir(parents=True, exist_ok=True); led_p.write_text(json.dumps(led, indent=2)+"\n")
    print(json.dumps({"decision":"PASS","indexed":args.chapter.name}))
if __name__=="__main__": main()
