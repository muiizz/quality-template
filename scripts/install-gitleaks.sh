#!/usr/bin/env bash
# Install a pinned gitleaks into .tools/ and verify its checksum. Linux x86_64 only.
set -euo pipefail

VERSION="8.30.1"
SHA256="551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
DEST="$(cd "$(dirname "$0")/.." && pwd)/.tools"

if [ -x "$DEST/gitleaks" ] && "$DEST/gitleaks" version | grep -q "$VERSION"; then
  exit 0
fi
if [ "$(uname -s)-$(uname -m)" != "Linux-x86_64" ]; then
  echo "install-gitleaks: only Linux x86_64 is scripted. Install gitleaks $VERSION yourself" >&2
  echo "and put it at $DEST/gitleaks." >&2
  exit 1
fi
mkdir -p "$DEST"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
url="https://github.com/gitleaks/gitleaks/releases/download/v${VERSION}/gitleaks_${VERSION}_linux_x64.tar.gz"
curl -fsSL "$url" -o "$tmp/gitleaks.tar.gz"
echo "$SHA256  $tmp/gitleaks.tar.gz" | sha256sum -c - >/dev/null
tar -xzf "$tmp/gitleaks.tar.gz" -C "$tmp" gitleaks
install -m 0755 "$tmp/gitleaks" "$DEST/gitleaks"
echo "installed gitleaks $VERSION"
