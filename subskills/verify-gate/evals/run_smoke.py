#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
# subskills/verify-gate/evals -> package is parents[2]
pkg=Path(__file__).resolve().parents[2]
good=pkg/"evals/fixtures/good_pack"; bad=pkg/"evals/fixtures/bad_pack"
script=Path(__file__).resolve().parents[1]/"scripts/verify_gate.py"
g=json.loads(subprocess.check_output([sys.executable,str(script),"--root",str(good),"--json"],text=True))
b=json.loads(subprocess.check_output([sys.executable,str(script),"--root",str(bad),"--json"],text=True))
assert g["decision"]=="PASS" and b["decision"]=="FAIL"
print(json.dumps({"decision":"PASS"}))
