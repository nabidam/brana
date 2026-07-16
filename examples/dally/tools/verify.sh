#!/usr/bin/env bash
# Dally verify script — the single fail-closed gate every task and demo gate runs.
# Any check exiting non-zero aborts the whole script. Referenced by CONVENTIONS.md
# §Test strategy. Requires network (dependency + advisory-DB lookups), like every
# dependency auditor.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> ruff check"
ruff check .

echo "==> ruff format --check"
ruff format --check .

echo "==> mypy (strict on src/)"
mypy

echo "==> pip-audit (dally dependency closure)"
# Audit dally's OWN dependency resolution, not the ambient environment: resolve
# the project's deps fresh from the index (the versions a clean install / the
# release-gate venv would get) and audit exactly those. The local project itself
# is dropped — it is not on PyPI.
audit_report="$(mktemp)"
audit_reqs="$(mktemp)"
trap 'rm -f "$audit_report" "$audit_reqs"' EXIT
python3 -m pip install --quiet --dry-run --ignore-installed --report "$audit_report" . >/dev/null
python3 - "$audit_report" "$audit_reqs" <<'PY'
import json
import sys

report, out = sys.argv[1], sys.argv[2]
with open(report) as fh:
    data = json.load(fh)
lines = sorted(
    f"{i['metadata']['name']}=={i['metadata']['version']}"
    for i in data.get("install", [])
    if i["metadata"]["name"].lower() != "dally"
)
with open(out, "w") as fh:
    fh.write("\n".join(lines) + "\n")
PY
pip-audit --requirement "$audit_reqs"

echo "==> detect-secrets (secret scan)"
secrets_json="$(mktemp)"
trap 'rm -f "$audit_report" "$audit_reqs" "$secrets_json"' EXIT
detect-secrets scan src tests pyproject.toml tools >"$secrets_json"
python3 - "$secrets_json" <<'PY'
import json
import sys

with open(sys.argv[1]) as fh:
    results = json.load(fh).get("results", {})
if results:
    print("SECRETS DETECTED in:", ", ".join(results), file=sys.stderr)
    sys.exit(1)
print("no secrets found")
PY

echo "==> pytest"
pytest

echo "ALL CHECKS PASSED"
