#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
s=Path(__file__).resolve().parents[1]/"scripts/assist_mode_router.py"
ab=json.loads(subprocess.check_output([sys.executable,str(s),"--text","add Storybook story for Button"],text=True))
ok=json.loads(subprocess.check_output([sys.executable,str(s),"--text","assisted novel about a lighthouse","--mode","assisted"],text=True))
assert ab["decision"]=="ABSTAIN" and ok["decision"]=="ROUTE"
print(json.dumps({"decision":"PASS"}))
