# Brana Skills (v2.0)

Three skills implementing `WORKFLOW.md` v2.0. Skills are thin routers: they
sequence the flow and point at the canon; the rules live in WORKFLOW.md only.

| Skill | Covers | Writes |
|---|---|---|
| `brana-plan` | Discover + Plan | `specs/NNN-name/PLAN.md` (single canonical artifact), `CONVENTIONS.md`, `DESIGN.md` (UI module only) |
| `brana-build` | Execute + Review | code + tests per unit, `.brana/ledger.md`, review findings |
| `brana-ship` | Release + Change | walkthrough close-out, change routing, doc sync, ADRs |

One persistent controller session per cycle; subagents per unit with
path-based packets. No mandated session flushes, no per-phase fresh sessions.

Deterministic checks: the gate script (`docs` for placeholder/contrast
scans, `claims` for cited-path grounding). Source of truth is
`tools/brana-gate`; `brana-plan` bundles a byte-identical copy
(`scripts/brana_gate.py`) plus the canon (`reference/WORKFLOW.md`) so
skill-only installs are self-contained — install all three skills together;
`tools/check-dist.sh` guards the bundle against drift.

v1's seven phase skills (`brana-1-spec` … `brana-7-change`) and the
nine-artifact document set are retired; see CHANGELOG 2.0.0 and
`docs/2026-07-30-v2-review.md` for the rationale and the before/after numbers.
