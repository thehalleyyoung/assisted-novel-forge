#!/usr/bin/env python3
"""Bridge novel-creator into assisted-novel-forge handoff pack."""
import argparse, json, subprocess, sys
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--title", default="Untitled"); ap.add_argument("--mode", default="autonomous")
    a=ap.parse_args()
    # prefer package-level handoff if present
    hp=Path(__file__).resolve().parents[3]/"scripts"/"handoff_pack.py"
    if not hp.exists(): hp=Path(__file__).resolve().parents[2]/"scripts"/"handoff_pack.py"
    if hp.exists():
        subprocess.check_call([sys.executable,str(hp),"init","--root",str(a.root),"--title",a.title,"--mode",a.mode])
    else:
        a.root.mkdir(parents=True, exist_ok=True)
        (a.root/"brief.json").write_text(json.dumps({"title":a.title,"mode":a.mode,"genre":"fantasy","target_chapters":10,"pov":"third-limited","tense":"past"}, indent=2)+"\n")
    (a.root/"task_plan.md").write_text(f"# Writing Plan: {a.title}\n\n## Characters\n\n## Foreshadowing Matrix\n")
    print(json.dumps({"decision":"PASS","root":str(a.root)}))
if __name__=="__main__": main()
