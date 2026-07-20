#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--claims", default='[{"id":"stakes_escalate","status":"open"}]')
    args=ap.parse_args(); p=args.root/"continuity/claims.json"; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"claims": json.loads(args.claims)}, indent=2)+"\n")
    print(json.dumps({"decision":"PASS","n":len(json.loads(args.claims))}))
if __name__=="__main__": main()
