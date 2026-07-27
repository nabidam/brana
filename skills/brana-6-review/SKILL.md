---
name: brana-6-review
description: "Use for code review after an implementation batch, at a planned demo-gate task, or before merging a feature branch; also when the user asks for code review, bug check, security check, product review, walkthrough, the v1 exit bar, architecture compliance, or says phase 6."
---

# Phase 6 — Review: Code (6a) + Product (6b)

Code review alone lets everything a compiler can't see — bad flows, bad layouts, integration bugs — ship unexamined. 6a reviews diffs after each 2–3-task implementation batch. 6b runs only at planned demo-gate tasks — roughly one per 8–10 feature tasks' worth of chunks (~3–4 chunks), minimum one and placed where runnable — plus the release gate before merge.

## Modes

- **run** (default): execute 6a below; if the current TASKS.md position is at a demo-gate task, run 6b instead.
- **prompt** (argument contains `prompt`): output the paste-ready reviewer prompt from the templates below with the actual git diff + relevant contract sections embedded. No other output.
- Argument contains `6b`, `gate`, or `product`: run 6b directly.

## 6a — Code review (run mode)

Reviewer must be a **different model than the implementer** — default Opus 4.8 reviewing Sonnet's code; cross-vendor (prompt mode) preferred when the user is in chat UIs anyway, a different vendor catches more.

**Reviewer independence:** the reviewer gets the diff and the contracts — never the implementer's report, self-review, or rationale; those are unverified claims that anchor the review. Never pre-judge the review ("do not flag X", "at most low severity") — a stated rationale never downgrades a finding. A finding that conflicts with the plan itself escalates to the user ("which governs?"), never gets silently resolved either way.

**Precondition:** lint and typecheck must be green before a 6a review starts — a finding a linter could catch is a lint-config gap, not a review finding; fix the config, not the code, and re-run.

1. Get the diff from git: commits since the range recorded in the last `specs/NNN-name/reviews/REVIEW_N.md` for mid-feature cadence (no prior review → since branch point), or the full branch diff before merge. Never review code that isn't in the diff.
2. Read only the ARCHITECTURE.md contract sections the diff touches, plus CONVENTIONS.md, plus the reviewed tasks' acceptance criteria from TASKS.md. Diff touches UI → also DESIGN.md and the relevant UX.md screen sections.
3. Report only:
   1. bugs / logic errors
   2. security issues (injection, XSS, auth) — judged against ARCHITECTURE.md's threat model when it exists
   3. race conditions
   4. contract violations
   5. convention violations
   6. UI-only: design contract violations (raw values where DESIGN.md tokens exist, missing component/view states, contrast/focus failures) and **UX contract violations** (screen structure or flow steps diverging from UX.md). With a pre-built design system: bypassed the system (hand-rolled what it provides).
   7. test adequacy: an acceptance criterion with no test at its declared layer, a test that asserts nothing meaningful (runs without checking the outcome), or a test that mocks away the exact behavior the criterion requires.
   8. composition and fake integrity: a runtime or gate path that composes bespoke wiring instead of the production entry point with injected seams, or a fake of an external system that diverges from its wire contract (accepts what the contract rejects, or lacks the shared contract suite).
   9. dependency-plan violations: hand-rolled code duplicating a package ARCHITECTURE.md's dependency plan names, an import of a package the plan doesn't name, or a resolved direct-dependency version that differs from the approved plan.

   Each finding: file:line, severity (high/med/low), one-line fix. Objective checks only — no style opinions, no praise, no rewrites.
