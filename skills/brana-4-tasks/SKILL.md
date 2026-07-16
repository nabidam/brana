---
name: brana-4-tasks
description: "Use when PLAN.md exists and the user wants it split into implementation tasks, asks for a task list or task breakdown, says create tasks or break this into tasks, or says phase 4."
---

# Phase 4 — TASKS.md

Split the plan into tasks small enough that each fits one implementation prompt. Task size is the workflow's unit of safety: a task that fits in one prompt can be verified, committed, and rolled back alone. Blocked until the Phase 3 consistency gate's machine pass is clean — refuse a PLAN.md still stamped `status: draft`; point back to Phase 3. Route B delta (no PLAN.md): the mini-spec must be stamped `gate-passed` by impact analysis.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): output the paste-ready prompt block from the template below with actual PLAN.md + UX.md flow section + PRD.md error/edge-case list embedded (Sonnet-tier target). No other output.

## Run mode

Read the current cycle's PLAN.md (latest `specs/NNN-name/`), root ARCHITECTURE.md, UX.md, and PRD.md (error/edge-case list). Split PLAN.md into small, isolated, sequential tasks. Each task includes:

- id, title, objective, inputs, outputs
- dependencies (task ids)
- files to create/modify
- acceptance criteria — **observable behaviors in the running app or a test that drives one**. "Compiles", "check passes", "renders" are gates, never the criterion. Tag every criterion with the layer that verifies it: `[unit]`, `[integration]`, `[contract]`, or `[e2e@gate-N]`. A `[e2e@gate-N]` criterion must appear as a step of gate N's journey — if it doesn't, add it there, not just here (the gate N task's journey as copied into TASKS.md is the amendable copy — PLAN.md is not re-edited here).
- estimated difficulty
- **interfaces block**, quoted from ARCHITECTURE.md: **CONSUMES** — the exact signatures, payload shapes, or endpoints this task uses from other tasks' output; **PRODUCES** — the exact signatures later tasks may rely on. An isolated implementer must learn neighboring types from this block, never by reading neighbor code. A task with a PRODUCES block gets one additional acceptance criterion, tagged `[contract]`: a test that calls the produced signature/endpoint exactly as specified and asserts the shape — catching drift before a consumer task ever reads it.
- **context pack**: the exact files to load into the implementation session plus the ARCHITECTURE.md sections to obey. UI tasks also name their UX.md screen ids and get DESIGN.md; backend-only tasks get neither.

Rules:

- Preserve PLAN.md's **DEMO GATE** entries as explicit tasks: journey to walk, observations required, a **preflight block** (exact build/launch command — a disposable/fixture path, fail-closed against non-disposable targets, when the journey would otherwise touch production state; seed/fixture command if the journey needs data; and the task ids whose output the journey walks — the gate depends on all of them), the human's walkthrough result as the completion artifact (screenshots optional). A journey step with no implementing task before the gate is a blocking finding — reorder or add the wiring task; never emit a gate that isn't walkable at its position. Every gate launch command is the production entry point with disposable inputs (same-composition rule) — a bespoke gate-only composition is the same blocking finding. PLAN.md's **RELEASE GATE** becomes a gate task too, same anatomy: its journey is the kernel journey in a release build, each step traced to a task exercised through the production composition, the production-composition proof task among its dependencies. A skipped gate is marked `GATE SKIPPED` on the task, never deleted. Append one unglamorous step to every gate journey, drawn from PRD.md's error/edge-case list, rotating across gates: restart → offline → invalid input → restart → ... — a gate never ships checking only the happy path.
- Every DEMO GATE task is immediately followed by a **crystallization task**: blocked until the gate's walkthrough passes, it encodes the just-walked journey (including its unglamorous step) as an automated e2e test on the harness named in CONVENTIONS.md's Test strategy; the new test joins the journey suite. No feature task may start before its preceding gate's crystallization task is done. A `GATE SKIPPED` gate defers its crystallization task instead — mark it `DEFERRED` with the same visible-debt mark as the gate; it unblocks once the journey is eventually walked, at latest the v1 exit bar. Feature work may proceed past a deferred crystallization task as part of the skip — the skip already accepted the debt.
- **Verified-fake rule** (only when ARCHITECTURE.md has wire contracts): a task producing a fake of an external system gets a `[contract]` criterion running ONE shared suite against both the fake and the real adapter, asserting the wire contract — the fake must reject what the contract rejects. The real-adapter side is offline (request-shape assertions, recorded fixtures); live provider calls happen only in a bounded canary task routed through the production composition.
- The walking-skeleton milestone tasks come first and may not be reordered after feature tasks.
- Tasks tiny — ~50–300 lines of new code, one prompt each. Task ids numbered fresh per cycle dir. Task 0 of a new app is always the scaffold (file tree from FILE_STRUCTURE.md, configs, data migrations, no feature logic); its smoke test is the app booting via a documented run command, recorded in CONVENTIONS.md.

Context packs are predictions made before code exists — mark them as hints; the implementation session verifies against real files. Interfaces blocks are firmer than packs: they quote the contract, and contract changes route through the docs, not through a task improvising. Isolation is for token budgets, not for truth: demo gates exist precisely because bugs live in the seams between well-tested tasks.

Write TASKS.md to the same `specs/NNN-name/` dir with frontmatter `status: ready` (Phase 5 refuses TASKS.md without it). Do not write any code. Task completions done-mark against `specs/NNN-name/evidence/task-N.txt` (Verification Machinery in WORKFLOW.md) — TASKS.md need not restate the format, only that done-marks reference it.

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
from this block, never by reading neighbor code. A task with a PRODUCES
block gets one additional acceptance criterion, tagged [contract]:
a test that calls the produced signature/endpoint exactly as specified
and asserts the shape — catching drift before a consumer task ever
reads it.
Rules:
- Acceptance criteria are observable behaviors in the running app or a
  test that drives one. "Compiles", "check passes", "renders" are gates,
  never the criterion. Tag every criterion with the layer that verifies
  it: [unit], [integration], [contract], or [e2e@gate-N]. A
  [e2e@gate-N] criterion must appear as a step of gate N's journey —
  if it doesn't, add it there, not just here (the gate N task's journey
  as copied into TASKS.md is the amendable copy — PLAN.md is not
  re-edited here).
