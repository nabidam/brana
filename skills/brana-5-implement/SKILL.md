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

Argument is the task id (e.g. `brana-5-implement 3`). No id → take the first incomplete task in the current cycle's TASKS.md. Refuse a TASKS.md not stamped `status: ready` (the Phase 4 task gate hasn't cleared; point back there). After a compaction or session flush, rebuild state from git log + TASKS.md done-marks (SHAs live there), never from remembered conversation — re-running a completed task is the classic post-compaction failure.

**Step 0, before Task 0 (every cycle, run first):** `git branch --show-current`. On main/master, create the cycle branch (named after the spec dir, e.g. `001-core`) before touching any code. Direct-to-main only when the human explicitly says so this turn, or as a standing rule in CONVENTIONS.md (Git Rule 1).

**Demo-gate task → preflight, then soft stop.** (The release-gate task runs this same path, with a release build launched via the production entry point.) Run the gate's preflight yourself first: run the **verify script**, build, launch via the gate task's launch command, seed the fixture data, confirm the journey's entry point is reachable in the running app. Preflight fails → log `GATE BLOCKED` on the task (distinct from `GATE SKIPPED` — blocked is a defect, not a choice), turn the breakage into fix tasks at the head of the queue, and re-run the preflight after they land; never invite the user to walk an app that won't run. **Spawn route:** when fixing a blocked gate reveals a missing subsystem or a new/changed contract (more than a few fix tasks, or a new ARCHITECTURE.md section), don't wedge it into the current TASKS.md — spawn a scoped child cycle in a new `specs/NNN-name/` dir (Phase 1→6 on the delta, Route C shape, ARCHITECTURE.md patched not regenerated); the parent gate stays `GATE BLOCKED` referencing the child spec, the stale-interface-block and stale-plan rules run on the parent's not-done tasks and patched PLAN.md sections, and the parent preflight re-runs only after the child cycle completes. Preflight passes → do not implement past the gate: halt the turn, print the gate's journey script plus its launch command, and wait for the user's walkthrough result (screenshots optional but recommended; archive any under `specs/NNN-name/screenshots/`). Findings become tasks at the head of the queue. User replies "continue" → skip, but log `GATE SKIPPED` against the gate task in TASKS.md — visible debt, surfaced at the v1 exit bar, never silence. After a passed gate, finish the gate task's **crystallization coverage step in the same session** (Phase 4): inspect the existing journey suite against the scripted journey — full coverage means rerun and record the serving test paths; partial coverage means extend an existing test only for uncovered behavior; no suitable test means create one. Never duplicate a test solely because this is a new gate N. The gate task is Done only when the walkthrough result is recorded AND cumulative journey coverage is green; no feature task starts before that. Clear/flush the session after the crystallization coverage step, not before. A `GATE SKIPPED` gate does NOT defer the coverage check — run the same check immediately from the scripted journey; the walkthrough remains `UNWITNESSED` until eventually walked, at latest the v1 exit bar, and feature work proceeds once cumulative journey coverage is green. (Legacy TASKS.md with separate crystallization tasks: same rule, the separate task is the step.)

1. Read the task from `specs/NNN-name/TASKS.md`, root CONVENTIONS.md, and the task's context pack files. Task touches UI → also read root DESIGN.md and the task's UX.md screen section (backend-only tasks skip both). The pack is a prediction — verify against the real tree, add/drop reads as reality dictates.
2. Implement under these rules:
   - Only modify files listed in the task (adjusted per real tree).
   - Follow ARCHITECTURE.md contracts and CONVENTIONS.md exactly.
   - UI task: follow DESIGN.md (tokens only, no raw hex/px/font values) and match the UX.md screen section — regions, hierarchy, and all states (hover, focus-visible, disabled; empty, loading, error), not just the happy path.
   - Write the implementation plus unit tests covering the acceptance criteria.
   - No placeholders, no TODO comments, no truncation. No refactoring unrelated code, no future tasks.
   - **Ambiguity rule:** internal ambiguity (naming, private structure) → choose the simplest interpretation, note it in a comment. Resolving it would CHANGE OR DROP USER-VISIBLE BEHAVIOR the spec implies → STOP and ask the user instead of coding. A blanket "don't ask" turns silent feature cuts into code comments instead of alarms.
   - **Dependency rule (same STOP):** needing a capability ARCHITECTURE.md's dependency plan doesn't cover → propose the package (or the hand-roll) and ask. A resolver conflict or required change to an approved version is also a STOP for a plan patch and re-approval. Never silently add a dependency, change planned versions, or hand-roll what the plan assigns to a package.
   - **Scope cuts are hard stops.** Discovering mid-flight that a spec'd, user-visible behavior won't be built → state the cut and end the turn. No default-proceed; documenting it in a gotchas file is laundering, not a decision.
