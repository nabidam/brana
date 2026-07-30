#!/usr/bin/env bash
# Distribution integrity check. The canon and the gate script each have
# exactly one source of truth (root WORKFLOW.md, tools/brana-gate) and one
# bundled copy inside skills/brana-plan/ so that skill-only installs carry
# them. This check fails when the bundle drifts from the source, or when any
# additional copy appears anywhere else in the repo.
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0

diff -q WORKFLOW.md skills/brana-plan/reference/WORKFLOW.md >/dev/null || { echo "DRIFT: skills/brana-plan/reference/WORKFLOW.md != WORKFLOW.md"; fail=1; }
diff -q tools/brana-gate skills/brana-plan/scripts/brana_gate.py >/dev/null || { echo "DRIFT: skills/brana-plan/scripts/brana_gate.py != tools/brana-gate"; fail=1; }

extra_gates=$(find . -path ./.git -prune -o -type f \( -name 'brana_gate.py' -o -name 'brana-gate' \) -print \
  | grep -v -e '^./tools/brana-gate$' -e '^./skills/brana-plan/scripts/brana_gate.py$' || true)
[ -n "$extra_gates" ] && { echo "EXTRA gate copies:"; echo "$extra_gates"; fail=1; }

extra_canons=$(find . -path ./.git -prune -o -path ./docs -prune -o -type f -name 'WORKFLOW.md' -print \
  | grep -v -e '^./WORKFLOW.md$' -e '^./skills/brana-plan/reference/WORKFLOW.md$' || true)
[ -n "$extra_canons" ] && { echo "EXTRA canon copies:"; echo "$extra_canons"; fail=1; }

[ "$fail" -eq 0 ] && echo "check-dist: OK (1 source + 1 bundle each)"
exit "$fail"
