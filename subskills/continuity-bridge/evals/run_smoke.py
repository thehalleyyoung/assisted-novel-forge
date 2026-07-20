#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=Path(tempfile.mkdtemp())/"led.json"
r=subprocess.run([sys.executable,str(root/"scripts/continuity_bridge.py"),"merge","--a",str(root/"evals/fixtures/a.json"),"--b",str(root/"evals/fixtures/b.json"),"--out",str(out)],capture_output=True,text=True)
assert r.returncode==1, r.stdout
print(json.dumps({"decision":"PASS","case":"contradiction_fails"}))
