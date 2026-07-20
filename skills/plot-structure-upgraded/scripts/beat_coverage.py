#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); a=ap.parse_args()
    beats=json.loads((a.root/"plot/beats.json").read_text())["beats"]
    missing=[b["id"] for b in beats if not b.get("done")]
    print(json.dumps({"decision":"PASS" if not missing else "FAIL","missing":missing}, indent=2))
    return 0 if not missing else 1
if __name__=="__main__": raise SystemExit(main())
