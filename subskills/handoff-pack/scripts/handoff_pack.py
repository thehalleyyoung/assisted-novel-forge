#!/usr/bin/env python3
"""Materialize / validate fiction project handoff pack."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED_DIRS = ["world", "plot", "chapters", "continuity", "characters"]
REQUIRED_FILES = ["brief.json", "bible.md", "continuity/ledger.json"]

BRIEF_SCHEMA = {
  "title": str, "mode": str, "genre": str, "target_chapters": int, "pov": str, "tense": str
}

def init_pack(root: Path, brief: dict) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for d in REQUIRED_DIRS:
        (root/d).mkdir(exist_ok=True)
    brief = {
        "title": brief.get("title") or "Untitled",
        "mode": brief.get("mode") or "assisted",
        "genre": brief.get("genre") or "literary",
        "target_chapters": int(brief.get("target_chapters") or 10),
        "pov": brief.get("pov") or "third-limited",
        "tense": brief.get("tense") or "past",
    }
    (root/"brief.json").write_text(json.dumps(brief, indent=2)+"\n")
    if not (root/"bible.md").exists():
        (root/"bible.md").write_text(f"# Story Bible — {brief['title']}\n\n## Premise\n\n(todo)\n")
    ledger = root/"continuity/ledger.json"
    if not ledger.exists():
        ledger.write_text(json.dumps({"dirty": False, "facts": [], "open_questions": [], "promises": []}, indent=2)+"\n")
    (root/"plot/_index.md").write_text("# Plot index\n\n") if not (root/"plot/_index.md").exists() else None
    (root/"chapters/_index.md").write_text("# Chapters\n\n") if not (root/"chapters/_index.md").exists() else None
    (root/"world/_index.md").write_text("# World\n\n") if not (root/"world/_index.md").exists() else None

def validate_pack(root: Path) -> dict:
    reasons = []
    if not root.exists():
        return {"decision": "FAIL", "reasons": [f"missing pack root {root}"]}
    for d in REQUIRED_DIRS:
        if not (root/d).is_dir():
            reasons.append(f"missing dir {d}/")
    for f in REQUIRED_FILES:
        if not (root/f).exists():
            reasons.append(f"missing file {f}")
    brief_path = root/"brief.json"
    if brief_path.exists():
        try:
            brief = json.loads(brief_path.read_text())
            for k, typ in BRIEF_SCHEMA.items():
                if k not in brief:
                    reasons.append(f"brief.json missing {k}")
                elif not isinstance(brief[k], typ):
                    reasons.append(f"brief.json {k} type")
            if brief.get("mode") not in ("assisted", "autonomous"):
                reasons.append("brief.mode must be assisted|autonomous")
        except json.JSONDecodeError as e:
            reasons.append(f"brief.json invalid: {e}")
    ledger_path = root/"continuity/ledger.json"
    if ledger_path.exists():
        try:
            led = json.loads(ledger_path.read_text())
            if led.get("dirty") is True:
                reasons.append("continuity ledger dirty=true — resolve via continuity-bridge")
        except json.JSONDecodeError:
            reasons.append("ledger.json invalid")
    return {"decision": "PASS" if not reasons else "FAIL", "reasons": reasons, "root": str(root)}

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--root", type=Path, required=True)
    i.add_argument("--brief", type=Path, default=None)
    i.add_argument("--title", default="Untitled")
    i.add_argument("--mode", default="assisted", choices=["assisted","autonomous"])
    v = sub.add_parser("validate")
    v.add_argument("--root", type=Path, required=True)
    v.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.cmd == "init":
        brief = json.loads(args.brief.read_text()) if args.brief else {"title": args.title, "mode": args.mode}
        init_pack(args.root, brief)
        print(json.dumps(validate_pack(args.root), indent=2))
        return 0 if validate_pack(args.root)["decision"]=="PASS" else 1
    out = validate_pack(args.root)
    print(json.dumps(out, indent=2) if args.json else out)
    return 0 if out["decision"]=="PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
