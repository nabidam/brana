#!/usr/bin/env bash
# Sync the canonical tools/brana-gate into every skill that invokes it.
# Run after any edit to tools/brana-gate, before release.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
for s in brana-3-plan brana-4-tasks brana-5-implement brana-6-review brana-7-change; do
  mkdir -p "$root/skills/$s/scripts"
  cp "$root/tools/brana-gate" "$root/skills/$s/scripts/brana_gate.py"
  chmod +x "$root/skills/$s/scripts/brana_gate.py"
done
echo "synced brana-gate into 5 skills"
