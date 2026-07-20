#!/usr/bin/env python3
"""Orchestrate assisted-novel-forge phases (dry structural run)."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args):
    return subprocess.run(args, capture_output=True, text=True)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--text", required=True)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--mode", choices=["assisted","autonomous"], default=None)
    ap.add_argument("--dry-chapters", action="store_true", help="Do not require real prose; skip verify word counts")
    a=ap.parse_args()
    route=json.loads(run([sys.executable,str(ROOT/"scripts/assist_mode_router.py"),"--text",a.text]+(["--mode",a.mode] if a.mode else [])).stdout)
    if route["decision"]=="ABSTAIN":
        print(json.dumps(route, indent=2)); return 2
    a.root.mkdir(parents=True, exist_ok=True)
    run([sys.executable,str(ROOT/"scripts/handoff_pack.py"),"init","--root",str(a.root),"--title","Pipeline","--mode",route["mode"]])
    # mark structural exports
    for script, args in [
        ("skills/writing-principles-upgraded/scripts/write_voice_contract.py", ["--root",str(a.root)]),
        ("skills/worldbuilding-upgraded/scripts/export_world_canon.py", ["--root",str(a.root)]),
        ("skills/plot-structure-upgraded/scripts/export_plot_index.py", ["--root",str(a.root)]),
        ("skills/story-architecture-upgraded/scripts/export_architecture.py", ["--root",str(a.root)]),
    ]:
        p=ROOT/script
        if p.exists(): run([sys.executable,str(p),*args])
    card={"route":route,"pack":str(a.root)}
    if not a.dry_chapters:
        vg=json.loads(run([sys.executable,str(ROOT/"scripts/verify_gate.py"),"--root",str(a.root),"--json"]).stdout)
        card["verify"]=vg
        print(json.dumps(card, indent=2)); return 0 if vg.get("decision")=="PASS" else 1
    print(json.dumps({**card,"verify":"skipped_dry"}, indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
