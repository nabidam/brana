# Brana Skills — Usage Guide

Seven skills implementing Brana, the 6-phase app-dev workflow + Phase 7 change loop (WORKFLOW.md v1.9). Each skill has **run** mode (executes in Claude Code, Agent Adaptation Layer applies) and **prompt** mode (emits paste-ready blocks for external chat UIs — copy-paste is the workflow's canon medium).

The workflow's guard: every task green, every doc consistent-looking, app unusable. Countermeasures baked into the skills — the deliverable is the running app; Done = demonstrated (with live verification evidence); demo gate every 2–3 tasks; scope cuts are hard stops; consistency gate before tasks; task gate before implementation; per-cycle docs carry `status:` stamps (`draft` → `gate-passed`; TASKS.md `draft` → `ready` via the task gate) that downstream phases refuse to consume unstamped.

---

## Quick Start — The Golden Path

### Building a new app (v1):

```
1. /brana-1-spec               → SPEC.md (idea → kernel/v1/backlog + kernel journey)
2. /brana-2-prd-arch           → UX.md + PRD.md + ARCHITECTURE.md  (read UX.md yourself!)
3. /brana-3-plan               → PLAN.md (walking skeleton first, demo gates) +
                              CONVENTIONS.md + DESIGN.md + FILE_STRUCTURE.md
                              + consistency gate (machine pass blocks Phase 4)
4. /brana-4-tasks              → TASKS.md (context packs + demo-gate tasks)
                              + task gate (machine pass blocks Phase 5)
5. /brana-5-implement          → implement in 2–3-task batches; halt at each demo gate
6. /brana-6-review             → 6a code review (diffs) + 6b product walkthrough
7. v1 exit bar = the release-gate task: kernel journey passes in a release
   build through the production composition, witnessed by you; every
   GATE SKIPPED walked or explicitly accepted
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

Scope decomposition first (multi-subsystem ideas split into per-cycle sub-products), then gap-check (has draft) or interview (from nothing — ask the user's own thinking first; AskUserQuestion multiple-choice when options are enumerable). Multiple plausible directions → 2–3 approaches with trade-offs, options presented **before** the recommendation. Then the **required scope challenge**: core promise in one sentence, KERNEL (3–5 features), KERNEL JOURNEY (end-to-end story exercising every kernel feature — becomes the walking-skeleton target and the standing demo-gate script), ranked backlog. Convenience features are backlog by default. **Provenance check:** process-derived v1 bullets (verification tooling, output modules the workflow itself wants) are listed with task cost and need the user's explicit call. **Minimal-form rule:** user minimizing language ("just a flag") caps the deliverable at its minimal form; elaborations are priced options, never silent inclusions. Integration check before writing (combine answers, probe non-obvious consequences; uncertainty → explicit assumption). Design direction required (3 adjectives, reference apps, density, WCAG AA) — or name a pre-built design system / reference pack. After writing: spec self-review (placeholders, contradictions, scope, ambiguity) fixed inline before you read it.

Big ideas (multiple subsystems or > ~15–20 estimated tasks) decompose into **milestones** first — each its own `specs/NNN-name/` cycle ≤ ~15 tasks ending in a working, release-gated version; M1 (kernel milestone) is spec'd now, later milestones live as 2–3 coarse lines in `specs/ROADMAP.md`. Last step: **profile choice** — small project (single subsystem, ≤ ~15 tasks, no *novel* external integration — a well-known API via an established SDK qualifies with a compact wire contract, low stakes) → `profile: lite` in the frontmatter; any criterion fails → `profile: full` + `profile-reason: <criterion>` (bare `profile: full` is a `brana-gate docs` finding). ≤ ~5 tasks additionally folds the mid demo gate into the release gate. Phase 4's split re-checks the count: a full profile that comes out ≤ ~15 tasks is a `retro-lite candidate` warning from `brana-gate tasks --spec`, and Phases 2–4 apply the **Route S** deltas: PRD folds into SPEC, UX/ARCHITECTURE ship mini/lite, PLAN/FILE_STRUCTURE cut, DESIGN only if UI-heavy, gates authored directly in TASKS.md. Route C change cycles qualify against the *delta* (existing documented integrations don't disqualify). Verify script, evidence, gates, task gate, exit bar, and hard stops are kept in every profile; outgrowing lite mid-flight is a hard stop + upgrade. A user **speed signal** ("fast delivery", "no demo gates") makes the lite proposal mandatory-before-drafting and adds a **delivery contract** to the frontmatter (`delivery: demo_gates=waived ...`, closed vocabulary) — waivers substitute existing machinery, never new tooling, and TASKS.md may only echo the line verbatim.

**Output:** `specs/001-core/SPEC.md`, under 500 words plus the kernel section (lite: ~700 words incl. acceptance criteria).

### Phase 2 — `/brana-2-prd-arch`

**Triggers:** "UX", "screens", "wireframes", "write the PRD", "architecture", "phase 2"

Order matters: **UX → PRD → ARCHITECTURE**. UX.md (root, living doc) is the floor plan: screen inventory with ids, navigation map, per-screen text wireframes with empty/loading/error states, key flows, density notes. Screens are interactive UI only — CLI/log/terminal surfaces get a one-block **operator surface note** (name, invocation, output format, error/exit convention), no wireframes, and their tasks never load DESIGN.md. PRD acceptance criteria must be falsifiable (observable behavior, never adjectives or "tests pass"). ARCHITECTURE.md commits to one stack, carries a **dependency plan** (buy is the default: capability → package @ registry-verified latest-stable/LTS version → what it replaces; hand-rolls justified; **the user approves the package list**; unlisted imports are a Phase 5 hard stop and a 6a finding), maps component hierarchy to UX screen ids, and obeys the traceability rule: every kernel-journey step names its serving API call/event; an external system in the kernel journey or a v1 flow (anything that will be faked) gets a versioned **wire contract** (exact request/response shapes, auth, error semantics); auth/user-data/external-input apps get a **threat model** section (trust boundaries, authN/Z per surface, input validation, secrets handling); a decision unresolvable by reasoning gets a `SPIKE:` marker (question, candidates, leading candidate, deciding measurement) instead of an open "X or Y". PRD NFRs each carry a budget + measurement command. Then the **architecture review** (blocks Phase 3): an independent model — 6a independence rules, cross-vendor preferred — reviews the design itself (failure handling, data-model flaws, races, 10× scale, over-engineering, simplest-credible-alternative per major decision, threat-model gaps); you arbitrate the findings and ARCHITECTURE.md is patched before Phase 3.

**Read UX.md and walk the flows yourself before Phase 3** — intent is the one thing no machine check verifies.

### Phase 3 — `/brana-3-plan`

**Triggers:** "implementation plan", "conventions", "design system", "consistency gate", "phase 3"

Opus-tier leverage point. PLAN.md's first milestone is the **walking skeleton** (thinnest slice that makes the kernel journey pass — ugly fine, fake not), with a DEMO GATE every 2–3 chunks; every gate launch command is the production entry point with disposable inputs (same-composition rule), and the last entry is the **RELEASE GATE** — the kernel journey in a release build, each step served through the production composition. DESIGN.md styles the screens UX.md defined; single-source rule (values only in the token table). Pre-built design system → adoption map + gap list instead of new tokens; reference pack → approved style-extraction pass first.

Then the **Consistency Gate**: machine pass is mandatory and blocking — script-first via `brana-gate docs` (placeholders; contrast ratios computed, never LLM-estimated), then the LLM judgment pass (contradictions, open decisions, unserved UX flow steps, unserved gate journey steps, bespoke gate compositions, missing wire contracts / RELEASE GATE, SPIKE markers without a head-of-plan spike chunk, NFRs with no serving mechanism) — findings fixed before Phase 4; human pass is advisory but read SPEC.md + UX.md at minimum (~20 min each).

### Phase 4 — `/brana-4-tasks`

**Triggers:** "split the plan", "create tasks", "phase 4"

TASKS.md per task: id, objective, dependencies, files, acceptance criteria (**observable behaviors** — "compiles"/"renders" are gates, never the criterion), difficulty, **interfaces block** (CONSUMES/PRODUCES — exact signatures quoted from ARCHITECTURE.md, so an isolated implementer never reads neighbor code), context pack (files + ARCHITECTURE sections; UI tasks name UX screen ids and get DESIGN.md). DEMO GATE entries preserved as explicit tasks with the human's walkthrough result as completion artifact (screenshots optional); the RELEASE GATE becomes a gate task too; skipped gates marked `GATE SKIPPED`, never deleted. Verified-fake rule when wire contracts exist: fake and real adapter share one contract suite; live calls only in a bounded canary through the production composition. Walking-skeleton tasks first, non-reorderable. **Merge bias:** emit the fewest tasks respecting the 50–300-line cap — consecutive linear-dependency tasks sharing a primary file merge; a catch-all "fill remaining gaps" task is a blocking finding. **Ceremony scales with risk:** boundary tasks (cross-module CONSUMES/PRODUCES, wire contracts, Task 0, gates, crystallization) carry the full interfaces block + context pack; interior tasks carry only objective/files/deps/criteria. **Downgrade valve:** a full profile whose split comes out ≤ ~15 tasks (one subsystem, no novel integration) stops and offers retro-lite — `brana-gate tasks --spec` warns `retro-lite candidate`. Context packs are hints, not gospel. In agent mode each task is a heading + fenced TOML block (schema in `brana-gate --help`) so the gate's structural half runs as a program. TASKS.md is written `status: draft`; the **task gate** (blocks Phase 5) cross-references TASKS.md against PLAN.md and ARCHITECTURE.md — chunk coverage, dependency cycles, journey steps with no earlier serving task, unmatched CONSUMES quotes, missing tags/`[contract]` criteria, incomplete preflight blocks, missing RELEASE GATE / production-composition proof, catch-all tasks, ad-hoc waiver frontmatter (vs. SPEC.md's delivery contract, `--spec`) — script-first via `brana-gate tasks`, then a Haiku-tier judgment pass — and flips the stamp to `ready` only when clean. A skipped gate still gets its journey crystallized immediately (test marked `UNWITNESSED` until walked) — a skip costs attention debt, never automation debt.

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

**6a code review** — different model than the implementer (Opus reviews Sonnet; cross-vendor via prompt mode when in chat UIs). Diffs only. Precondition: lint and typecheck must be green before the review starts — a finding a linter could catch is a lint-config gap, not a review finding. Reviewer independence: diff + contracts + the reviewed tasks' acceptance criteria from TASKS.md only — never the implementer's report/rationale, never "do not flag X"; plan-vs-finding conflicts escalate to you. Reports bugs, security (against the threat model when it exists), races, contract/convention violations, UI: design violations (raw values, missing states, contrast/focus) + UX violations (structure/flow diverging from UX.md), category 7 — test adequacy (missing test at the declared layer, an assertion-free test, a test that mocks away the behavior under review), and category 8 — composition and fake integrity (bespoke wiring where the production entry point belongs; a fake diverging from its wire contract). Findings are unverified claims: a confirmation pass (fixer-tier) reproduces each bug/race (failing test or concrete repro) and quotes both sides of each contract violation before any fix task is written; unconfirmable findings escalate to you. Confirmed findings → `specs/NNN-name/reviews/REVIEW_N.md` → Phase 5 fixer session; repro tests join the suite.

**6b product review (demo gate)** — you + the running app, zero tokens: launch, walk the scripted journey, check falsifiable criteria, judge against UX.md/DESIGN.md and your own eyes ("passes contracts but looks wrong" is valid — contracts are floors). Screenshots optional (→ `specs/NNN-name/screenshots/`) — they enable fix prompts and the optional vision pass. Findings become head-of-queue tasks; feature work does not resume past a failed gate.

**v1 exit bar:** the release-gate task, preflighted like any gate (preflight includes a `brana-gate tasks` re-run — done-mark integrity: SHA + existing non-empty evidence file per Done mark, deps resolved in order) — kernel journey end-to-end in a release build through the production composition, witnessed, including restart/offline/error paths; production-composition proof + verified-fake suites green when fakes stood in; every PRD NFR budget measured at or under budget (or explicitly accepted over); every `GATE SKIPPED` listed with its `UNWITNESSED` journey test, walked now or explicitly accepted; unresolved `GATE BLOCKED` fails the bar. "All tasks Done" is not the bar. Blocked-gate fixes that reveal a missing subsystem spawn a child spec cycle (Spawn route), never a wedge into the current TASKS.md.

### Phase 7 — `/brana-7-change [request]`

**Triggers:** "add dark mode", "fix the login bug", "redesign", "impact analysis", "doc sync", "phase 7"

Agent **self-triages** A/B/C/R, announces route + one-line reason, proceeds; you override by replying.

| Route | Type | Path |
|---|---|---|
| **A — trivial** | Bugfix, copy, config | Short-lived branch (human may waive per instance) → hand-write one task → Phase 5 → verify (incl. journey suite) green before merge. |
| **B — small feature** | Fits architecture | Mini-spec → impact analysis → Phase 4 delta → 5/6 incl. 6b. Branch. |
| **C — big feature** | New module/schema/integration | Full Phase 1–6 on delta; ARCHITECTURE.md + UX.md patched, never regenerated. Branch. |
| **R — refactor** | Refactor, dependency upgrade, debt paydown; no user-visible behavior change intended | Feature branch → verify + journey suite green BEFORE, as baseline → chunked tasks (~300-line cap, one green commit each) → verify green after each chunk → 6a on the full diff (test adequacy matters most here) → doc sync (append Decision log entry if a boundary moved) → 6b only if UI touched → merge. |

Escalations: mid-flight boundary touch → re-enter as C; mid-flight behavior drop → hard stop for your decision (Route R also freezes on ANY user-visible change discovered mid-flight, not just a drop). Stale-interface-block rule: a mid-cycle CONSUMES/PRODUCES patch triggers a pass that updates every not-done task quoting the changed section, before the next implementation session. Stale-plan rule: a mid-cycle PLAN.md section rewrite reverts PLAN.md + TASKS.md to `draft` until a scoped re-gate (consistency checks on the patched section, `brana-gate tasks` on its tasks) is clean. B/C get one 6a of the full feature diff + one 6b walkthrough before merge; Route R gets one 6a always and 6b only if UI was touched; Route A gets 6a only if it touches logic, auth, or data handling. Redesigns start from observed failures feeding a **UX.md patch first** — retokening without touching UX.md repaints the same wrong rooms. Impact analysis covers architecture fit + UX screens/flows + affected files + doc sections to patch.

**Doc sync (mandatory after every B/C/R merge):** ARCHITECTURE/UX/DESIGN vs the feature diff; amend every now-false statement directly — never a deviations appendix. If a module boundary moved, append a Decision log line to ARCHITECTURE.md. Close the sync with `brana-gate claims` over the living docs — every cited path must exist in the working tree. `FILE_STRUCTURE.md` is per-cycle, archived with its `specs/NNN-name/` dir, and is never compared here.

---

## Model Bindings (from WORKFLOW.md)

| Step | Default (Anthropic) | Fallback (chat UI) |
|---|---|---|
| P1 gap-check / interview | Haiku 4.5 / Sonnet 5 | Gemini Flash / Pro |
| P2 UX.md + PRD.md | Sonnet 5 | Gemini Pro |
| P2 architecture review | Opus 4.8 (fresh session) | GPT/Gemini (cross-vendor preferred) |
| P2 ARCHITECTURE, P3 (all four docs), P7 impact analysis | Opus 4.8 | Gemini Pro |
| Consistency-gate + task-gate judgment passes (structural half is `brana-gate`, zero tokens), doc sync, code map | Haiku 4.5 | Gemini Flash |
| 6a finding confirmation | Sonnet 5 | Gemini Pro |
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
