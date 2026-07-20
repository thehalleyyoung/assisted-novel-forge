#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--title", default="Architecture")
    args=ap.parse_args(); p=args.root/"architecture.md"
    p.write_text(f"# {args.title}\n\n## Acts\n\n## Chapter map\n\n## Scene beats\n")
    print('{"decision":"PASS","path":"architecture.md"}')
if __name__=="__main__": main()
