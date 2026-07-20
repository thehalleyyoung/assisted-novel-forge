#!/usr/bin/env python3
"""Compose a *minimal* plan from forge_state — more than a phase checklist.

Rules of emergence:
1. Never run all members — only those that reduce the dominant pressures.
2. Detectors and scrubbers must be different families (adversarial).
3. Voice constraints ride along every humanize/deslop prescription.
4. Continuity dirt blocks prose generation until resolved.
5. Beat gaps prescribe chapter focus before craft/tell scrub.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import forge_state as fs

# Pressure → candidate lanes (ordered)
LANE_MAP = {
    "continuity_dirty": [
        ("continuity-bridge", "continuity-bridge"),
        ("story-memory-upgraded", "memory"),
        ("glossary-reference-upgraded", "canon"),
    ],
    "beat_gaps": [
        ("plot-structure-upgraded", "plot"),
        ("story-architecture-upgraded", "architecture"),
        ("novel-outlining-upgraded", "outline"),
        ("chapter-writing-upgraded", "chapter"),
    ],
    "thin_prose": [
        ("chapter-writing-upgraded", "chapter"),
        ("oh-story-long-write-upgraded", "long-write"),
        ("story-upgraded", "oh-story"),
    ],
    "review_blocking": [
        ("story-review-upgraded", "review"),
        ("oh-story-review-upgraded", "oh-review"),
        ("writing-issues-upgraded", "issues"),
    ],
    "craft_rewrite": [
        ("creative-writing-craft-upgraded", "craft"),
        ("better-writing-upgraded", "better-writing"),
        ("revision-upgraded", "revision"),
        ("prose-upgraded", "prose"),
    ],
    "ai_tells": [
        # detect family
        ("ai-writing-detection-upgraded", "detect"),
        ("writing-anti-ai-upgraded", "anti-ai-protocol"),
        ("prose-critique-upgraded", "prose-critique"),
        # scrub family (disjoint from detect)
        ("slopbuster-upgraded", "slopbuster"),
        ("oh-story-deslop-upgraded", "deslop"),
        ("humanize-upgraded", "humanize"),
        ("humanizer-upgraded", "humanizer"),
        ("humanize-writing-upgraded", "humanize-writing"),
        ("english-humanizer-upgraded", "english-humanizer"),
        ("writing-humanizer-upgraded", "writing-humanizer"),
        ("humanizer-cn-upgraded", "humanizer-cn"),
    ],
    "voice_drift": [
        ("writing-principles-upgraded", "principles"),
        ("character-sim-upgraded", "character-sim"),
        ("story-sense-upgraded", "story-sense"),
    ],
}

DETECT_FAMILY = {
    "ai-writing-detection-upgraded",
    "writing-anti-ai-upgraded",
    "prose-critique-upgraded",
}
SCRUB_FAMILY = {
    "slopbuster-upgraded",
    "oh-story-deslop-upgraded",
    "humanize-upgraded",
    "humanizer-upgraded",
    "humanize-writing-upgraded",
    "english-humanizer-upgraded",
    "writing-humanizer-upgraded",
    "humanizer-cn-upgraded",
    "better-writing-upgraded",
}


def read_voice_constraints(root: Path) -> list[str]:
    p = root / "voice_contract.md"
    if not p.exists():
        return ["prefer concrete sensory detail", "avoid generic AI cadence"]
    lines = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line.lstrip("- ").strip())
    return lines[:12] or ["prefer concrete sensory detail"]


def diagnose(root: Path, st: dict) -> dict:
    pressures = {k: 0.0 for k in fs.DEFAULT["pressures"]}
    signals = st.setdefault("signals", fs.DEFAULT["signals"])

    # continuity
    led = root / "continuity" / "ledger.json"
    if led.exists():
        try:
            L = json.loads(led.read_text())
            pressures["continuity_dirty"] = 1.0 if L.get("dirty") else 0.0
            signals["contradictions"] = L.get("contradictions") or []
        except json.JSONDecodeError:
            pressures["continuity_dirty"] = 1.0

    # beats
    beats_p = root / "plot" / "beats.json"
    if beats_p.exists():
        try:
            beats = json.loads(beats_p.read_text()).get("beats") or []
            open_b = [b["id"] for b in beats if not b.get("done")]
            signals["open_beats"] = open_b
            pressures["beat_gaps"] = fs.clamp01(len(open_b) / max(1, len(beats)))
        except json.JSONDecodeError:
            pressures["beat_gaps"] = 0.5
    elif not (root / "plot" / "_index.md").exists():
        pressures["beat_gaps"] = 0.8

    # thin prose
    chapters = []
    if (root / "chapters").exists():
        chapters = [p for p in (root / "chapters").glob("*.md") if p.name != "_index.md"]
    if not chapters:
        pressures["thin_prose"] = 1.0
    else:
        import re
        thin = 0
        for ch in chapters:
            wc = len(re.findall(r"\b\w+\b", ch.read_text(encoding="utf-8", errors="ignore")))
            if wc < 800:
                thin += 1
        pressures["thin_prose"] = fs.clamp01(thin / len(chapters))

    # review blocking
    blk = root / "review" / "blocking.json"
    if blk.exists():
        try:
            pressures["review_blocking"] = 1.0 if json.loads(blk.read_text()).get("blocking") else 0.0
        except json.JSONDecodeError:
            pressures["review_blocking"] = 0.5

    # craft rewrite
    craft = root / "review" / "craft_report.json"
    if craft.exists():
        try:
            pressures["craft_rewrite"] = 1.0 if json.loads(craft.read_text()).get("decision") == "REWRITE" else 0.0
        except json.JSONDecodeError:
            pass
    rt = root / "review" / "revision_targets.json"
    if rt.exists():
        try:
            targets = json.loads(rt.read_text()).get("targets") or []
            signals["revision_targets"] = targets
            if targets:
                pressures["craft_rewrite"] = max(pressures["craft_rewrite"], fs.clamp01(len(targets) / 5))
        except json.JSONDecodeError:
            pass

    # ai tells — run lexicon inline (no subprocess) for speed
    from ai_tells_ensemble import score_text, TELLS  # type: ignore
    total_hits = 0
    families: dict[str, int] = {}
    hit_list = []
    for ch in chapters:
        hits = score_text(ch.read_text(encoding="utf-8", errors="ignore"))
        total_hits += len(hits)
        for h in hits:
            fam = h["pattern"]
            families[fam] = families.get(fam, 0) + 1
            hit_list.append({**h, "chapter": ch.name})
    signals["tell_hits"] = hit_list[:50]
    signals["tell_families"] = families
    pressures["ai_tells"] = fs.clamp01(total_hits / 8.0)

    # voice drift — crude: if voice contract missing while chapters exist
    if chapters and not (root / "voice_contract.md").exists():
        pressures["voice_drift"] = 0.7
    else:
        pressures["voice_drift"] = 0.0

    st["pressures"] = pressures
    st["signals"] = signals
    st["voice"]["constraints"] = read_voice_constraints(root)
    return st


def prescribe(st: dict, budget: int = 5) -> dict:
    """Pick top pressures and a *small* adversarial member set."""
    pressures = st.get("pressures") or {}
    ranked = sorted(pressures.items(), key=lambda kv: -float(kv[1]))
    # hard priority: continuity before generation; beats before craft; tells after craft
    order_boost = {
        "continuity_dirty": 100,
        "beat_gaps": 80,
        "thin_prose": 70,
        "voice_drift": 60,
        "review_blocking": 50,
        "craft_rewrite": 40,
        "ai_tells": 30,
    }
    ranked = sorted(pressures.items(), key=lambda kv: -(float(kv[1]) * 10 + order_boost.get(kv[0], 0)))

    members: list[str] = []
    lanes: list[str] = []
    rationale: list[str] = []
    pairs: list[dict] = []
    lang = st.get("lang") or "en"

    for pressure, val in ranked:
        if float(val) < 0.15:
            continue
        if len(members) >= budget:
            break
        cands = LANE_MAP.get(pressure) or []
        if pressure == "ai_tells":
            # adversarial pair: one detector + one scrubber (not same family)
            detect = next((m for m, _ in cands if m in DETECT_FAMILY), None)
            scrub_opts = [m for m, _ in cands if m in SCRUB_FAMILY]
            if lang.startswith("zh") and "humanizer-cn-upgraded" in scrub_opts:
                scrub = "humanizer-cn-upgraded"
            else:
                scrub = scrub_opts[0] if scrub_opts else None
            # diversify scrub by tell family hash
            fams = st.get("signals", {}).get("tell_families") or {}
            if fams and len(scrub_opts) > 1:
                scrub = scrub_opts[sum(ord(c) for c in "".join(fams.keys())) % len(scrub_opts)]
            for m in (detect, scrub, "anti-ai-tells"):
                if m and m not in members and len(members) < budget:
                    members.append(m)
            if detect and scrub:
                pairs.append({"detect": detect, "scrub": scrub, "voice_constraints": st.get("voice", {}).get("constraints")})
                rationale.append(
                    f"ai_tells={val:.2f}: adversarial pair {detect} → {scrub} under voice constraints (not detect=scrub)"
                )
            lanes.append("anti-ai-tells")
            continue

        # generic: take first unused candidate for this pressure
        for mid, lane in cands:
            if mid in members:
                continue
            members.append(mid)
            lanes.append(lane)
            rationale.append(f"{pressure}={val:.2f} → {mid}")
            break

    # Always end with verify if any work prescribed
    if members and "verify-gate" not in members:
        # verify is a gate not a member skill — noted in plan
        pass

    st["prescription"] = {
        "lanes": lanes,
        "members": members,
        "rationale": rationale,
        "detector_scrubber_pairs": pairs,
        "compound_pressure": fs.compound_pressure(st),
        "budget": budget,
    }
    st["signals"]["detector_scrubber_pairs"] = pairs
    return st


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--budget", type=int, default=5)
    ap.add_argument("--write", action="store_true", help="persist forge_state.json")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    args.root.mkdir(parents=True, exist_ok=True)
    st = fs.load(args.root)
    st = diagnose(args.root, st)
    st = prescribe(st, budget=args.budget)
    if args.write:
        fs.save(args.root, st)
    out = {
        "decision": "PASS",
        "compound_pressure": fs.compound_pressure(st),
        "pressures": st["pressures"],
        "prescription": st["prescription"],
        "voice_constraints": st.get("voice", {}).get("constraints"),
        "emergence": {
            "thesis": "Minimal pressure-driven plan with adversarial detect≠scrub and voice-coupled humanization",
            "not": "Run all 50+ members in a fixed checklist",
        },
    }
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
