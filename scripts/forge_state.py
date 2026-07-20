#!/usr/bin/env python3
"""Manuscript State Graph — the shared brain all lanes read/write.

Emergence comes from *coupling*: voice constrains humanizers, tell hits dirty
continuity, beat gaps prescribe chapters, compound pressure picks the next move.
"""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
from typing import Any

VERSION = 1

DEFAULT = {
    "schema": "assisted-novel-forge/forge_state",
    "version": VERSION,
    "updated_at": None,
    "mode": "assisted",
    "lang": "en",
    "voice": {"contract_path": "voice_contract.md", "fingerprint": {}, "constraints": []},
    "pressures": {
        "continuity_dirty": 0.0,
        "beat_gaps": 0.0,
        "ai_tells": 0.0,
        "review_blocking": 0.0,
        "craft_rewrite": 0.0,
        "thin_prose": 0.0,
        "voice_drift": 0.0,
    },
    "signals": {
        "tell_hits": [],
        "tell_families": {},
        "open_beats": [],
        "contradictions": [],
        "revision_targets": [],
        "detector_scrubber_pairs": [],
    },
    "loop": {"iteration": 0, "history": [], "max_iterations": 8},
    "prescription": {"lanes": [], "members": [], "rationale": []},
}


def load(root: Path) -> dict:
    p = root / "forge_state.json"
    if not p.exists():
        st = json.loads(json.dumps(DEFAULT))
        st["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return st
    st = json.loads(p.read_text())
    # fill defaults
    for k, v in DEFAULT.items():
        if k not in st:
            st[k] = json.loads(json.dumps(v))
        elif isinstance(v, dict):
            for kk, vv in v.items():
                st[k].setdefault(kk, json.loads(json.dumps(vv)))
    return st


def save(root: Path, st: dict) -> Path:
    st["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    st["version"] = VERSION
    p = root / "forge_state.json"
    p.write_text(json.dumps(st, indent=2) + "\n")
    return p


def compound_pressure(st: dict) -> float:
    """Weighted sum in [0, ~7]. Emergence metric: not any single lane."""
    w = {
        "continuity_dirty": 1.5,
        "beat_gaps": 1.2,
        "ai_tells": 1.4,
        "review_blocking": 1.3,
        "craft_rewrite": 0.9,
        "thin_prose": 1.0,
        "voice_drift": 1.1,
    }
    p = st.get("pressures") or {}
    return sum(w[k] * float(p.get(k) or 0.0) for k in w)


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--root", type=Path, required=True)
    i.add_argument("--mode", default="assisted")
    i.add_argument("--lang", default="en")
    s = sub.add_parser("show")
    s.add_argument("--root", type=Path, required=True)
    s.add_argument("--json", action="store_true")
    c = sub.add_parser("compound")
    c.add_argument("--root", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "init":
        st = load(args.root)
        st["mode"] = args.mode
        st["lang"] = args.lang
        save(args.root, st)
        print(json.dumps({"decision": "PASS", "path": "forge_state.json"}, indent=2))
        return 0
    st = load(args.root)
    if args.cmd == "show":
        print(json.dumps(st, indent=2))
        return 0
    score = compound_pressure(st)
    print(json.dumps({"compound_pressure": score, "pressures": st.get("pressures")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
