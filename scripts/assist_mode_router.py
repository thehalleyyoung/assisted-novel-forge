#!/usr/bin/env python3
"""Route autonomous vs assisted creative writing; reject wrong-sense intents."""
from __future__ import annotations
import argparse, json, re

NON_TRIGGERS = [
    (r"storybook|react native stor", "Storybook/UI component stories — not fiction"),
    (r"user stor(y|ies)|acceptance criteria|sprint backlog", "Agile user stories — not fiction"),
    (r"scientific manuscript|nature paper|arxiv", "Scientific manuscript — use sciwrite skills"),
    (r"seo blog|keyword density", "Marketing SEO — out of scope for novel forge"),
    (r"tweet thread|linkedin post only", "Social posts — not novel forge"),
]


def route(text: str, mode: str | None = None) -> dict:
    low = text.lower()
    for pat, reason in NON_TRIGGERS:
        if re.search(pat, low):
            return {"decision": "ABSTAIN", "reason": reason, "mode": None, "planner": None}
    mode = mode or (
        "autonomous"
        if re.search(r"autonomous|just write|full novel without asking", low)
        else "assisted"
    )
    if re.search(r"deslop|oh-story", low):
        planner = "story-upgraded"
    elif re.search(r"inkos|multi-agent novel", low):
        planner = "inkos-multi-agent-novel-writing-upgraded"
    elif re.search(r"webnovel|xianxia|穿越", low):
        planner = "novel-creator-upgraded"
    elif re.search(r"short story", low):
        planner = "story-upgraded"
    elif re.search(r"literary|workshop", low):
        planner = "novel-writer-upgraded"
    else:
        planner = "novel-creator-upgraded" if mode == "autonomous" else "novel-writer-upgraded"
    return {
        "decision": "ROUTE",
        "mode": mode,
        "planner": planner,
        "phases": [
            "writing-principles-upgraded",
            "worldbuilding-upgraded",
            "plot-structure-upgraded",
            "story-architecture-upgraded",
            planner,
            "chapter-writing-upgraded",
            "creative-writing-craft-upgraded",
            "better-writing-upgraded",
            "revision-upgraded",
            "story-review-upgraded",
            "anti-ai-tells",
            "verify-gate",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--mode", choices=["assisted", "autonomous"], default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = route(args.text, args.mode)
    print(json.dumps(out, indent=2))
    return 0 if out["decision"] != "ABSTAIN" else 2


if __name__ == "__main__":
    raise SystemExit(main())
