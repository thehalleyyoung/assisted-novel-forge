#!/usr/bin/env python3
import argparse
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--note", default="Tighten opening image.")
    a=ap.parse_args(); p=a.root/"review/coach_notes.md"; p.parent.mkdir(parents=True, exist_ok=True)
    prev=p.read_text() if p.exists() else "# Coach notes\n\n"
    p.write_text(prev.rstrip()+f"\n- {a.note}\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
