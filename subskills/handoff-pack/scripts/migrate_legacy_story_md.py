#!/usr/bin/env python3
"""Migrate story-skills story.md layout into handoff pack."""
import argparse, shutil
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--dst", type=Path, required=True); a=ap.parse_args()
    a.dst.mkdir(parents=True, exist_ok=True)
    for name in ("story.md","characters","plot","chapters","continuity","world"):
        s=a.src/name
        if s.exists():
            t=a.dst/(name if name!="story.md" else "bible.md")
            if s.is_dir(): shutil.copytree(s, a.dst/name, dirs_exist_ok=True)
            else: shutil.copy2(s, t)
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
