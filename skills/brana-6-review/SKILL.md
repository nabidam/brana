---
name: brana-6-review
description: "Use after every 2-3 implemented tasks or before merging a feature branch, when the user asks for code review, bug check, security check, a demo gate, product review, walkthrough, the v1 exit bar, or whether the code matches the architecture contract, or says phase 6."
---

# Phase 6 — Review: Code (6a) + Product (6b)

Code review alone lets everything a compiler can't see — bad flows, bad layouts, integration bugs — ship unexamined. 6b is the half most workflows are missing. Cadence for both: every 2–3 tasks, and always before a feature branch merges.

## Modes

- **run** (default): execute 6a below; if the current TASKS.md position is at a demo-gate task, run 6b instead.
- **prompt** (argument contains `prompt`): output the paste-ready reviewer prompt from the templates below with the actual git diff + relevant contract sections embedded. No other output.
- Argument contains `6b`, `gate`, or `product`: run 6b directly.

## 6a — Code review (run mode)

Reviewer must be a **different model than the implementer** — default Opus 4.8 reviewing Sonnet's code; cross-vendor (prompt mode) preferred when the user is in chat UIs anyway, a different vendor catches more.

**Reviewer independence:** the reviewer gets the diff and the contracts — never the implementer's report, self-review, or rationale; those are unverified claims that anchor the review. Never pre-judge the review ("do not flag X", "at most low severity") — a stated rationale never downgrades a finding. A finding that conflicts with the plan itself escalates to the user ("which governs?"), never gets silently resolved either way.

1. Get the diff from git: commits since the range recorded in the last REVIEW_N.md for mid-feature cadence (no prior review → since branch point), or the full branch diff before merge. Never review code that isn't in the diff.
2. Read only the ARCHITECTURE.md contract sections the diff touches, plus CONVENTIONS.md. Diff touches UI → also DESIGN.md and the relevant UX.md screen sections.
3. Report only:
   1. bugs / logic errors
   2. security issues (injection, XSS, auth)
   3. race conditions
   4. contract violations
   5. convention violations
   6. UI-only: design contract violations (raw values where DESIGN.md tokens exist, missing component/view states, contrast/focus failures) and **UX contract violations** (screen structure or flow steps diverging from UX.md). With a pre-built design system: bypassed the system (hand-rolled what it provides).

   Each finding: file:line, severity (high/med/low), one-line fix. Objective checks only — no style opinions, no praise, no rewrites.
4. Write findings to `REVIEW_N.md` (next N), reviewed commit range in the header — the next review starts from there.
5. Fixes go back to a Phase 5 session (Sonnet-tier fixer): apply findings, full suite must still pass, change only flagged files.

## 6b — Product review (the demo gate)

The human plus the running app; zero tokens for the walkthrough itself. **Soft stop:** halt the turn, print the gate task's journey script, and wait for the walkthrough result (screenshots optional but recommended — cheap context for fixes). "Continue" skips — log `GATE SKIPPED` on the task in TASKS.md; every skipped gate is surfaced at the v1 exit bar.

The user's walkthrough:

1. Build and launch the actual app.
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

**v1 exit bar:** the kernel journey passes end-to-end in a release build, witnessed by the user, including the unglamorous steps (restart, offline, error paths named in the PRD). Every `GATE SKIPPED` entry in TASKS.md is listed here and either walked now or explicitly accepted. "All tasks Done" is not the bar; this is.

## Prompt mode templates

Reviewer (different model/vendor than implementer — Opus 4.8, or GPT/Gemini cross-vendor):

```
Review this diff against the attached contracts. Report only:
(1) bugs/logic errors, (2) security issues, (3) race conditions,
(4) contract violations, (5) convention violations, (6) UI-only: design
contract violations (raw values where tokens exist, missing states,
contrast/focus failures) and UX contract violations (screen structure or
flow steps that diverge from UX.md). Each finding: file:line, severity,
one-line fix. Objective checks only — no style opinions, no praise, no
rewrites.
[embed diff + relevant ARCHITECTURE.md sections + CONVENTIONS.md
+ DESIGN.md and UX.md screen sections if the diff touches UI]
```

Fixer (back to the implementation model):

```
A senior engineer reviewed your code and found these issues: [embed
findings]. Apply these fixes. All existing tests must still pass. Output
only the changed files.
```
