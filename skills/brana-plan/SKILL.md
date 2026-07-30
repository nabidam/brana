---
name: brana-plan
description: "Use for Brana v2 steps 1–2 (Discover, Plan): a new app idea, a spec, requirements, plan, architecture, UX flows, or task breakdown, or 'start the workflow'. Also answers legacy v1 phase names 1–4 (spec, UX/PRD/arch, plan, tasks) — v1 aliases only, not v2 numbering. Use before coding starts on a new project or feature cycle."
---

# Brana — Discover & Plan

Canon: `WORKFLOW.md` — resolve in order: (1) the Brana checkout's repo root,
(2) bundled beside this skill at `reference/WORKFLOW.md`. Gate script:
(1) `tools/brana-gate` in the checkout, (2) bundled at
`scripts/brana_gate.py` beside this skill. (Sibling skills reach both via
`../brana-plan/`.) Read §Principles, §Artifacts, §Risk Modules, §Units, and
Flow steps 1–2. This skill only sequences them; the rules live there.

## Steps

1. **Discover** (Flow §1): interview — ask what the user already has in mind
   before offering ideas; challenge vague requirements (AskUserQuestion for
   2–4-option decisions). Run the scope challenge: core promise, kernel
   (3–5 features), kernel journey (KJ-numbered steps), everything else
   backlog. Apply the minimal-form and provenance rules. Multi-subsystem or
   >~15 units → milestone split first (`specs/ROADMAP.md`).
2. **Propose risk modules** from the table in §Risk Modules — name each
   trigger you see; the user confirms the set.
3. **Write** `specs/NNN-name/PLAN.md` — the single canonical artifact, all 8
   sections from §Artifacts. Contracts stated once (producing unit or module
   section); interior units stay lean (outcome, deps, files, criteria).
   U1 is the walking skeleton. Also write/patch `CONVENTIONS.md` (≤1 page)
   if absent; `DESIGN.md` only when the UI-heavy module is active.
4. **Self-review, same session** (Flow §2): coverage → placeholders →
   consistency → gate script: `docs PLAN.md`, adding `DESIGN.md` as an
   argument whenever it exists (contrast only runs on DESIGN-named files it
   is passed). Fix inline.
5. Money/external/migration/auth module active → dispatch one independent
   architecture-review subagent (findings only, no author rationale). The
   user arbitrates findings.
6. Ask the user to read PLAN.md §§1–3 (intent check — no machine can do it),
   then hand off to `brana-build`.

Never write code here. Never create SPEC/UX/PRD/TASKS/FILE_STRUCTURE files —
those are v1 artifacts; v2 has one plan.
