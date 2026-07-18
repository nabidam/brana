---
name: brana-7-change
description: "Use for any post-v1 change to an app built with the workflow — add a feature, fix a bug, refactor, migrate schema, redesign UI — or when the user mentions impact analysis, doc sync, change routes A/B/C/R, phase 7, or the change loop."
---

# Phase 7 — Change Loop

Every change after v1 enters through triage. The living docs (ARCHITECTURE.md, UX.md, CONVENTIONS.md, DESIGN.md) are the source of truth — keep them accurate or every future impact analysis is poisoned. `FILE_STRUCTURE.md` is per-cycle now, archived under each `specs/NNN-name/` dir — never a root doc, never compared in doc sync.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): emit the paste-ready block for whichever step is current (impact analysis or doc sync — templates below), files embedded. No other output.

## Triage

Self-triage: pick the route, announce it + a one-line reason, and proceed — the user overrides by replying. Wrong-way-cheap mistakes are caught by the escalation rules below.

**Speed signal (hard rule):** the user saying "fast delivery", "no demo gates", "just ship it so I can test" or kin at cycle entry makes two proposals mandatory *before any cycle doc is drafted*: (1) the lite profile if the delta qualification holds; (2) an explicit delivery contract in the cycle SPEC.md's frontmatter (`delivery: demo_gates=waived ...` — closed vocabulary, WORKFLOW.md Delivery Contract). A waiver's substitute verification reuses existing machinery — never new tooling; tooling the process wants is process-derived scope for Phase 1's provenance check, priced and confirmed by the user. Waivers invented in TASKS.md frontmatter are a `brana-gate tasks --spec` finding.

