#!/usr/bin/env python3
import argparse, json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument("--ledger", type=Path, required=True); a=ap.parse_args()
led=json.loads(a.ledger.read_text()); raise SystemExit(0 if not led.get("dirty") else 1)
