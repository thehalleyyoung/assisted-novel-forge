#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--name", default="Primary locale")
    args=ap.parse_args(); w=args.root/"world"; w.mkdir(parents=True, exist_ok=True)
    (w/"_index.md").write_text("# World\n\n")
    (w/"locations.md").write_text(f"# Locations\n\n## {args.name}\n\n")
    facts=[{"key":"world.primary_locale","value":args.name}]
    led=args.root/"continuity/ledger.json"; led.parent.mkdir(parents=True, exist_ok=True)
    prev=json.loads(led.read_text()) if led.exists() else {"dirty":False,"facts":[],"open_questions":[],"promises":[]}
    prev["facts"]=list(prev.get("facts") or [])+facts
    led.write_text(json.dumps(prev, indent=2)+"\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
