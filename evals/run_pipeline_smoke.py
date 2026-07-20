#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
r=subprocess.run([sys.executable,str(root/"scripts/run_pipeline.py"),"--text","Storybook button story","--root",tempfile.mkdtemp()],capture_output=True,text=True)
assert r.returncode==2
d=tempfile.mkdtemp()
r=subprocess.run([sys.executable,str(root/"scripts/run_pipeline.py"),"--text","assisted lighthouse novel","--root",d,"--mode","assisted","--dry-chapters"],capture_output=True,text=True)
assert r.returncode==0, r.stdout+r.stderr
print(json.dumps({"decision":"PASS"}))
