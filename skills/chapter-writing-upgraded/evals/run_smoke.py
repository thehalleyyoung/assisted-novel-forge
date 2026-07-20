#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
short=root/"evals/fixtures/short.md"
r=subprocess.run([sys.executable,str(root/"scripts/chapter_verify.py"),"--root",str(root),"--chapter",str(short),"--min-words","800","--json"],capture_output=True,text=True)
out=json.loads(r.stdout); assert out["decision"]=="FAIL", out
print(json.dumps({"decision":"PASS","case":"short_fails"}))
