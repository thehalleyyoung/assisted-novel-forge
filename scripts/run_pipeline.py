#!/usr/bin/env python3
"""Structural pipeline: seed pack → compose → brief (superadditive path)."""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--mode", choices=["assisted", "autonomous"], default=None)
    ap.add_argument("--dry-chapters", action="store_true")
    a = ap.parse_args()
    route = json.loads(
        run(
            [sys.executable, str(ROOT / "scripts/assist_mode_router.py"), "--text", a.text]
            + (["--mode", a.mode] if a.mode else [])
        ).stdout
    )
    if route["decision"] == "ABSTAIN":
        print(json.dumps(route, indent=2))
        return 2
    a.root.mkdir(parents=True, exist_ok=True)
    run([sys.executable, str(ROOT / "scripts/handoff_pack.py"), "init", "--root", str(a.root), "--title", "Pipeline", "--mode", route["mode"]])
    run([sys.executable, str(ROOT / "scripts/forge_state.py"), "init", "--root", str(a.root), "--mode", route["mode"]])
    # seed exporters if present
    for script in [
        "skills/writing-principles-upgraded/scripts/write_voice_contract.py",
        "skills/worldbuilding-upgraded/scripts/export_world_canon.py",
        "skills/plot-structure-upgraded/scripts/export_plot_index.py",
        "skills/story-architecture-upgraded/scripts/export_architecture.py",
    ]:
        p = ROOT / script
        if p.exists():
            run([sys.executable, str(p), "--root", str(a.root)])
    comp = json.loads(run([sys.executable, str(ROOT / "scripts/compose.py"), "--root", str(a.root), "--write"]).stdout)
    run([sys.executable, str(ROOT / "scripts/forge_loop.py"), "--root", str(a.root), "--dry"])
    card = {"route": route, "compose": comp, "pack": str(a.root), "brief": str(a.root / "review/forge_brief.md")}
    if not a.dry_chapters:
        # still may FAIL verify until chapters exist — that's correct
        vg = json.loads(run([sys.executable, str(ROOT / "scripts/verify_gate.py"), "--root", str(a.root), "--json"]).stdout)
        card["verify"] = vg
        print(json.dumps(card, indent=2))
        return 0 if vg.get("decision") == "PASS" else 1
    print(json.dumps({**card, "verify": "skipped_dry"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