4. **Confirmation pass — findings are unverified claims.** Before any finding becomes a fix task (fixer-tier model): a bug, logic error, or race condition gets a reproduction — a failing test or concrete repro steps; a contract, convention, or design violation gets both sides quoted (code line + contract line). A finding that fails confirmation escalates to the user with the failed-confirmation note — never silently dropped, never blindly fixed; a reviewer false positive turned into a fix task is churn plus regression risk. The reproduction test lands with the fix and joins the suite.
5. Write findings to `specs/NNN-name/reviews/REVIEW_N.md` (next N) with each finding's confirmation status, reviewed commit range in the header — the next review starts from there. Each confirmed finding becomes a TASKS.md fix task quoting file:line and referencing the review file's path — findings are never fixed off the review output directly.
6. **Compound rule:** when the same specific rule or pattern — not the same numbered category — repeats a second time in one review cycle, its fix task also adds a CONVENTIONS.md line or a lint rule closing that class — the same class never needs a reviewer's eyes again.
7. Fixes go back to a Phase 5 session (Sonnet-tier fixer): apply confirmed findings, each repro test must now pass, full suite must still pass, change only flagged files.

## 6b — Product review (the demo gate)

The human plus the running app; zero tokens for the walkthrough itself. **Preflight first (agent):** run the **verify script**, build, launch via the gate task's preflight block (launch command + seed data), confirm the journey's entry point is reachable. Preflight fails → log `GATE BLOCKED` on the task (a defect, not a choice — distinct from `GATE SKIPPED`), route the breakage as fix tasks at the head of the queue, re-run the preflight after they land; the human is only invited to walk an app that provably runs. **Soft stop:** halt the turn, print the gate task's journey script plus its launch command, and wait for the walkthrough result (screenshots optional but recommended — cheap context for fixes). "Continue" skips — log `GATE SKIPPED` on the task in TASKS.md; every skipped gate is surfaced at the v1 exit bar.

After a passed gate, complete its **crystallization coverage step** in the same session. Compare the scripted journey with the existing journey suite: full coverage → rerun and record serving test paths; partial coverage → extend an existing test only for uncovered behavior; no suitable test → create one. Never duplicate a test merely because this is a new gate — but the unglamorous step rotates across gates, so a full-coverage claim must name the test serving *this* gate's rotated step. Quote the coverage test path(s) in the completion mark (`` coverage `tests/...` ``, WALKED and SKIPPED alike); `brana-gate` verifies each cited path exists. The gate task is not Done, and no feature task may start, until cumulative journey coverage is green. A `GATE SKIPPED` gate runs the same coverage check immediately from the script; the walkthrough remains `UNWITNESSED` until eventually walked, at latest the v1 exit bar. A skip costs human attention debt, never automation debt.

The user's walkthrough:

1. Launch the app with the gate's launch command (the agent's preflight has already proven it boots).
2. Walk the scripted journey from the gate task (kernel journey at minimum, once it exists).
3. Check each step against its falsifiable criterion — did the observable thing happen?
4. Optional: screenshot screens touched — archive under `specs/NNN-name/screenshots/`; they make fix prompts and the vision pass possible, but the walkthrough result alone passes the gate.
5. Judge the screens against UX.md (structure) and DESIGN.md (styling) — and against their own eyes. Reference pack → put the reference screenshot next to the app's; comparative judgment beats absolute. "Passes contracts but looks wrong" is a valid finding; contracts are floors, not ceilings.
6. Every finding becomes a task at the head of the queue. Feature work does not resume past a failed gate.

Optional token-assisted pass — screenshots to a vision-capable model (Sonnet-tier):

```
Here are screenshots of the app and the UX.md + DESIGN.md contracts:
[embed]. Report divergences from the contracts and the three changes
that would most improve clarity and hierarchy. Findings only.
```

