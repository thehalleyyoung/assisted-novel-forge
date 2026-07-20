#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-assisted-novel-forge}"
bash "$ROOT/scripts/install_skill_dual.sh" "$ROOT" --name "$NAME"
# also install invocable subskills
for s in handoff-pack verify-gate continuity-bridge assist-mode-router; do
  if [ -d "$ROOT/subskills/$s" ]; then
    bash "$ROOT/scripts/install_skill_dual.sh" "$ROOT/subskills/$s" --name "$s"
  fi
done
# install buffed members
for d in "$ROOT"/skills/*-upgraded; do
  [ -d "$d" ] || continue
  n="$(basename "$d")"
  bash "$ROOT/scripts/install_skill_dual.sh" "$d" --name "$n"
done
echo "installed superskill + subskills + upgraded members"
