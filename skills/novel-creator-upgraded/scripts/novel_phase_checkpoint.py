#!/usr/bin/env python3
import argparse, json
from pathlib import Path
PHASES=["setup","rpg","plan","chapters","epub"]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--phase", required=True, choices=PHASES)
    a=ap.parse_args(); p=a.root/"checkpoints.json"
    data=json.loads(p.read_text()) if p.exists() else {"phases":{}}
    data["phases"][a.phase]="done"; p.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"decision":"PASS","phase":a.phase}))
if __name__=="__main__": main()
