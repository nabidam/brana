# Brana Skills — Usage Guide

Seven skills implementing Brana, the 6-phase app-dev workflow + Phase 7 change loop (WORKFLOW.md v1.1). Each skill has **run** mode (executes in Claude Code, Agent Adaptation Layer applies) and **prompt** mode (emits paste-ready blocks for external chat UIs — copy-paste is the workflow's canon medium).

The workflow's guard: every task green, every doc consistent-looking, app unusable. Countermeasures baked into the skills — the deliverable is the running app; Done = demonstrated (with live verification evidence); demo gate every 2–3 tasks; scope cuts are hard stops; consistency gate before tasks; per-cycle docs carry `status:` stamps (`draft` → `gate-passed`; TASKS.md `ready`) that downstream phases refuse to consume unstamped.

---

## Quick Start — The Golden Path

### Building a new app (v1):

```
1. /brana-1-spec               → SPEC.md (idea → kernel/v1/backlog + kernel journey)
2. /brana-2-prd-arch           → UX.md + PRD.md + ARCHITECTURE.md  (read UX.md yourself!)
3. /brana-3-plan               → PLAN.md (walking skeleton first, demo gates) +
                              CONVENTIONS.md + DESIGN.md + FILE_STRUCTURE.md
                              + consistency gate (machine pass blocks Phase 4)
4. /brana-4-tasks              → TASKS.md (with context packs + demo-gate tasks)
5. /brana-5-implement          → implement in 2–3-task batches; halt at each demo gate
6. /brana-6-review             → 6a code review (diffs) + 6b product walkthrough
7. v1 exit bar: kernel journey passes in a release build, witnessed by you;
   every GATE SKIPPED walked or explicitly accepted
```

### Post-v1 iteration (change loop):

```
1. /brana-7-change [request]   → agent self-triages A/B/C/R, announces route, proceeds
2. Route B: mini-spec → impact analysis → Phase 4 on delta → Phase 5/6 (incl. 6b)
3. Route C: full Phase 1–6 scoped to delta
4. Route R: verify + journey suite green as baseline → chunked tasks → 6a on full diff → doc sync
5. After merge (B/C/R): doc sync (mandatory) on ARCHITECTURE/UX/DESIGN
```

---

## Skill Details

### Phase 1 — `/brana-1-spec`

**Triggers:** "I have an app idea", "let's build X", "write a spec", "check my draft", "phase 1"

Scope decomposition first (multi-subsystem ideas split into per-cycle sub-products), then gap-check (has draft) or interview (from nothing — ask the user's own thinking first; AskUserQuestion multiple-choice when options are enumerable). Multiple plausible directions → 2–3 approaches with trade-offs, options presented **before** the recommendation. Then the **required scope challenge**: core promise in one sentence, KERNEL (3–5 features), KERNEL JOURNEY (end-to-end story exercising every kernel feature — becomes the walking-skeleton target and the standing demo-gate script), ranked backlog. Convenience features are backlog by default. Integration check before writing (combine answers, probe non-obvious consequences; uncertainty → explicit assumption). Design direction required (3 adjectives, reference apps, density, WCAG AA) — or name a pre-built design system / reference pack. After writing: spec self-review (placeholders, contradictions, scope, ambiguity) fixed inline before you read it.

**Output:** `specs/001-core/SPEC.md`, under 500 words plus the kernel section.

### Phase 2 — `/brana-2-prd-arch`

**Triggers:** "UX", "screens", "wireframes", "write the PRD", "architecture", "phase 2"

Order matters: **UX → PRD → ARCHITECTURE**. UX.md (root, living doc) is the floor plan: screen inventory with ids, navigation map, per-screen text wireframes with empty/loading/error states, key flows, density notes. PRD acceptance criteria must be falsifiable (observable behavior, never adjectives or "tests pass"). ARCHITECTURE.md commits to one stack, maps component hierarchy to UX screen ids, and obeys the traceability rule: every kernel-journey step names its serving API call/event.

**Read UX.md and walk the flows yourself before Phase 3** — intent is the one thing no machine check verifies.

### Phase 3 — `/brana-3-plan`

**Triggers:** "implementation plan", "conventions", "design system", "consistency gate", "phase 3"

Opus-tier leverage point. PLAN.md's first milestone is the **walking skeleton** (thinnest slice that makes the kernel journey pass — ugly fine, fake not), with a DEMO GATE every 2–3 chunks. DESIGN.md styles the screens UX.md defined; single-source rule (values only in the token table). Pre-built design system → adoption map + gap list instead of new tokens; reference pack → approved style-extraction pass first.

Then the **Consistency Gate**: machine pass (contradictions, placeholders, open decisions, unserved UX flow steps) is mandatory and blocking — findings fixed before Phase 4; human pass is advisory but read SPEC.md + UX.md at minimum (~20 min each).

### Phase 4 — `/brana-4-tasks`

**Triggers:** "split the plan", "create tasks", "phase 4"

TASKS.md per task: id, objective, dependencies, files, acceptance criteria (**observable behaviors** — "compiles"/"renders" are gates, never the criterion), difficulty, **interfaces block** (CONSUMES/PRODUCES — exact signatures quoted from ARCHITECTURE.md, so an isolated implementer never reads neighbor code), context pack (files + ARCHITECTURE sections; UI tasks name UX screen ids and get DESIGN.md). DEMO GATE entries preserved as explicit tasks with the human's walkthrough result as completion artifact (screenshots optional); skipped gates marked `GATE SKIPPED`, never deleted. Walking-skeleton tasks first, non-reorderable. Context packs are hints, not gospel.

### Phase 5 — `/brana-5-implement [task-id]`

**Triggers:** "implement task 0", "do the next task", "phase 5"

**One session per 2–3-task batch, cleared at each demo gate** (tune batch size in CONVENTIONS.md). Reading roams the repo; writing only touches task-listed files. UI tasks read DESIGN.md + their UX.md screen section and implement all states.

- **Done = demonstrated:** run the acceptance behavior in the real app. Per-task launch-and-look + screenshot is opt-in (user request or CONVENTIONS.md) — otherwise visual quality waits for the demo gate. Green tests alone never mark Done.
- **Demo gate = soft stop:** halt, print journey script, wait. "continue" skips → `GATE SKIPPED` logged.
- **Ambiguity:** internal → simplest interpretation + comment; would change/drop user-visible behavior → STOP and ask.
- **Scope cut = hard stop:** state the cut, end the turn. No default-proceed.
- Run the **verify script**, then commit per green task; the done-mark in TASKS.md carries the commit SHA + the path to the captured **evidence file** (`specs/NNN-name/evidence/task-N.txt` — the exercised command plus its last ~30 lines of output, captured live, not reconstructable from the diff afterward). Stuck twice → escalate to Opus-tier (may conclude PLAN.md itself is wrong).
- After compaction/flush: rebuild state from git log + TASKS.md marks, never from remembered conversation.

`delegate` mode: subagent per task (haiku boilerplate / sonnet rest); dispatch passes **file paths, never pasted content or re-narrated summaries**; report ≤15 lines with status `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` + SHA + evidence file path — verify it (it's unverified claims); two failures → take over directly.

### Phase 6 — `/brana-6-review`

**Triggers:** "code review", "demo gate", "product review", "walkthrough", "exit bar", "phase 6"

**6a code review** — different model than the implementer (Opus reviews Sonnet; cross-vendor via prompt mode when in chat UIs). Diffs only. Reviewer independence: diff + contracts only — never the implementer's report/rationale, never "do not flag X"; plan-vs-finding conflicts escalate to you. Reports bugs, security, races, contract/convention violations, and UI: design violations (raw values, missing states, contrast/focus) + UX violations (structure/flow diverging from UX.md). Findings → REVIEW_N.md → Phase 5 fixer session.

**6b product review (demo gate)** — you + the running app, zero tokens: launch, walk the scripted journey, check falsifiable criteria, judge against UX.md/DESIGN.md and your own eyes ("passes contracts but looks wrong" is valid — contracts are floors). Screenshots optional (→ `specs/NNN-name/screenshots/`) — they enable fix prompts and the optional vision pass. Findings become head-of-queue tasks; feature work does not resume past a failed gate.

**v1 exit bar:** kernel journey end-to-end in a release build, witnessed, including restart/offline/error paths; every `GATE SKIPPED` walked or explicitly accepted. "All tasks Done" is not the bar.

### Phase 7 — `/brana-7-change [request]`

**Triggers:** "add dark mode", "fix the login bug", "redesign", "impact analysis", "doc sync", "phase 7"

Agent **self-triages** A/B/C/R, announces route + one-line reason, proceeds; you override by replying.

| Route | Type | Path |
|---|---|---|
| **A — trivial** | Bugfix, copy, config | Short-lived branch (human may waive per instance) → hand-write one task → Phase 5 → verify (incl. journey suite) green before merge. |
| **B — small feature** | Fits architecture | Mini-spec → impact analysis → Phase 4 delta → 5/6 incl. 6b. Branch. |
| **C — big feature** | New module/schema/integration | Full Phase 1–6 on delta; ARCHITECTURE.md + UX.md patched, never regenerated. Branch. |
| **R — refactor** | Refactor, dependency upgrade, debt paydown; no user-visible behavior change intended | Feature branch → verify + journey suite green BEFORE, as baseline → chunked tasks (~300-line cap, one green commit each) → verify green after each chunk → 6a on the full diff (test adequacy matters most here) → doc sync (append Decision log entry if a boundary moved) → 6b only if UI touched → merge. |

Escalations: mid-flight boundary touch → re-enter as C; mid-flight behavior drop → hard stop for your decision (Route R also freezes on ANY user-visible change discovered mid-flight, not just a drop). Stale-interface-block rule: a mid-cycle CONSUMES/PRODUCES patch triggers a pass that updates every not-done task quoting the changed section, before the next implementation session. B/C get one 6a of the full feature diff + one 6b walkthrough before merge; Route R gets one 6a always and 6b only if UI was touched; Route A gets 6a only if it touches logic, auth, or data handling. Redesigns start from observed failures feeding a **UX.md patch first** — retokening without touching UX.md repaints the same wrong rooms. Impact analysis covers architecture fit + UX screens/flows + affected files + doc sections to patch.

**Doc sync (mandatory after every B/C/R merge):** ARCHITECTURE/UX/DESIGN vs the feature diff; amend every now-false statement directly — never a deviations appendix. If a module boundary moved, append a Decision log line to ARCHITECTURE.md. `FILE_STRUCTURE.md` is per-cycle, archived with its `specs/NNN-name/` dir, and is never compared here.

---

## Model Bindings (from WORKFLOW.md)

| Step | Default (Anthropic) | Fallback (chat UI) |
|---|---|---|
| P1 gap-check / interview | Haiku 4.5 / Sonnet 5 | Gemini Flash / Pro |
| P2 UX.md + PRD.md | Sonnet 5 | Gemini Pro |
| P2 ARCHITECTURE, P3 (all four docs), P7 impact analysis | Opus 4.8 | Gemini Pro |
| Consistency-gate machine pass, doc sync, code map | Haiku 4.5 | Gemini Flash |
| P4 task split, P5 implementation, 6a fixer | Sonnet 5 | Gemini Pro |
| P5 pure boilerplate | Haiku 4.5 | Gemini Flash |
| P5 escalation (failed twice) | Opus 4.8 | Gemini Pro |
| 6a reviewer | Opus 4.8 | Gemini Pro |
| 6b vision pass | Sonnet 5 | Gemini Pro |

6a rule: a different model than the implementer reviews; cross-vendor preferred when already in chat UIs.

---

## Sessions & Stops

**Fresh session per phase; per 2–3-task batch in Phase 5**, cleared at each demo gate (the natural flush point). Run mode is NOT automatic — `/clear` before each phase and at each gate. Never carry chat history across phases; carry only the output files.

Two stop types, deliberately different:

- **Soft stops (gates):** consistency-gate human read, every 6b demo gate. The agent halts and reminds you; "continue" skips, logged as visible debt (`GATE SKIPPED`), surfaced at the v1 exit bar.
- **Hard stops (scope cuts):** any mid-flight discovery that a spec'd, user-visible behavior won't be built. The agent states the cut and ends its turn — no "continue" default, in every medium. Verification is delegable; product decisions are not.

---

## Best Practices

1. **Read SPEC.md and UX.md yourself** (~20 min each) — they encode intent; wrong-but-consistent docs pass every machine check. Cheapest QA in the workflow.
2. **Walk the demo gates.** Skipping is allowed but logged; silent skipping is how "every task green, app unusable" happens.
3. **The kernel journey is the spine:** walking-skeleton target in Phase 5, standing gate script in 6b, exit bar for v1.
4. **Living docs are patched, never regenerated** — ARCHITECTURE.md, UX.md, CONVENTIONS.md, DESIGN.md. One source of truth per fact; no deviations ledgers. (`FILE_STRUCTURE.md` is per-cycle, not living — see File Locations below.)
5. **Context packs are hints** — verify against the real tree at Phase 5 time.
6. **Commit per green task**, branch per B/C feature, diffs from git.
7. **Doc sync after every B/C/R merge** — stale docs poison every future impact analysis.
8. **Screenshots are cheap context, not a requirement** — capturing is always the human's choice; when you have them, paste into review/fix prompts and archive gate shots under `specs/NNN-name/screenshots/`.
9. **Escalation is structured:** two failed attempts → Opus with task spec + code + failing output + attempt summary. The fix may be a PLAN.md edit.
10. **Scaling:** when Phase 4 context packs start guessing wrong (~200 files), feed the splitter a code map (one paragraph per module, cheap-model regenerated after each Route C).

---

## File Locations

```
repo/
  specs/
    001-core/         SPEC.md PRD.md PLAN.md TASKS.md FILE_STRUCTURE.md
                       evidence/ reviews/ screenshots/   (v1, Route C scale)
    002-reminders/     SPEC.md PLAN.md TASKS.md FILE_STRUCTURE.md
                       evidence/ reviews/                (Route C)
    003-dark-mode/     SPEC.md TASKS.md evidence/         (Route B mini-spec)
  ARCHITECTURE.md     (living, patched per change; ends in an append-only Decision log)
  UX.md               (living, patched per change)
  CONVENTIONS.md      (living, patched per change)
  DESIGN.md           (living, patched per change)
  src/  tests/  ...
```

`specs/` is append-only history; task ids numbered fresh per dir.

---

## Troubleshooting

| Issue | Root cause | Fix |
|---|---|---|
| Every task green, app unusable | Gates skipped, Done on green tests | Walk the skipped gates; re-verify Done = demonstrated. |
| Phase 5 keeps failing | Ambiguous task or wrong PLAN.md | Escalate to Opus with task + failing output; fix may be a PLAN.md edit. |
| Contradictions found mid-implementation | Consistency-gate machine pass skipped | Run it now; fix findings before more tasks. |
| Feature quietly shrank | Scope cut laundered into a comment/gotchas file | Hard-stop rule: cuts are your decision, restore or accept explicitly. |
| Docs drift after merges | Doc sync not run | Non-optional after every B/C/R merge. |
| UI incoherent across screens | UX.md missing or unread | UX.md is the floor plan; patch it, don't just retoken DESIGN.md. |
