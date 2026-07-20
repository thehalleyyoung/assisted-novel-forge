# assisted-novel-forge

Remix of 10 middling creative-writing skills into one **autonomous or assisted** novel pipeline with shared handoff packs and an independent verify gate.

## Install

```bash
git clone <repo-url>
cd assisted-novel-forge
bash install.sh assisted-novel-forge
```

## Use (after install)

```text
/assisted-novel-forge assisted: write a literary novel about a lighthouse keeper who finds a door that shouldn't exist
```

```text
/assisted-novel-forge autonomous --chapters 12 --genre mystery: the floating market heist
```

```bash
python3 scripts/assist_mode_router.py --text "write my novel" --mode assisted
python3 scripts/handoff_pack.py init --root ./novel_project --title "Lighthouse" --mode assisted
python3 scripts/verify_gate.py --root ./novel_project --json
```

## Upstream

See `UPSTREAM.md` and `REMIX_PLAN.md`.
