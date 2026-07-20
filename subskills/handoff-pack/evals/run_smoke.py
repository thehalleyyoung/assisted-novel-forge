#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
    r=subprocess.run([sys.executable,str(root/"scripts/handoff_pack.py"),"init","--root",td,"--title","T","--mode","assisted"],capture_output=True,text=True)
    assert r.returncode==0, r.stdout+r.stderr
print(json.dumps({"decision":"PASS"}))
