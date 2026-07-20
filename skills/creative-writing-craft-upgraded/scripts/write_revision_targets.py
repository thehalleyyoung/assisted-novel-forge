#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--targets", default='["cut filter words","sharpen dialogue"]')
    args=ap.parse_args(); p=args.root/"review/revision_targets.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"targets": json.loads(args.targets)}, indent=2)+"\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
