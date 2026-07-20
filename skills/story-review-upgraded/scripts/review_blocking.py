#!/usr/bin/env python3
"""Emit review/blocking.json — blocking=true until issues resolved."""
from __future__ import annotations
import argparse, json
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--issues", default="[]"); ap.add_argument("--blocking", action="store_true")
    args=ap.parse_args(); outdir=args.root/"review"; outdir.mkdir(parents=True, exist_ok=True)
    issues=json.loads(args.issues)
    payload={"blocking": bool(args.blocking or issues), "issues": issues}
    (outdir/"blocking.json").write_text(json.dumps(payload, indent=2)+"\n")
    print(json.dumps({"decision":"FAIL" if payload["blocking"] else "PASS", **payload}, indent=2))
    return 1 if payload["blocking"] else 0
if __name__=="__main__": raise SystemExit(main())
