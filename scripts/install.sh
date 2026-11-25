#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

SCOPE="global"
PROJECT_DIR="$(pwd)"
CUSTOM_TARGET=""
CORE_ONLY=false
SKIP_CONFIG=false
INCLUDE_COMMANDS=true

CORE_SKILLS=(
  "grill-me"
  "project-planner"
  "systematic-debugging"
  "verification-before-done"
  "tdd-workflow"
  "code-review"
  "security-review"
  "git-commit"
  "readme-generator"
)

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [OPTIONS]

Install devkit-opencode skills, slash commands, AGENTS.md, and opencode.jsonc.

Options:
  --global            Install globally to ~/.config/opencode (default)
  --project [DIR]     Install into project DIR (.opencode/ + root AGENTS.md/opencode.jsonc)
  --target DIR        Install everything under a custom directory DIR (useful for testing)
  --core-only         Install only the 9 high-priority core skills
  --skip-config       Do not copy AGENTS.md or opencode.jsonc
  --no-commands       Do not copy commands/*.md
  -h, --help          Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global)
      SCOPE="global"
      shift
      ;;
    --project)
      SCOPE="project"
      if [[ $# -gt 1 && ! "$2" =~ ^- ]]; then
        PROJECT_DIR="$2"
        shift 2
      else
        shift
      fi
      ;;
    --target)
      [[ $# -lt 2 ]] && { echo "Missing value for --target" >&2; exit 1; }
      CUSTOM_TARGET="$2"
      shift 2
      ;;
    --core-only)
      CORE_ONLY=true
      shift
      ;;
    --skip-config)
      SKIP_CONFIG=true
      shift
      ;;
    --no-commands)
      INCLUDE_COMMANDS=false
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -n "$CUSTOM_TARGET" ]]; then
  SKILLS_DEST="$CUSTOM_TARGET/skills"
  COMMANDS_DEST="$CUSTOM_TARGET/commands"
  CONFIG_ROOT="$CUSTOM_TARGET"
elif [[ "$SCOPE" == "project" ]]; then
  SKILLS_DEST="$PROJECT_DIR/.opencode/skills"
  COMMANDS_DEST="$PROJECT_DIR/.opencode/commands"
  CONFIG_ROOT="$PROJECT_DIR"
else
  SKILLS_DEST="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/skills"
  COMMANDS_DEST="${XDG_CONFIG_HOME:-$HOME/.config}/opencode/commands"
  CONFIG_ROOT="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
fi

backup_and_copy() {
  local src="$1"
  local dst="$2"
  local ts
  ts="$(date +%Y%m%d-%H%M%S)"
  if [[ -e "$dst" ]]; then
    cp "$dst" "${dst}.bak.${ts}"
    echo "[backup] $dst -> ${dst}.bak.${ts}"
  fi
  cp "$src" "$dst"
  echo "[copy]   $dst"
}

mkdir -p "$SKILLS_DEST"

installed_skills=0
if [[ "$CORE_ONLY" == true ]]; then
  for skill in "${CORE_SKILLS[@]}"; do
    rm -rf "$SKILLS_DEST/$skill"
    cp -R "$REPO_ROOT/skills/$skill" "$SKILLS_DEST/$skill"
    installed_skills=$((installed_skills + 1))
  done
else
  for skill_dir in "$REPO_ROOT"/skills/*/; do
    skill_name="$(basename "$skill_dir")"
    rm -rf "$SKILLS_DEST/$skill_name"
    cp -R "$skill_dir" "$SKILLS_DEST/$skill_name"
    installed_skills=$((installed_skills + 1))
  done
fi
echo "[skills] Installed $installed_skills skill(s) into $SKILLS_DEST"

installed_cmds=0
if [[ "$INCLUDE_COMMANDS" == true && -d "$REPO_ROOT/commands" ]]; then
  mkdir -p "$COMMANDS_DEST"
  for cmd_file in "$REPO_ROOT"/commands/*.md; do
    cp "$cmd_file" "$COMMANDS_DEST/$(basename "$cmd_file")"
    installed_cmds=$((installed_cmds + 1))
  done
  echo "[cmds]   Installed $installed_cmds slash command(s) into $COMMANDS_DEST"
fi

if [[ "$SKIP_CONFIG" == false ]]; then
  mkdir -p "$CONFIG_ROOT"
  backup_and_copy "$REPO_ROOT/AGENTS.md" "$CONFIG_ROOT/AGENTS.md"
  backup_and_copy "$REPO_ROOT/config/opencode.jsonc.example" "$CONFIG_ROOT/opencode.jsonc"
fi

echo "Done! Launch OpenCode and verify with /verify or ask which skills are loaded."
