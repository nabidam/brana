---
name: brana-ship
description: "Use when the cycle's units are done and the user wants to release, walk through, or close the spec — or for any post-v1 change: new feature, bugfix, refactor, migration, redesign. Covers Brana phases 6b–7, release gate, walkthrough, doc sync, change routes."
---

# Brana — Release & Change

Canon: `WORKFLOW.md` — resolve: (1) Brana checkout root, (2)
`../brana-plan/reference/WORKFLOW.md` beside this skill. Gate script:
(1) `tools/brana-gate`, (2) `../brana-plan/scripts/brana_gate.py`. Read
Flow §§5–6. This skill sequences; rules live there.

## Release (closes the cycle)

1. **Preflight** (agent): verify green, release build, launch via the
   production entry point (deployment module: production composition,
   disposable config), walkthrough entry reachable. Failure → fix units
   first; never invite the user to walk an app that doesn't run.
2. **Soft stop**: print PLAN.md §8 (walkthrough script: kernel journey +
   edge behaviors) and the launch command; wait for the user's walkthrough.
   Measure NFR budgets by their named commands. Findings → fix units at the
   head of the queue → re-walk.
3. Walkthrough passes → merge the branch; `specs/NNN-name/` is history.
   Record cycle metrics in the ledger footer (§Measurement).

## Change (post-v1)

Self-triage, announce route + one-line reason; user overrides by replying:

- **Fix** — bugfix/copy/config: branch → one unit → verify green (kernel
  e2e included) → merge. Independent review only if a risk-module area is
  touched.
- **Cycle** — user-visible or structural: new `specs/NNN-name/PLAN.md` on
  the delta via `brana-plan`; risk modules re-evaluated for the delta;
  living docs patched, never regenerated.

Mid-flight escalations (hard): change crosses a module boundary / schema /
wire contract → stop, re-enter as Cycle. Refactor changes user-visible
behavior → stop, it isn't a refactor.

## Doc sync (after every merge)

Amend every living-doc statement the diff made false (never a deviations
appendix); run the gate script's `claims` subcommand on living docs (cited
paths must exist); one ADR line per non-obvious decision (`docs/adr/`).
Cheap, mechanical, non-optional.
