---
name: brana-4-tasks
description: "Use when PLAN.md exists and the user wants it split into implementation tasks, asks for a task list or task breakdown, says create tasks or break this into tasks, or says phase 4."
---

# Phase 4 — TASKS.md

**Locating `brana-gate`:** every `brana-gate` invocation below resolves in order — (1) `scripts/brana_gate.py` bundled beside this SKILL.md (run `python3 <skill-dir>/scripts/brana_gate.py ...`); (2) `brana-gate` on PATH; (3) `tools/brana-gate` when the working directory is the Brana repo itself. None found -> state which locations were checked, then the full checklist runs as the LLM pass (copy-paste mode).

Split the plan into tasks small enough that each fits one implementation prompt. Task size is the workflow's unit of safety: a task that fits in one prompt can be verified, committed, and rolled back alone. Blocked until the Phase 3 consistency gate's machine pass is clean — refuse a PLAN.md still stamped `status: draft`; point back to Phase 3. Route B delta (no PLAN.md): the mini-spec must be stamped `gate-passed` by impact analysis. **Route S delta (SPEC.md `profile: lite`, no PLAN.md):** refuse a SPEC.md still stamped `draft`; split from SPEC.md's kernel journey + acceptance criteria and ARCHITECTURE.md; author the DEMO GATE (≥1) and RELEASE GATE tasks directly here with full gate anatomy (journey, preflight block, unglamorous step, crystallization task); the task gate runs `brana-gate tasks` without `--plan` (chunk checks skip) and every other check stands.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): output the paste-ready prompt block for whichever step is current — the splitter (Sonnet-tier target) or the task-gate machine pass (Haiku/Flash-tier target) — from the templates below, actual files embedded. No other output.

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
- Every DEMO GATE task is immediately followed by a **crystallization task**: it encodes the gate's scripted journey (including its unglamorous step) as an automated e2e test on the harness named in CONVENTIONS.md's Test strategy; the new test joins the journey suite. No feature task may start before its preceding gate's crystallization task is done. A `GATE SKIPPED` gate does NOT defer the encoding — writing the e2e needs only the scripted journey, not a walkthrough: the crystallization task runs immediately and its test is marked `UNWITNESSED` (same visible-debt mark as the gate) until the journey is eventually walked, at latest the v1 exit bar. Feature work proceeds once the unwitnessed test is green — a skip costs human attention debt, never automation debt.
- **Verified-fake rule** (only when ARCHITECTURE.md has wire contracts): a task producing a fake of an external system gets a `[contract]` criterion running ONE shared suite against both the fake and the real adapter, asserting the wire contract — the fake must reject what the contract rejects. The real-adapter side is offline (request-shape assertions, recorded fixtures); live provider calls happen only in a bounded canary task routed through the production composition.
- The walking-skeleton milestone tasks come first and may not be reordered after feature tasks.
- Tasks tiny — ~50–300 lines of new code, one prompt each — but the count is a cost, not a virtue: emit the FEWEST tasks that respect the cap. **Merge bias:** two consecutive tasks in a linear dependency whose primary file is the same merge into one unless the merged task would exceed the cap. Task ids numbered fresh per cycle dir. Task 0 of a new app is always the scaffold (file tree from FILE_STRUCTURE.md, configs, data migrations, no feature logic); its smoke test is the app booting via a documented run command, recorded in CONVENTIONS.md.
- **No catch-all task:** a final "fill remaining gaps" task depending on (nearly) every other task is a blocking finding — every acceptance criterion belongs to the task that owns the behavior. Gate and crystallization tasks are the only sanctioned wide-dependency tasks. `brana-gate` flags this deterministically.
- **Delivery contract echo only:** TASKS.md frontmatter carries `status:` and, when SPEC.md declares one, a verbatim `delivery:` echo — never waiver/exception keys of its own. Waivers are chosen in SPEC.md at cycle entry (WORKFLOW.md, Delivery Contract); a waiver's substitute verification reuses existing machinery and never adds tasks. Tasks serving only operator surfaces (CLI/log output) reference UX.md's operator surface note and load no DESIGN.md.

Context packs are predictions made before code exists — mark them as hints; the implementation session verifies against real files. Interfaces blocks are firmer than packs: they quote the contract, and contract changes route through the docs, not through a task improvising. Isolation is for token budgets, not for truth: demo gates exist precisely because bugs live in the seams between well-tested tasks.

