#!/usr/bin/env python3
import argparse, json, subprocess, sys
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); a=ap.parse_args()
    vg=json.loads(subprocess.check_output([sys.executable,str(Path(__file__).parent/"verify_gate.py"),"--root",str(a.root),"--json"],text=True))
    card={"verify": vg["decision"], "n_chapters": vg.get("n_chapters"), "false_done_blocked": vg["decision"]!="PASS"}
    print(json.dumps({"decision": vg["decision"], "metric_card": card}, indent=2))
    return 0 if vg["decision"]=="PASS" else 1
if __name__=="__main__": raise SystemExit(main())