| Route | Change type | Path |
|---|---|---|
| **A — trivial** | Bugfix, copy change, config tweak | Short-lived branch (Git Rule 3, human may waive per instance) → one hand-written task → Phase 5 (`brana-5-implement`) → verify (incl. journey suite) green before merge. No doc updates unless a behavior contract changed. Styling still obeys DESIGN.md tokens. |
| **B — small feature** | Fits existing architecture, no schema/API/module-boundary change | Mini-spec → impact analysis → Phase 4 on the delta → Phase 5/6 (incl. 6b). Feature branch. |
| **C — big feature** | New module, schema migration, new integration | Full Phase 1→6 scoped to the delta (`brana-1` … `brana-6`), new `specs/NNN-name/` dir. Phase 1 runs the **Route C delta qualification** (WORKFLOW.md, Route S): delta in one subsystem, ≤ ~15 tasks, no *new* external system (an integration already in ARCHITECTURE.md doesn't disqualify), delta stakes low → the cycle takes `profile: lite` regardless of the app's own profile. ARCHITECTURE.md and UX.md are patched (Opus-tier), never regenerated. Feature branch. |
| **R — refactor** | Refactor, dependency upgrade, debt paydown; no user-visible behavior change intended | Feature branch → verify + journey suite green BEFORE, as baseline → chunked tasks (~300-line cap, one green commit each) → verify green after each chunk → 6a on the full diff → doc sync (append **Decision log** entry if a boundary moved) → 6b only if UI touched → merge. |

No verify script / journey suite yet (pre-v1.1 app, or all gates were skipped) → Route R's and Route A's baseline preconditions are unsatisfiable as written; the route's first task is the backfill: create the verify script and crystallize the kernel journey, before any chunked/behavior work starts.

**Escalation rules:**

- Any change that mid-flight touches a schema/API/module boundary stops and re-enters as Route C — impact analysis re-run, quoted doc sections patched — before more tasks run. (Pre-v1, the same discovery inside a blocked gate routes through the Spawn route in Phase 6b.)
- Any change that mid-flight would drop or degrade user-visible behavior stops for the user's decision — same stop-the-line rule as Phase 5. Hard stop in every medium: state the cut, end the turn, no default-proceed. Route R additionally freezes on ANY user-visible change discovered mid-flight, not just a drop — a refactor that changes behavior isn't a refactor; same hard stop.
- **Stale-interface-block rule:** any mid-cycle contract patch (CONSUMES/PRODUCES section of ARCHITECTURE.md changes) triggers a cheap pass that diffs old vs. new contract and updates the CONSUMES/PRODUCES blocks of every not-done TASKS.md task quoting the changed section — before the next implementation session starts. An implementer working from a stale interfaces block is the seam-bug failure mode rule 8 exists to close.
- **Stale-plan rule (Phase 5) applies here too:** a mid-cycle PLAN.md section rewrite reverts PLAN.md and TASKS.md to `draft` until the scoped re-gate is clean — consistency checks on the patched section, `brana-gate tasks` (resolve `brana-gate` via bundled `scripts/brana_gate.py` beside this SKILL.md, else PATH) on the tasks serving the patched chunk — before the next implementation session.

**Review policy:** Routes B/C get one 6a review of the full feature diff plus one 6b walkthrough before merge. Route A gets 6a only if it touches logic, auth, or data handling — skip for copy, config, styling. Route R gets one 6a review of the full diff always (6a category 7 — test adequacy — matters most on a refactor) and 6b only if the diff touched UI.

**Redesigns:** a visual/UX rework is driven by observed failures — the user's usage notes and screenshots of what is bad and why — feeding a UX.md patch first. Re-specifying tokens and animation parameters without touching UX.md repaints the same wrong rooms.

**Git:** commit per green task (Git Rule 2). B/C/R work on a feature branch, merged only after Phase 6 review + doc sync (Git Rule 3). Route A uses a short-lived branch merged after verify is green; the human may waive the branch per instance.

## Route B steps (run mode)

1. **Mini-spec** — 5–15 lines, confirmed with the user: what, why, falsifiable acceptance criteria, out-of-scope. New dir `specs/NNN-name/SPEC.md` (create it directly) with frontmatter `status: draft`; task ids numbered fresh per dir. `specs/NNN-name/` also holds `evidence/` (per-task command output), `reviews/` (6a/6b writeups), and `screenshots/` (gate captures). `specs/` is append-only history — never edit merged dirs.
2. **Impact analysis** (Opus-tier, fresh session) — against ARCHITECTURE.md + UX.md, answer only: (1) does this fit the existing architecture, or does a module boundary/schema/API contract need to change? (2) which screens/flows in UX.md does it touch or add? (3) which existing files are affected? (4) which doc sections need edits (quote them)? No code, no plan yet. "Fits" → continue; stamp the mini-spec `status: gate-passed` (impact analysis is Route B's gate). "Needs change" → escalate to Route C; the quoted sections are patched before any tasks are written.
3. Phase 4 on the delta (`brana-4-tasks`), then Phase 5/6 per task, 6b walkthrough before merge.

## Doc sync (after every merged B/C/R feature — non-optional)

Haiku/Flash-tier work. Compare ARCHITECTURE.md, UX.md, and DESIGN.md against the feature's branch diff. List every statement in the docs now false, with the correction (include new screens, tokens, or components the feature added that the docs don't list); apply the corrections directly to the source docs. Then run `brana-gate claims ARCHITECTURE.md UX.md CONVENTIONS.md DESIGN.md` from the repo root (resolve `brana-gate` via bundled `scripts/brana_gate.py` beside this SKILL.md, else PATH; skip absent docs) — every backticked path a living doc cites must exist in the working tree; a clean exit is part of the sync, not optional. A doc citing a file the feature renamed is exactly the poisoned-impact-analysis failure doc sync exists to prevent. If a module boundary moved or a non-obvious decision was made, also draft and append one **Decision log** line (`YYYY-MM-DD — decision — why`) to ARCHITECTURE.md's Decision log — append-only, never delete an earlier entry's why. Never record divergence as a "deviations" appendix or gotchas list — amend the statement that became false. FILE_STRUCTURE.md is out of scope here — it's per-cycle, archived with its `specs/NNN-name/` dir, never corrected in place. Cheap, mechanical — stale docs are the failure mode that kills this workflow at scale.

## Scaling note

Context packs work at 20 files, degrade at 200. When the Phase 4 splitter starts guessing wrong, feed it a code map first — one-paragraph summary per module, regenerated by a cheap model after each Route C change.

## Prompt mode templates

Impact analysis (Opus-tier, fresh session):

```
Here are ARCHITECTURE.md, UX.md, and a feature request: [embed].
Answer only: (1) does this fit the existing architecture, or does a
module boundary/schema/API contract need to change? (2) which screens/
flows in UX.md does it touch or add? (3) which existing files are
affected? (4) which doc sections need edits (quote them)?
Do not write code or a plan.
```

Doc sync (Haiku/Flash-tier):

```
Here are ARCHITECTURE.md / UX.md / DESIGN.md and the diff of the last
feature: [embed]. List every statement in the docs now false, with the
correction (include new screens, tokens, or components the feature
added that the docs don't list). If a module boundary moved or a
non-obvious decision was made, also draft one Decision log line:
`YYYY-MM-DD — decision — why`. Output only the corrections and the log
line.
```
