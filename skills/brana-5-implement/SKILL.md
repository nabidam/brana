---
name: brana-5-implement
description: "Use when the user says implement task N, do the next task, or asks to start coding or build a feature from a TASKS.md task list, or says phase 5."
---

# Phase 5 — Implement tasks

Sessions run per **batch of 2–3 tasks**, cleared at each demo gate — the gate is the natural flush point (copy-paste mode: fresh session per task). Batch size starts at 2–3, tuned per project; the tuned number lives in CONVENTIONS.md. Context per task: the task spec + conventions + the files it touches — reading may roam the repo, but **writing only touches files listed in the task**.

The deliverable is the running app, not green tests. Done = demonstrated: the task's behavior exercised in the running app (or via a test that actually drives it). Per-task visual verification (launch-and-look + screenshot) is **opt-in** — do it only if the user asked for it on this task or CONVENTIONS.md requires it; otherwise UI tasks pass on tests + acceptance behavior, and visual quality is the human's call at the next demo gate.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): output the paste-ready per-task prompt from the template below with the actual task spec, CONVENTIONS.md, and touched files embedded (Sonnet-tier target; Haiku/Flash for pure boilerplate). No other output.
- **delegate** (argument contains `delegate`): spawn a subagent (Agent tool, `run_in_background: false`). Controller ensures the branch (Step 0 below) before dispatching any task — a subagent never runs Step 0 itself. **Pass paths, not prose:** the prompt names the task id + TASKS.md path, CONVENTIONS.md path, the context-pack file paths (UI tasks: DESIGN.md + the UX.md screen section), the implementation rules from run-mode step 2, and run-mode steps 3–5 — the subagent reads the files itself. Never paste file contents into the dispatch and never re-narrate them (pasted content stays resident in this session; re-narration compresses lossily). Pick `model` by task type: `haiku` for pure boilerplate (loggers, configs, presentational components), `sonnet` for everything else — never a stronger model for first attempts. **Parallel dispatch** is allowed only for tasks with disjoint file sets and no dependency edge between them; anything else runs sequentially in one session. **Report contract:** ≤15 lines; status one of `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`; the commit SHA; the **evidence file** path (Verification Machinery). `BLOCKED`/`NEEDS_CONTEXT` route to the ambiguity/scope-cut rules — never guessed past. The report is unverified claims: check suite green, behavior demonstrated, task marked done in TASKS.md before accepting. Subagent fails twice → do not respawn; you (the stronger base model) take the task over directly, using the escalation prompt below as your diagnosis checklist.

## Run mode

Argument is the task id (e.g. `brana-5-implement 3`). No id → take the first incomplete task in the current cycle's TASKS.md. Refuse a TASKS.md not stamped `status: ready` (Phase 4's gate hasn't cleared). After a compaction or session flush, rebuild state from git log + TASKS.md done-marks (SHAs live there), never from remembered conversation — re-running a completed task is the classic post-compaction failure.

**Step 0, before Task 0 (every cycle, run first):** `git branch --show-current`. On main/master, create the cycle branch (named after the spec dir, e.g. `001-core`) before touching any code. Direct-to-main only when the human explicitly says so this turn, or as a standing rule in CONVENTIONS.md (Git Rule 1).

**Demo-gate task → preflight, then soft stop.** Run the gate's preflight yourself first: run the **verify script**, build, launch via the gate task's launch command, seed the fixture data, confirm the journey's entry point is reachable in the running app. Preflight fails → log `GATE BLOCKED` on the task (distinct from `GATE SKIPPED` — blocked is a defect, not a choice), turn the breakage into fix tasks at the head of the queue, and re-run the preflight after they land; never invite the user to walk an app that won't run. Preflight passes → do not implement past the gate: halt the turn, print the gate's journey script plus its launch command, and wait for the user's walkthrough result (screenshots optional but recommended; archive any under `specs/NNN-name/screenshots/`). Findings become tasks at the head of the queue. User replies "continue" → skip, but log `GATE SKIPPED` against the gate task in TASKS.md — visible debt, surfaced at the v1 exit bar, never silence. Clear/flush the session at each gate. After a passed gate, the next task is the gate's **crystallization task** (Phase 4) — it encodes the just-walked journey as an automated e2e test joining the journey suite; no feature task starts before it's done. A `GATE SKIPPED` gate instead marks its crystallization task `DEFERRED` (same visible-debt mark as the gate) and feature work proceeds past it — the deferred task unblocks once the journey is eventually walked, at latest the v1 exit bar.

