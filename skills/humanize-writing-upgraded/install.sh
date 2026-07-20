#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-humanize-writing-upgraded}"
# Prefer bundled dual installer
if [ -f "$ROOT/scripts/install_skill_dual.sh" ]; then
  bash "$ROOT/scripts/install_skill_dual.sh" "$ROOT" --name "$NAME"
elif [ -f "$ROOT/../skillremix/scripts/install_skill_dual.sh" ]; then
  bash "$ROOT/../skillremix/scripts/install_skill_dual.sh" "$ROOT" --name "$NAME"
elif [ -f "$ROOT/../randomupgrade/scripts/install_skill_dual.sh" ]; then
  bash "$ROOT/../randomupgrade/scripts/install_skill_dual.sh" "$ROOT" --name "$NAME"
else
  DEST_C="$HOME/.claude/skills/$NAME"
  DEST_U="$HOME/.cursor/skills/$NAME"
  for d in "$DEST_C" "$DEST_U"; do
    rm -rf "$d"; mkdir -p "$d"
    tar -C "$ROOT" --exclude='.git' --exclude='.claude' --exclude='.cursor' -cf - . | tar -C "$d" -xf -
    echo "installed: $d"
  done
fi
