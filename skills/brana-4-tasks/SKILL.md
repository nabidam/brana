---
name: brana-4-tasks
description: "Use when PLAN.md exists and the user wants it split into implementation tasks, asks for a task list or task breakdown, says create tasks or break this into tasks, or says phase 4."
---

# Phase 4 — TASKS.md

Split the plan into tasks small enough that each fits one implementation prompt. Task size is the workflow's unit of safety: a task that fits in one prompt can be verified, committed, and rolled back alone. Blocked until the Phase 3 consistency gate's machine pass is clean — refuse a PLAN.md still stamped `status: draft`; point back to Phase 3. Route B delta (no PLAN.md): the mini-spec must be stamped `gate-passed` by impact analysis.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): output the paste-ready prompt block from the template below with actual PLAN.md + UX.md flow section embedded (Sonnet-tier target). No other output.

## Run mode

Read the current cycle's PLAN.md (latest `specs/NNN-name/`), root ARCHITECTURE.md and UX.md. Split PLAN.md into small, isolated, sequential tasks. Each task includes:

- id, title, objective, inputs, outputs
- dependencies (task ids)
- files to create/modify
- acceptance criteria — **observable behaviors in the running app or a test that drives one**. "Compiles", "check passes", "renders" are gates, never the criterion.
- estimated difficulty
- **interfaces block**, quoted from ARCHITECTURE.md: **CONSUMES** — the exact signatures, payload shapes, or endpoints this task uses from other tasks' output; **PRODUCES** — the exact signatures later tasks may rely on. An isolated implementer must learn neighboring types from this block, never by reading neighbor code.
- **context pack**: the exact files to load into the implementation session plus the ARCHITECTURE.md sections to obey. UI tasks also name their UX.md screen ids and get DESIGN.md; backend-only tasks get neither.

Rules:

- Preserve PLAN.md's **DEMO GATE** entries as explicit tasks: journey to walk, observations required, the human's walkthrough result as the completion artifact (screenshots optional). A skipped gate is marked `GATE SKIPPED` on the task, never deleted.
- The walking-skeleton milestone tasks come first and may not be reordered after feature tasks.
- Tasks tiny — ~50–300 lines of new code, one prompt each. Task ids numbered fresh per cycle dir. Task 0 of a new app is always the scaffold (file tree from FILE_STRUCTURE.md, configs, data migrations, one smoke test, no feature logic).

Context packs are predictions made before code exists — mark them as hints; the implementation session verifies against real files. Interfaces blocks are firmer than packs: they quote the contract, and contract changes route through the docs, not through a task improvising. Isolation is for token budgets, not for truth: demo gates exist precisely because bugs live in the seams between well-tested tasks.

Write TASKS.md to the same `specs/NNN-name/` dir with frontmatter `status: ready` (Phase 5 refuses TASKS.md without it). Do not write any code.

## Prompt mode template

Sonnet-tier model, fresh session:

```
Split PLAN.md into small, isolated, sequential implementation tasks.
Each task: id, title, objective, inputs, outputs, dependencies (task
ids), files to create/modify, acceptance criteria, estimated difficulty,
an interfaces block, and a context pack (exact files to paste + the
ARCHITECTURE.md sections to obey; UI tasks also name their UX.md screen
ids and get DESIGN.md).
The interfaces block has two parts, quoted from ARCHITECTURE.md:
CONSUMES — the exact signatures, payload shapes, or endpoints this task
uses from other tasks' output; PRODUCES — the exact signatures later
tasks may rely on. An isolated implementer must learn neighboring types
from this block, never by reading neighbor code.
Rules:
- Acceptance criteria are observable behaviors in the running app or a
  test that drives one. "Compiles", "check passes", "renders" are gates,
  never the criterion.
- Preserve PLAN.md's DEMO GATE entries as explicit tasks: journey to
  walk, observations required, the human's walkthrough result as the
  completion artifact (screenshots optional). A skipped gate is marked
  GATE SKIPPED on the task, never deleted.
- The walking-skeleton milestone tasks come first and may not be
  reordered after feature tasks.
- Tasks tiny: ~50–300 lines of code, one prompt each.
Output TASKS.md as a numbered list. Do not write any code.
[embed PLAN.md + UX.md flow section]
```
