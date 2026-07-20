#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
TELLS=["moreover","tapestry","delve","underscore","landscape of"]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--chapter", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args=ap.parse_args(); text=args.chapter.read_text(encoding="utf-8", errors="ignore").lower()
    hits=[t for t in TELLS if t in text]
    report={"ai_tell_hits":hits,"decision":"PASS" if len(hits)==0 else "REWRITE"}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2)+"\n"); print(json.dumps(report, indent=2))
    return 0 if report["decision"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
