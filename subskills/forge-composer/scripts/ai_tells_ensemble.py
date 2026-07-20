#!/usr/bin/env python3
"""Anti-AI-tells gate with voice coupling + adversarial family split.

More than a lexicon: couples to voice_contract, writes forge_state pressures,
and recommends detect≠scrub pairs so scrubbing isn't graded by the scrubber.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

TELLS = [
    r"\bmoreover\b", r"\bfurthermore\b", r"\btapestry\b", r"\bdelve\b",
    r"\bunderscore[sd]?\b", r"\blandscape of\b", r"\brobust\b", r"\bseamless\b",
    r"\bin the realm of\b", r"\ba testament to\b", r"\bit'?s important to note\b",
    r"\bin conclusion\b", r"\bvibrant\b", r"\bnestled\b", r"\bembark on a journey\b",
    r"\bplays a crucial role\b", r"\bunlock the potential\b",
    r"\bas an ai\b", r"\bi hope this helps\b",
]

# Family buckets for adversarial pairing
FAMILY = {
    "connective_slop": [r"\bmoreover\b", r"\bfurthermore\b", r"\bin conclusion\b", r"\bit'?s important to note\b"],
    "purple_metaphor": [r"\btapestry\b", r"\blandscape of\b", r"\bnestled\b", r"\bembark on a journey\b"],
    "corporate_abstract": [r"\brobust\b", r"\bseamless\b", r"\bdelve\b", r"\bunderscore[sd]?\b", r"\bunlock the potential\b", r"\bplays a crucial role\b", r"\ba testament to\b", r"\bin the realm of\b", r"\bvibrant\b"],
    "assistant_leak": [r"\bas an ai\b", r"\bi hope this helps\b"],
}

DETECT = [
    "ai-writing-detection-upgraded",
    "writing-anti-ai-upgraded",
    "prose-critique-upgraded",
]
SCRUB = [
    "slopbuster-upgraded",
    "oh-story-deslop-upgraded",
    "humanize-upgraded",
    "humanizer-upgraded",
    "humanize-writing-upgraded",
    "english-humanizer-upgraded",
    "writing-humanizer-upgraded",
    "better-writing-upgraded",
]


def score_text(text: str) -> list[dict]:
    low = text.lower()
    hits = []
    for pat in TELLS:
        for m in re.finditer(pat, low, flags=re.I):
            fam = "other"
            for fname, pats in FAMILY.items():
                if pat in pats:
                    fam = fname
                    break
            hits.append({"pattern": pat, "family": fam, "span": [m.start(), m.end()], "match": m.group(0)})
    return hits


def voice_constraints(root: Path) -> list[str]:
    p = root / "voice_contract.md"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line.lstrip("- ").strip())
    return out[:12]


def pick_pair(families: dict[str, int], lang: str) -> dict:
    # map dominant family → preferred scrubber (still ≠ detect)
    dominant = max(families.items(), key=lambda kv: kv[1])[0] if families else "connective_slop"
    scrub_map = {
        "connective_slop": "slopbuster-upgraded",
        "purple_metaphor": "oh-story-deslop-upgraded",
        "corporate_abstract": "writing-humanizer-upgraded",
        "assistant_leak": "humanize-upgraded",
        "other": "humanizer-upgraded",
    }
    scrub = scrub_map.get(dominant, "humanize-upgraded")
    if lang.startswith("zh"):
        scrub = "humanizer-cn-upgraded"
    detect = DETECT[sum(ord(c) for c in dominant) % len(DETECT)]
    return {"detect": detect, "scrub": scrub, "dominant_family": dominant}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--max-hits", type=int, default=3)
    ap.add_argument("--lang", default="en")
    ap.add_argument("--voice-aware", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    chapters = []
    if (args.root / "chapters").exists():
        chapters = [p for p in (args.root / "chapters").glob("*.md") if p.name != "_index.md"]

    per = []
    total = 0
    families: dict[str, int] = {}
    for ch in chapters:
        hits = score_text(ch.read_text(encoding="utf-8", errors="ignore"))
        total += len(hits)
        for h in hits:
            families[h["family"]] = families.get(h["family"], 0) + 1
        per.append({"chapter": ch.name, "n_hits": len(hits), "hits": hits[:20]})

    pair = pick_pair(families, args.lang)
    constraints = voice_constraints(args.root) if args.voice_aware or True else []
    decision = "PASS" if total <= args.max_hits else "FAIL"

    report = {
        "decision": decision,
        "total_hits": total,
        "max_hits": args.max_hits,
        "families": families,
        "chapters": per,
        "adversarial_pair": pair,
        "voice_constraints": constraints,
        "coupling": {
            "rule": "Scrubbers must preserve voice_constraints; detectors must not be the scrubber",
            "detect_family": DETECT,
            "scrub_family": SCRUB + (["humanizer-cn-upgraded"] if args.lang.startswith("zh") else []),
        },
        "ensemble_members": DETECT + SCRUB,
        "procedure": (
            f"On FAIL: run `{pair['detect']}` for inventory, then `{pair['scrub']}` "
            f"bound by voice_constraints, then re-score with a *different* detector. "
            f"Update forge_state via compose.py."
        ),
    }
    outdir = args.root / "review"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "ai_tells_report.json").write_text(json.dumps(report, indent=2) + "\n")

    # couple into forge_state if present/importable
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import forge_state as fs
        st = fs.load(args.root)
        st.setdefault("pressures", {})
        st["pressures"]["ai_tells"] = fs.clamp01(total / 8.0)
        st.setdefault("signals", {})
        st["signals"]["tell_families"] = families
        st["signals"]["detector_scrubber_pairs"] = [pair]
        if constraints:
            st.setdefault("voice", {})["constraints"] = constraints
        fs.save(args.root, st)
    except Exception:
        pass

    print(json.dumps(report, indent=2))
    return 0 if decision == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
