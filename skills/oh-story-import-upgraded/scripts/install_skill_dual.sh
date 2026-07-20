#!/usr/bin/env bash
# Dual-install a skill package into ~/.claude/skills and ~/.cursor/skills.
# Excludes .git / .claude / .cursor to prevent recursive nest on re-install.
set -euo pipefail

usage() {
  echo "usage: $0 <skill-dir> [--name NAME] [--repo-root DIR] [--dry-run]" >&2
  exit 1
}

SKILL_DIR=""
NAME=""
REPO_ROOT=""
DRY=0

while [ $# -gt 0 ]; do
  case "$1" in
    --name) NAME="${2:-}"; shift 2 ;;
    --repo-root) REPO_ROOT="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) usage ;;
    *)
      if [ -z "$SKILL_DIR" ]; then SKILL_DIR="$1"; shift
      else usage
      fi
      ;;
  esac
done

[ -n "$SKILL_DIR" ] || usage
SKILL_DIR="$(cd "$SKILL_DIR" && pwd)"
[ -f "$SKILL_DIR/SKILL.md" ] || { echo "error: missing SKILL.md" >&2; exit 1; }

if [ -z "$NAME" ]; then
  NAME="$(basename "$SKILL_DIR")"
fi
NAME="$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9-]+/-/g; s/^-+//; s/-+$//')"

CLAUDE_DEST="${HOME}/.claude/skills/${NAME}"
CURSOR_DEST="${HOME}/.cursor/skills/${NAME}"

# Refuse to install FROM a destination into itself
case "$SKILL_DIR" in
  "$HOME/.claude/skills"|"$HOME/.cursor/skills"|"$HOME/.claude/skills/"*|"$HOME/.cursor/skills/"*)
    # OK if source is the skill dir itself being refreshed from a clean tree —
    # but never if path contains nested .claude/skills inside skill package copy loops
    ;;
esac

copy_one() {
  local dest="$1"
  if [ "$DRY" -eq 1 ]; then
    echo "dry-run: $SKILL_DIR -> $dest"
    return 0
  fi
  if [ "$SKILL_DIR" = "$dest" ]; then
    echo "error: refusing to install skill dir onto itself: $dest" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  mkdir -p "$dest"
  # Exclude VCS + prior dual-install mirrors to avoid infinite nesting
  tar -C "$SKILL_DIR" \
    --exclude='.git' \
    --exclude='.claude' \
    --exclude='.cursor' \
    --exclude='node_modules' \
    --exclude='randomupgrade-wip-*' \
    --exclude='skillremix-wip-*' \
    -cf - . | tar -C "$dest" -xf -
  echo "installed: $dest"
}

copy_one "$CLAUDE_DEST"
copy_one "$CURSOR_DEST"

if [ "$DRY" -eq 0 ]; then
  [ -f "$CLAUDE_DEST/SKILL.md" ] || { echo "error: Claude install incomplete" >&2; exit 1; }
  [ -f "$CURSOR_DEST/SKILL.md" ] || { echo "error: Cursor install incomplete" >&2; exit 1; }
  # Sanity: no nested self-copies
  if [ -d "$CLAUDE_DEST/.claude" ] || [ -d "$CURSOR_DEST/.cursor" ]; then
    echo "error: nested .claude/.cursor leaked into install — fix excludes" >&2
    exit 1
  fi
fi

if [ -n "$REPO_ROOT" ]; then
  REPO_ROOT="$(cd "$REPO_ROOT" && pwd)"
  copy_one "${REPO_ROOT}/.claude/skills/${NAME}"
  copy_one "${REPO_ROOT}/.cursor/skills/${NAME}"
fi

python3 - <<PY
import json
print(json.dumps({
  "skill": "$NAME",
  "source": "$SKILL_DIR",
  "claude": "$CLAUDE_DEST",
  "cursor": "$CURSOR_DEST",
  "dual_user_install": True,
  "dry_run": bool($DRY),
}))
PY
