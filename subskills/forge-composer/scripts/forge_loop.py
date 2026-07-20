#!/usr/bin/env python3
"""Closed forge loop — the emergent behavior vs linear pipelines.

Each iteration:
  diagnose (compose) → emit agent_brief.md for prescribed members →
  remeasure after agent applies → stop when compound_pressure < threshold
  or max iterations.

Scripts never invent prose; they force the *routing intelligence*.
"""
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path
import forge_state as fs
import compose


def write_brief(root: Path, st: dict) -> Path:
    presc = st.get("prescription") or {}
    lines = [
        "# Forge brief (compose — do not ignore)",
        "",
        f"Compound pressure: **{presc.get('compound_pressure', fs.compound_pressure(st)):.3f}**",
        f"Iteration: {st.get('loop', {}).get('iteration', 0)}",
        "",
        "## Voice constraints (bind every rewrite)",
        "",
    ]
    for c in st.get("voice", {}).get("constraints") or []:
        lines.append(f"- {c}")
    lines += ["", "## Prescribed members (ONLY these — do not run the whole marketplace)", ""]
    for m in presc.get("members") or []:
        lines.append(f"- `{m}`")
    lines += ["", "## Why (coupling rationale)", ""]
    for r in presc.get("rationale") or []:
        lines.append(f"- {r}")
    pairs = presc.get("detector_scrubber_pairs") or []
    if pairs:
        lines += ["", "## Adversarial detect→scrub pairs", ""]
        for p in pairs:
            lines.append(f"- detect `{p['detect']}` then scrub `{p['scrub']}` (never same family)")
            lines.append(f"  - voice: {p.get('voice_constraints')}")
    lines += [
        "",
        "## After edits",
        "",
        "```bash",
        "python3 scripts/compose.py --root . --write",
        "python3 scripts/ai_tells_ensemble.py --root . --voice-aware",
        "python3 scripts/verify_gate.py --root . --json",
        "```",
        "",
        "Refuse done until verify_gate PASS **and** compound_pressure < threshold.",
        "",
    ]
    p = root / "review" / "forge_brief.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n")
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--threshold", type=float, default=0.85)
    ap.add_argument("--max-iter", type=int, default=8)
    ap.add_argument("--budget", type=int, default=5)
    ap.add_argument("--dry", action="store_true", help="diagnose+brief only (no claim of prose edits)")
    args = ap.parse_args()
    root = args.root
    root.mkdir(parents=True, exist_ok=True)
    st = fs.load(root)
    st["loop"]["max_iterations"] = args.max_iter
    history = []

    for i in range(args.max_iter):
        st["loop"]["iteration"] = i + 1
        st = compose.diagnose(root, st)
        st = compose.prescribe(st, budget=args.budget)
        score = fs.compound_pressure(st)
        brief = write_brief(root, st)
        # refresh ai tells report as part of remeasure
        subprocess.run([sys.executable, str(Path(__file__).parent / "ai_tells_ensemble.py"), "--root", str(root), "--voice-aware"], capture_output=True, text=True)
        entry = {
            "iteration": i + 1,
            "compound_pressure": score,
            "pressures": dict(st.get("pressures") or {}),
            "members": list((st.get("prescription") or {}).get("members") or []),
            "brief": str(brief),
        }
        history.append(entry)
        st["loop"]["history"] = history
        fs.save(root, st)
        if score < args.threshold and not any(float(v) >= 0.99 for k, v in (st.get("pressures") or {}).items() if k in ("continuity_dirty", "review_blocking")):
            # also require verify-ish: no hard blockers
            if float((st.get("pressures") or {}).get("continuity_dirty") or 0) < 0.5 and float((st.get("pressures") or {}).get("ai_tells") or 0) < 0.5:
                print(json.dumps({"decision": "PASS", "reason": "compound_pressure under threshold", "loop": history}, indent=2))
                return 0
        if args.dry:
            # one iteration of diagnosis for the agent
            print(json.dumps({"decision": "CONTINUE", "note": "dry: apply forge_brief members then re-run", "loop": history, "prescription": st.get("prescription")}, indent=2))
            return 2

    print(json.dumps({"decision": "FAIL", "reason": "max iterations without relief", "loop": history}, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
