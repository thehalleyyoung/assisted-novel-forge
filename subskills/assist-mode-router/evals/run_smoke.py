#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
s=Path(__file__).resolve().parents[1]/"scripts/assist_mode_router.py"
ab=subprocess.run([sys.executable,str(s),"--text","add Storybook story for Button"],capture_output=True,text=True)
ok=subprocess.run([sys.executable,str(s),"--text","assisted novel about a lighthouse","--mode","assisted"],capture_output=True,text=True)
abj=json.loads(ab.stdout); okj=json.loads(ok.stdout)
assert abj["decision"]=="ABSTAIN" and ab.returncode==2
assert okj["decision"]=="ROUTE" and ok.returncode==0
print(json.dumps({"decision":"PASS"}))
