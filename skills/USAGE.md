# Brana v2 — Usage

Canon: `WORKFLOW.md`. Skills sequence it; this page is the golden path.

## New app (or new feature cycle)

```
1. /brana-plan    → interview + scope challenge + risk modules
                    → specs/NNN-name/PLAN.md (one canonical doc)
                    → self-review + brana-gate docs
                    → you read PLAN.md §§1–3 (~15 min — the intent check)
2. /brana-build   → cycle branch → U1 walking skeleton → kernel e2e (once)
                    → subagent per unit, verify green per unit, ledger line
                    → risk diffs reviewed immediately; rest batched
                    → say "show me" any time for a zero-ceremony demo
3. /brana-ship    → preflight → you walk the release build (kernel journey
                    + edge behaviors) → findings become fix units → merge
```

## Post-v1 change

```
/brana-ship [request] → routes it:
  Fix   — one unit, verify green, merge
  Cycle — new specs/NNN-name/PLAN.md on the delta (via /brana-plan)
Doc sync after every merge: amend living docs + brana-gate claims + ADR line.
```

## Hard stops (all modes)

Scope cut · user-visible ambiguity · out-of-plan dependency (strategic tier)
— the agent stops and asks; "continue" is never the default.

## What no longer exists (v1 → v2)

SPEC/UX/PRD/TASKS/FILE_STRUCTURE files, status stamps, consistency gate,
task gate, scheduled mid demo gates, per-gate crystallization, per-task
evidence files, GATE BLOCKED/SKIPPED bookkeeping, full/lite profiles,
fresh-session-per-phase. Replacements: one PLAN.md, plan self-review, risk
modules, kernel e2e written once, pull gates, the final walkthrough, and
`.brana/ledger.md`.