1. Read the task from `specs/NNN-name/TASKS.md`, root CONVENTIONS.md, and the task's context pack files. Task touches UI → also read root DESIGN.md and the task's UX.md screen section (backend-only tasks skip both). The pack is a prediction — verify against the real tree, add/drop reads as reality dictates.
2. Implement under these rules:
   - Only modify files listed in the task (adjusted per real tree).
   - Follow ARCHITECTURE.md contracts and CONVENTIONS.md exactly.
   - UI task: follow DESIGN.md (tokens only, no raw hex/px/font values) and match the UX.md screen section — regions, hierarchy, and all states (hover, focus-visible, disabled; empty, loading, error), not just the happy path.
   - Write the implementation plus unit tests covering the acceptance criteria.
   - No placeholders, no TODO comments, no truncation. No refactoring unrelated code, no future tasks.
   - **Ambiguity rule:** internal ambiguity (naming, private structure) → choose the simplest interpretation, note it in a comment. Resolving it would CHANGE OR DROP USER-VISIBLE BEHAVIOR the spec implies → STOP and ask the user instead of coding. A blanket "don't ask" turns silent feature cuts into code comments instead of alarms.
   - **Scope cuts are hard stops.** Discovering mid-flight that a spec'd, user-visible behavior won't be built → state the cut and end the turn. No default-proceed; documenting it in a gotchas file is laundering, not a decision.
3. Run the **verify script** (Verification Machinery — not just the task's tests or the suite alone). Red → fix before committing.
4. Run the acceptance behavior itself — exercise it in the running app (or via a test that actually drives it). UI task: launch-and-look + screenshot only if the user asked or CONVENTIONS.md requires it; otherwise skip visual verification — the demo gate covers it. Green tests alone never mark Done — that is the classic failure.
5. **Migration task:** run up, then down, then up again against fixture data, with an assertion that the pre-up fixture data survives the round trip (not just that each step exits zero). Rollback always means the down migration, never `git revert` (Git Rule 2) — a reverted commit leaves the schema changed underneath a codebase that no longer expects it.
6. Commit (per CONVENTIONS.md commit style) and capture the **evidence file** at `specs/NNN-name/evidence/task-N.txt`: the exercised command (verify script, test, or journey step) plus the last ~30 lines of its output, captured live — not reconstructable from the diff afterward. Mark the task done in TASKS.md with the commit SHA plus the evidence file's path; a done-mark without it doesn't pass the demo gate or the v1 exit bar.

Task 0 is always the scaffold: file tree from FILE_STRUCTURE.md, configs, data migrations, no feature logic; its smoke test is the app booting via a documented run command, recorded in CONVENTIONS.md. Task 0 also creates the **verify script** and sets up the linter/formatter/typecheck it runs per CONVENTIONS.md (machine-checkable conventions become lint rules, not review findings); UI stacks: verify also wires an automated a11y check (axe or equivalent) at Task 0; in agent mode, when the repo has a remote, Task 0 wires CI to run the verify script on push. Then the walking skeleton — the kernel journey passes in the real app before any feature deepening begins.

Stuck after two failed attempts within the batch session → stop and tell the user to escalate to Opus-tier with: task spec, current code, failing output, summary of attempts. The escalation may conclude the plan itself is wrong — then the fix is a PLAN.md edit, not more code attempts.

## Prompt mode template

```
Implement Task N of TASKS.md.
Task spec: [embed task].
Conventions: [embed CONVENTIONS.md].
Design + UX contracts (UI tasks only): [embed DESIGN.md + the task's
UX.md screen section].
Current relevant files: [embed ONLY the files this task touches].

Rules:
- Only modify files listed in the task.
- Follow ARCHITECTURE.md contracts and CONVENTIONS.md exactly.
- UI task: follow DESIGN.md (tokens only, no raw values) and match the
  UX.md screen section pasted — regions, hierarchy, and all states
  (hover, focus, disabled; empty, loading, error), not just the happy
  path.
- Write the implementation plus unit tests covering the acceptance
  criteria. The full existing suite must still pass.
- Migration task: run up, then down, then up again against fixture
  data; assert the pre-up fixture data is intact after the round trip.
  Rollback means the down migration, never git revert.
- Output complete files with exact paths. No placeholders, no TODOs,
  no truncation. No refactoring unrelated code, no future tasks.
- Ambiguity rule: if the ambiguity is internal (naming, private
  structure), choose the simplest interpretation and note it in a
  comment. If resolving it would CHANGE OR DROP USER-VISIBLE BEHAVIOR
  the spec implies, STOP and output the question instead of code.
```

Escalation prompt (Opus-tier, only when stuck twice):

```
Sonnet has failed this task twice. Task spec: [embed]. Current code:
[embed]. Failing output: [embed]. Attempts: [summarize]. Diagnose the
root cause, then either provide corrected code or, if the plan itself is
wrong, rewrite the affected PLAN.md section.
```
