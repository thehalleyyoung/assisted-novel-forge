#!/usr/bin/env python3
"""Independent done-gate for assisted-novel-forge (no chat self-grade)."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))

def check(root: Path, min_chapter_words: int = 800, min_chapters: int = 1) -> dict:
    reasons = []
    # pack validate inline
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from handoff_pack import validate_pack
    pack = validate_pack(root)
    if pack["decision"] != "PASS":
        reasons.extend(["pack:"+r for r in pack["reasons"]])

    chapters = sorted((root/"chapters").glob("ch*.md")) if (root/"chapters").exists() else []
    # also accept chapter-01.md style
    if not chapters:
        chapters = sorted([p for p in (root/"chapters").glob("*.md") if p.name != "_index.md"]) if (root/"chapters").exists() else []
    if len(chapters) < min_chapters:
        reasons.append(f"need >={min_chapters} chapter files, found {len(chapters)}")
    for ch in chapters:
        wc = word_count(ch.read_text(encoding="utf-8", errors="ignore"))
        if wc < min_chapter_words:
            reasons.append(f"{ch.name} word_count={wc} < {min_chapter_words}")

    # claims file optional but if present must be covered
    claims = root/"continuity/claims.json"
    if claims.exists():
        try:
            data = json.loads(claims.read_text())
            for c in data.get("claims") or []:
                if c.get("status") not in ("covered", "waived"):
                    reasons.append(f"uncovered claim: {c.get('id') or c}")
        except json.JSONDecodeError:
            reasons.append("claims.json invalid")

    # refuse if anti-AI-tells ensemble reported FAIL
    ait = root/"review/ai_tells_report.json"
    if ait.exists():
        try:
            ar = json.loads(ait.read_text())
            if ar.get("decision") == "FAIL":
                reasons.append("ai_tells_report decision=FAIL — run anti-ai-tells ensemble")
        except json.JSONDecodeError:
            reasons.append("ai_tells_report.json invalid")

    # refuse if REVIEW says blocking issues
    review = root/"review/blocking.json"
    if review.exists():
        try:
            blk = json.loads(review.read_text())
            if blk.get("blocking"):
                reasons.append("review/blocking.json still has blocking=true")
        except json.JSONDecodeError:
            reasons.append("blocking.json invalid")

    return {
        "decision": "PASS" if not reasons else "FAIL",
        "reasons": reasons,
        "n_chapters": len(chapters),
        "min_chapter_words": min_chapter_words,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--min-chapter-words", type=int, default=800)
    ap.add_argument("--min-chapters", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = check(args.root, args.min_chapter_words, args.min_chapters)
    print(json.dumps(out, indent=2) if args.json else out)
    return 0 if out["decision"]=="PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