**v1 exit bar:** the exit bar is the **release-gate task** and runs like any gate — preflight it (verify script, release build, launch via the production entry point, journey entry reachable; failure is `GATE BLOCKED`, fix tasks first). The preflight also re-runs `brana-gate tasks` (resolve via bundled `scripts/brana_gate.py` beside this SKILL.md, else PATH) — done-mark integrity fires here: every Done mark must quote its commit SHA and an existing non-empty evidence file, deps resolved in order; merged-form gate marks (WALKED and SKIPPED alike) must quote coverage test paths that exist on disk, and a SKIPPED mark needs its evidence path too; an evidence-less done-mark or an uncitable coverage claim is a machine finding, never a reviewer's recall. The bar: the kernel journey passes end-to-end in a release build through the production composition, witnessed by the user, including the unglamorous steps (restart, offline, error paths named in the PRD), _and_ cumulative journey-suite coverage for every kernel step is green in the release build, _and_ — when fakes stood in for an external system — the production-composition proof task and the verified-fake contract suites are Done/green, _and_ every PRD NFR budget is measured via its named measurement in the release build — at or under budget, or explicitly accepted over with the number recorded. Every `GATE SKIPPED` entry in TASKS.md is listed here with its `UNWITNESSED` walkthrough, and each is either walked now or explicitly accepted (automation coverage exists — the missing human witness is the recorded, accepted debt); an unresolved `GATE BLOCKED` fails the bar outright — a gate that never became runnable is a defect, not debt. Every gate's crystallization coverage step (legacy: crystallization task) must be done — reuse, extension, or creation is acceptable, but duplicate tests are not required. "All tasks Done" is not the bar; this is.

**Spawn route (pre-v1):** when fixing a `GATE BLOCKED` — any gate, including the release gate — reveals a missing subsystem or a new/changed contract (more than a few fix tasks, or a new ARCHITECTURE.md section), spawn a scoped child cycle in a new `specs/NNN-name/` dir (Phase 1→6 on the delta, Route C shape, ARCHITECTURE.md patched not regenerated). The parent gate stays `GATE BLOCKED` referencing the child spec; the stale-interface-block and stale-plan rules run on the parent's not-done tasks and patched PLAN.md sections; the parent preflight re-runs only after the child cycle completes.

## Prompt mode templates

Reviewer (different model/vendor than implementer — Opus 4.8, or GPT/Gemini cross-vendor):

Lint and typecheck must be green before running this prompt — a finding a linter could catch is a lint-config gap, not a review finding; fix the config, not the code, and re-run.

```
Review this diff against the attached contracts and acceptance criteria.
Report only:
(1) bugs/logic errors, (2) security issues — judged against
ARCHITECTURE.md's threat model when it exists, (3) race conditions,
(4) contract violations, (5) convention violations, (6) UI-only: design
contract violations (raw values where tokens exist, missing states,
contrast/focus failures) and UX contract violations (screen structure or
flow steps that diverge from UX.md), (7) test adequacy: an acceptance
criterion with no test at its declared layer, a test that asserts
nothing meaningful (runs without checking the outcome), or a test that
mocks away the exact behavior the criterion requires, (8) composition
and fake integrity: a runtime or gate path that composes bespoke
wiring instead of the production entry point with injected seams, or a
fake of an external system that diverges from its wire contract
(accepts what the contract rejects, or lacks the shared contract
 suite), (9) dependency-plan violations: hand-rolled code duplicating
 a package ARCHITECTURE.md's dependency plan names, an import of a
 package the plan doesn't name, or a resolved direct-dependency version
 that differs from the approved plan. Each finding:
file:line, severity, one-line fix. Objective checks only — no style
opinions, no praise, no rewrites.
[embed diff + relevant ARCHITECTURE.md sections + CONVENTIONS.md
+ the reviewed tasks' acceptance criteria from TASKS.md
+ DESIGN.md and UX.md screen sections if the diff touches UI]
```

Write findings to `specs/NNN-name/reviews/REVIEW_N.md`; confirm each finding first (repro for bugs/races, both sides quoted for contract/convention violations — unconfirmable findings escalate to the user), then each confirmed finding becomes a TASKS.md fix task referencing the review file's path. The same specific rule or pattern — not the same numbered category — twice in a cycle → the fix task also adds a CONVENTIONS.md line or lint rule.

Fixer (back to the implementation model):

```
A senior engineer reviewed your code; these findings are confirmed with
reproductions: [embed confirmed findings + repros]. Apply these fixes;
each repro test must now pass and join the suite. All existing tests
must still pass. Output only the changed files.
```
