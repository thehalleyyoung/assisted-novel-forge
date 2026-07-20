#!/usr/bin/env python3
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--beats", default='["hook","first_turn","midpoint","climax","resolution"]')
    args=ap.parse_args(); beats=json.loads(args.beats)
    idx=args.root/"plot/_index.md"; idx.parent.mkdir(parents=True, exist_ok=True)
    body="# Plot index\n\n"+"\n".join(f"- [ ] {b}" for b in beats)+"\n"
    idx.write_text(body)
    (args.root/"plot/beats.json").write_text(json.dumps({"beats":[{ "id":b,"done":False} for b in beats]}, indent=2)+"\n")
    print('{"decision":"PASS"}')
if __name__=="__main__": main()
