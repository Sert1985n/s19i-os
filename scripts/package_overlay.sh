#!/usr/bin/env bash
set -euo pipefail

OUT="artifacts/s19i-overlay-$(date +%F_%H%M%S).tar.gz"
mkdir -p artifacts
tar -czf "$OUT" webui daemon api docs README.md .gitignore
echo "$OUT"