3. Run the **verify script** (Verification Machinery — not just the task's tests or the suite alone). Red → fix before committing.
4. Run the acceptance behavior itself — exercise it in the running app (or via a test that actually drives it). UI task: launch-and-look + screenshot only if the user asked or CONVENTIONS.md requires it; otherwise skip visual verification — the demo gate covers it. Green tests alone never mark Done — that is the classic failure.
5. **Migration task:** run up, then down, then up again against fixture data, with an assertion that the pre-up fixture data survives the round trip (not just that each step exits zero). Rollback always means the down migration, never `git revert` (Git Rule 2) — a reverted commit leaves the schema changed underneath a codebase that no longer expects it.
6. Commit (per CONVENTIONS.md commit style) and capture the **evidence file** at `specs/NNN-name/evidence/task-N.txt`: the exercised command (verify script, test, or journey step) plus the last ~30 lines of its output, captured live — not reconstructable from the diff afterward. Mark the task done in TASKS.md with the commit SHA plus the evidence file's path — grammar `` - **Done:** `SHA` — evidence `specs/NNN-name/evidence/task-N.txt` `` — which `brana-gate tasks` machine-checks on every re-run (SHA present, evidence file exists non-empty, deps resolved first); a done-mark without it doesn't pass the demo gate or the v1 exit bar.

Task 0 is always the scaffold: file tree from FILE_STRUCTURE.md, configs, data migrations, and ARCHITECTURE.md's approved dependency set installed in frozen/locked mode, with the lockfile or equivalent resolution artifact committed; no feature logic. If resolution reports a version/peer conflict or requires changing an approved version, stop and patch and re-approve the dependency plan — never chase the error with ad-hoc latest installs or independent upgrades/downgrades. Its smoke test is the app booting via a documented run command, recorded in CONVENTIONS.md. Task 0 also creates the **verify script** and sets up the linter/formatter/typecheck it runs per CONVENTIONS.md (machine-checkable conventions become lint rules, not review findings); UI stacks: verify also wires an automated a11y check (axe or equivalent) at Task 0; every stack: a dependency audit (npm audit / pip-audit / stack equivalent) and a secret scan, both failing the script; in agent mode, when the repo has a remote, Task 0 wires CI to run the verify script on push. Then the walking skeleton — the kernel journey passes in the real app before any feature deepening begins.

Stuck after two failed attempts within the batch session → stop and tell the user to escalate to Opus-tier with: task spec, current code, failing output, summary of attempts. The escalation may conclude the plan itself is wrong — then the fix is a PLAN.md edit, not more code attempts.

**Stale-plan rule:** any mid-cycle PLAN.md section rewrite (escalation verdict, spawn-route patch, human edit) reverts PLAN.md's stamp — and TASKS.md's — to `draft` until a scoped re-gate is clean: consistency checks re-run on the patched section, `brana-gate tasks` (resolve `brana-gate` via bundled `scripts/brana_gate.py` beside this SKILL.md, else PATH) re-runs on every task serving the patched chunk, and affected tasks/gate journeys are updated — before the next implementation session. A plan edited mid-flight without re-gating is the same self-certification seam the task gate closes. (Contract patches additionally trigger the stale-interface-block rule, Phase 7.)

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
- Dependency rule: needing a capability ARCHITECTURE.md's dependency
  plan doesn't cover is the same STOP — propose the package (or the
  hand-roll) and ask; a resolver conflict or required change to an
  approved version is also a STOP for a plan patch and re-approval.
  Never silently add a dependency, change planned versions, or hand-roll
  what the plan assigns to a package.
```

Escalation prompt (Opus-tier, only when stuck twice):

```
Sonnet has failed this task twice. Task spec: [embed]. Current code:
[embed]. Failing output: [embed]. Attempts: [summarize]. Diagnose the
root cause, then either provide corrected code or, if the plan itself is
wrong, rewrite the affected PLAN.md section.
```
