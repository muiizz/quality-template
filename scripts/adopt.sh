#!/usr/bin/env bash
# Copy the gate files from quality-template into the current repo.
#
#   curl -fsSL https://raw.githubusercontent.com/muiizz/quality-template/<sha>/scripts/adopt.sh \
#     | bash -s -- <sha>
#
# Never overwrites an existing file unless --force or --update is given.
# Env: QT_SOURCE (a local path or git URL, default the GitHub repo).
set -euo pipefail

SOURCE="${QT_SOURCE:-https://github.com/muiizz/quality-template}"
FILES=(
  Makefile
  .pre-commit-config.yaml
  .gitleaks.toml
  .sqlfluff
  scripts/install-gitleaks.sh
  python/tools/mutation_gate.py
  .github/pull_request_template.md
  .github/workflows/check.yml
  .github/workflows/codeql.yml
  .github/dependabot.yml
  SECURITY.md
  GATES.md
)

force=0
update=0
ref=""
for arg in "$@"; do
  case "$arg" in
    --force) force=1 ;;
    --update) update=1; force=1 ;;
    *) ref="$arg" ;;
  esac
done
if [ "$update" = 1 ] && [ -z "$ref" ] && [ -f .quality-template-version ]; then
  ref="main"
fi
if [ -z "$ref" ]; then
  echo "usage: adopt.sh <commit-sha-or-tag> [--force]" >&2
  exit 2
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
git clone -q "$SOURCE" "$tmp/src"
git -C "$tmp/src" checkout -q "$ref"
sha="$(git -C "$tmp/src" rev-parse HEAD)"

if [ "$force" = 0 ]; then
  clash=0
  for f in "${FILES[@]}"; do
    if [ -e "$f" ]; then
      echo "exists: $f" >&2
      clash=1
    fi
  done
  if [ "$clash" = 1 ]; then
    echo "adopt: nothing copied. Re-run with --force to overwrite." >&2
    exit 1
  fi
fi

for f in "${FILES[@]}"; do
  mkdir -p "$(dirname "$f")"
  cp "$tmp/src/$f" "$f"
done
echo "$sha" > .quality-template-version
echo "adopt: copied ${#FILES[@]} files from quality-template $sha"
echo "next: edit the paths in Makefile for your layout, then run: make setup && make check"
