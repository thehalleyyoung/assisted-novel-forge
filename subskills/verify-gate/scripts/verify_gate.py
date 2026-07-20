#!/usr/bin/env python3
"""Independent done-gate — compound pressures, not chat self-grade."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def check(root: Path, min_chapter_words: int = 800, min_chapters: int = 1, max_compound: float = 0.85) -> dict:
    reasons = []
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from handoff_pack import validate_pack
    import forge_state as fs

    pack = validate_pack(root)
    if pack["decision"] != "PASS":
        reasons.extend(["pack:" + r for r in pack["reasons"]])

    chapters = sorted((root / "chapters").glob("ch*.md")) if (root / "chapters").exists() else []
    if not chapters and (root / "chapters").exists():
        chapters = sorted([p for p in (root / "chapters").glob("*.md") if p.name != "_index.md"])
    if len(chapters) < min_chapters:
        reasons.append(f"need >={min_chapters} chapter files, found {len(chapters)}")
    for ch in chapters:
        wc = word_count(ch.read_text(encoding="utf-8", errors="ignore"))
        if wc < min_chapter_words:
            reasons.append(f"{ch.name} word_count={wc} < {min_chapter_words}")

    claims = root / "continuity" / "claims.json"
    if claims.exists():
        try:
            data = json.loads(claims.read_text())
            for c in data.get("claims") or []:
                if c.get("status") not in ("covered", "waived"):
                    reasons.append(f"uncovered claim: {c.get('id') or c}")
        except json.JSONDecodeError:
            reasons.append("claims.json invalid")

    ait = root / "review" / "ai_tells_report.json"
    if ait.exists():
        try:
            ar = json.loads(ait.read_text())
            if ar.get("decision") == "FAIL":
                reasons.append("ai_tells_report decision=FAIL — adversarial scrub under voice constraints")
            # require adversarial pair documented when tells were present
            if ar.get("total_hits", 0) > 0 and not ar.get("adversarial_pair"):
                reasons.append("ai_tells_report missing adversarial_pair (detect≠scrub)")
        except json.JSONDecodeError:
            reasons.append("ai_tells_report.json invalid")
    elif chapters:
        reasons.append("missing review/ai_tells_report.json — run ai_tells_ensemble before done")

    review = root / "review" / "blocking.json"
    if review.exists():
        try:
            if json.loads(review.read_text()).get("blocking"):
                reasons.append("review/blocking.json still has blocking=true")
        except json.JSONDecodeError:
            reasons.append("blocking.json invalid")

    # compound pressure from forge_state (emergence metric)
    st = fs.load(root)
    compound = fs.compound_pressure(st)
    pressures = st.get("pressures") or {}
    if compound > max_compound:
        reasons.append(f"compound_pressure={compound:.3f} > {max_compound} — run compose/forge_loop")
    if float(pressures.get("continuity_dirty") or 0) >= 0.99:
        reasons.append("continuity_dirty pressure — resolve via continuity-bridge before done")

    # voice coupling: if humanize happened, voice_contract should exist
    if chapters and not (root / "voice_contract.md").exists():
        reasons.append("missing voice_contract.md — principles must bind humanizers")

    return {
        "decision": "PASS" if not reasons else "FAIL",
        "reasons": reasons,
        "n_chapters": len(chapters),
        "min_chapter_words": min_chapter_words,
        "compound_pressure": compound,
        "pressures": pressures,
        "emergence": "done iff pack+prose+tells+continuity AND compound_pressure under threshold",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--min-chapter-words", type=int, default=800)
    ap.add_argument("--min-chapters", type=int, default=1)
    ap.add_argument("--max-compound", type=float, default=0.85)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = check(args.root, args.min_chapter_words, args.min_chapters, args.max_compound)
    print(json.dumps(out, indent=2) if args.json else out)
    return 0 if out["decision"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
