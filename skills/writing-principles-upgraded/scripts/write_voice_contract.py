#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--voice", default="concrete sensory; short clauses under stress")
    a=ap.parse_args(); p=a.root/"voice_contract.md"
    p.write_text(f"# Voice contract\n\n{a.voice}\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
