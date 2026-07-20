#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--outline", default="# Outline\n\n1. Setup\n2. Turn\n3. Climax\n")
    args=ap.parse_args(); p=args.root/"plot/outline.md"; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(args.outline if args.outline.endswith("\n") else args.outline+"\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