**Task schema (agent mode):** each task is a heading plus one fenced ```toml block — `id`, `type` (scaffold/feature/gate/crystallization/fix/proof/spike), `chunk`, `deps`, `files`, `consumes`/`produces` (exact quotes), `skeleton`, `fake_of`, `[[criteria]]` (text + layer, `gate` on e2e), and for gate tasks a `[gate]` table (`n`, `release`, `launch`, `seed`, `unglamorous`, `[[gate.journey]]` step + serving task id); full schema in `brana-gate --help`. The format exists so the task gate's structural half runs as a program, not as a model's recall; prose around the blocks stays free-form.

Write TASKS.md to the same `specs/NNN-name/` dir with frontmatter `status: draft` — the task gate below flips it to `ready` (Phase 5 refuses a draft TASKS.md). Do not write any code. Task completions done-mark against `specs/NNN-name/evidence/task-N.txt` (Verification Machinery in WORKFLOW.md) — TASKS.md need not restate the format, only that done-marks reference it.

## Task gate (blocks Phase 5)

Without this gate TASKS.md is self-certified — the splitter stamps its own output and the first integrity check is a gate preflight *during* Phase 5, the most expensive moment to learn a journey step has no serving task. Every check is cross-referencing, not judgment; machine pass only — intent was already checked at the Phase 3 consistency gate, and TASKS.md is a mechanical derivation of PLAN.md.

**Script-first:** run `brana-gate tasks TASKS.md --plan PLAN.md --arch ARCHITECTURE.md --spec SPEC.md` — it covers every structural check in the list below deterministically; fix findings to a clean exit. Then an LLM pass (fresh session, Haiku/Flash tier) covers only the judgment remainder: is a journey step *semantically* served by the task claiming it; does a criterion actually restate its PLAN.md requirement. Copy-paste mode (no tool): the full checklist is the LLM pass. Against TASKS.md + PLAN.md + ARCHITECTURE.md's interface and wire-contract sections, list:

- every PLAN.md chunk with no task implementing it, and every task serving no chunk;
- every dependency cycle, and every walking-skeleton task ordered after a feature task;
- every gate-task journey step with no implementing task earlier in the order, and every such serving task missing from the gate's dependency ids;
- every CONSUMES quote with no earlier task whose PRODUCES matches it and no ARCHITECTURE.md section stating it;
- every acceptance criterion missing its layer tag; every `[e2e@gate-N]` criterion absent from gate N's journey; every task with a PRODUCES block missing its `[contract]` criterion;
- every gate task missing a preflight field (launch command; seed/fixture command when the journey needs data; dependency ids) or not immediately followed by its crystallization task; every gate journey missing its unglamorous step;
- a missing RELEASE GATE task; and — when ARCHITECTURE.md has wire contracts — a production-composition proof absent from the release gate's dependencies, plus every fake-producing task missing its shared-suite `[contract]` criterion;
- every catch-all task: a non-gate, non-crystallization task depending on (nearly) every other task and producing nothing;
- every waiver/exception key in TASKS.md frontmatter that is not a verbatim echo of SPEC.md's `delivery:` contract line.

Mandatory and blocking: fix all findings, re-run until clean, then flip TASKS.md `status: draft` → `ready`. A gate unwalkable on paper here is the same gate that would go `GATE BLOCKED` mid-implementation — this pass moves that discovery to the cheapest moment.

## Prompt mode templates

Splitter — Sonnet-tier model, fresh session:

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
  task**: it encodes the gate's scripted journey (including its
  unglamorous step) as an automated e2e test on the harness named in
  CONVENTIONS.md's Test strategy; the new test joins the journey
  suite. No feature task may start before its preceding gate's
  crystallization task is done. A GATE SKIPPED gate does NOT defer
  the encoding — the e2e needs only the scripted journey, not a
  walkthrough: the crystallization task runs immediately and its test
  is marked UNWITNESSED (same visible-debt mark as the gate) until
  the journey is eventually walked, at latest the v1 exit bar.
  Feature work proceeds once the unwitnessed test is green.
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
- Tasks tiny: ~50–300 lines of code, one prompt each — but emit the
  FEWEST tasks that respect the cap: two consecutive tasks in a linear
  dependency sharing a primary file merge unless the merge exceeds it.
- No catch-all task: a final "fill remaining gaps" task depending on
  (nearly) every other task is a blocking finding — every criterion
  belongs to the task owning the behavior; only gate and
  crystallization tasks may depend wide.
Task done-marks reference `specs/NNN-name/evidence/task-N.txt`
(Verification Machinery in WORKFLOW.md) — note this in TASKS.md, do
not restate the format.
Output TASKS.md as a numbered list. Do not write any code.
[embed PLAN.md + UX.md flow section + PRD.md error/edge-case list]
```

Task gate — Haiku/Flash-tier model, fresh session:

```
Here are TASKS.md, PLAN.md, and ARCHITECTURE.md's interface and wire-
contract sections: [embed]. Findings in TASKS.md only — list:
- every PLAN.md chunk with no task implementing it, and every task
  serving no chunk;
- every dependency cycle, and every walking-skeleton task ordered
  after a feature task;
- every gate-task journey step with no implementing task earlier in
  the order, and every such serving task missing from the gate's
  dependency ids;
- every CONSUMES quote with no earlier task whose PRODUCES matches it
  and no ARCHITECTURE.md section stating it;
- every acceptance criterion missing its layer tag; every
  [e2e@gate-N] criterion absent from gate N's journey; every task
  with a PRODUCES block missing its [contract] criterion;
- every gate task missing a preflight field (launch command; seed/
  fixture command when the journey needs data; dependency ids) or not
  immediately followed by its crystallization task; every gate journey
  missing its unglamorous step;
- a missing RELEASE GATE task; and — when ARCHITECTURE.md has wire
  contracts — a production-composition proof absent from the release
  gate's dependencies, plus every fake-producing task missing its
  shared-suite [contract] criterion;
- every catch-all task: a non-gate, non-crystallization task depending
  on (nearly) every other task and producing nothing;
- every waiver/exception key in TASKS.md frontmatter that is not a
  verbatim echo of SPEC.md's delivery contract line.
Report only findings with task id + quote. No rewrites.
```
