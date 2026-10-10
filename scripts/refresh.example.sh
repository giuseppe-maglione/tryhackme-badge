#!/usr/bin/env bash

set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# --- CUSTOM CONFIG ---
# REPLACE YOUR INFORMATION BELOW
USERNAME="TRYHACKME_USERNAME"
GITHUB_REPO="GITHUB_USERNAME/GITHUB_USERNAME"
COMMITTER_NAME="GITHUB_USERNAME"
COMMITTER_EMAIL="GITHUB_EMAIL"
THEME_CHOICE="cherry_dark"
TMP_PROFILE_REPO="$HOME/.github_profile"
# ---------------------------------

ENGINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

wait_for_network() {
  local i
  for i in $(seq 1 12); do
    if curl -fsS -m 8 -o /dev/null https://github.com 2>/dev/null; then
      return 0
    fi
    log "Network non pronta, attendo 20s..."
    sleep 20
  done
  return 1
}

if ! wait_for_network; then
  log "Nessuna rete disponibile — salto l'esecuzione."
  exit 0
fi

# clone the profile repository if it doesn't exist
if [ ! -d "$TMP_PROFILE_REPO/.git" ]; then
  log "Cloning profile repository ($GITHUB_REPO)..."
  git clone --quiet "git@github.com:$GITHUB_REPO.git" "$TMP_PROFILE_REPO"
fi

cd "$TMP_PROFILE_REPO" || exit 1
git fetch --quiet origin main
git reset --quiet --hard origin/main

mkdir -p assets

# generate svg badge
export THM_USERNAME="$USERNAME"
export OUTPUT_PATH="$TMP_PROFILE_REPO/assets/thm_badge.svg"
export THEME="$THEME_CHOICE"

log "Generating new SVG badge..."
source "$ENGINE_DIR/../src/venv/bin/activate"
python3 "$ENGINE_DIR/../src/generate.py"
deactivate

# save and push
git add assets/thm_badge.svg
if git diff --staged --quiet; then
  log "No changes to commit."
  exit 0
fi

log "Commit and push of the new badge..."
git -c user.name="$COMMITTER_NAME" -c user.email="$COMMITTER_EMAIL" \
  commit --quiet -m "chore: refresh TryHackMe badge"

for attempt in 1 2 3; do
  if git push --quiet origin HEAD:main; then
    log "Push completed successfully ✓"
    exit 0
  fi
  log "Push failed (attempt $attempt/3). Retrying in 15s..."
  sleep 15
done

log "ERROR: Push failed after 3 attempts."
exit 1