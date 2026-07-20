#!/usr/bin/env python3
import argparse, json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True); a=ap.parse_args()
ok=(a.root/"architecture.md").exists(); print(json.dumps({"decision":"PASS" if ok else "FAIL"})); raise SystemExit(0 if ok else 1)