- Preserve PLAN.md's DEMO GATE entries as explicit tasks: journey to
  walk, observations required, a preflight block (exact build/launch
  command — a disposable/fixture path, fail-closed against
  non-disposable targets, when the journey would otherwise touch
  production state; seed/fixture command if the journey needs data;
  and the task ids whose output the journey walks — the gate depends
  on all of them), the human's walkthrough result as the completion artifact
  (screenshots optional). A journey step with no implementing task
  before the gate is a blocking finding — reorder or add the wiring
  task; never emit a gate that isn't walkable at its position. Every
  gate launch command is the production entry point with disposable
  inputs (same-composition rule) — a bespoke gate-only composition is
  the same blocking finding. PLAN.md's RELEASE GATE becomes a gate
  task too, same anatomy: its journey is the kernel journey in a
  release build, each step traced to a task exercised through the
  production composition, the production-composition proof task among
  its dependencies. A
  skipped gate is marked GATE SKIPPED on the task, never deleted. Append
  one unglamorous step to every gate journey, drawn from PRD.md's
  error/edge-case list, rotating across gates: restart → offline →
  invalid input → restart → ... — a gate never ships checking only the
  happy path.
- Every DEMO GATE task is immediately followed by a **crystallization
  task**: blocked until the gate's walkthrough passes, it encodes the
  just-walked journey (including its unglamorous step) as an automated
  e2e test on the harness named in CONVENTIONS.md's Test strategy; the
  new test joins the journey suite. No feature task may start before
  its preceding gate's crystallization task is done. A GATE SKIPPED
  gate defers its crystallization task instead — mark it DEFERRED with
  the same visible-debt mark as the gate; it unblocks once the journey
  is eventually walked, at latest the v1 exit bar. Feature work may
  proceed past a deferred crystallization task as part of the skip —
  the skip already accepted the debt.
- Verified-fake rule (only when ARCHITECTURE.md has wire contracts):
  a task producing a fake of an external system gets a [contract]
  criterion running ONE shared suite against both the fake and the
  real adapter, asserting the wire contract — the fake must reject
  what the contract rejects. The real-adapter side is offline
  (request-shape assertions, recorded fixtures); live provider calls
  happen only in a bounded canary task routed through the production
  composition.
- The walking-skeleton milestone tasks come first and may not be
  reordered after feature tasks.
- Tasks tiny: ~50–300 lines of code, one prompt each.
Task done-marks reference `specs/NNN-name/evidence/task-N.txt`
(Verification Machinery in WORKFLOW.md) — note this in TASKS.md, do
not restate the format.
Output TASKS.md as a numbered list. Do not write any code.
[embed PLAN.md + UX.md flow section + PRD.md error/edge-case list]
```
