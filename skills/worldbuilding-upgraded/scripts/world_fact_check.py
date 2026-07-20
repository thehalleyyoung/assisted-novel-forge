#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--chapter", type=Path, required=True); a=ap.parse_args()
    led=json.loads((a.root/"continuity/ledger.json").read_text())
    text=a.chapter.read_text(encoding="utf-8", errors="ignore")
    missing=[]
    for f in led.get("facts") or []:
        if str(f.get("key","")).startswith("world.") and f.get("value") and str(f["value"]) not in text:
            missing.append(f)
    # advisory only
    print(json.dumps({"decision":"PASS","advisory_missing_mentions":missing}, indent=2))
if __name__=="__main__": main()
