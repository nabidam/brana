# Brana v2 — App Development Workflow

v2 is a token-efficiency redesign. Two independent audits of v1.12 (see
`docs/2026-07-30-brana-workflow-audit.md` and `ANALYSIS-brana-vs-superpowers.md`)
found the same root causes: nine planning artifacts re-expressing the same facts,
duplicated instructions, a gate stack whose crystallization machinery dominated
execution cost, and mandated session flushes that defeated prompt caching.
v2 keeps what found real bugs — the kernel journey, scope-cut hard stops,
production-composition verification, the human walkthrough — and deletes the
apparatus that existed only to police drift between documents v1 itself created.

Maintenance rules for this doc:
1. Every line must change agent behavior; if deleting it would not change the
   output, delete it.
2. **Removal policy:** every new rule must state the failure it prevents, what
   activates it, and what would justify removing it. A rule that hasn't fired
   in three consecutive cycles is a removal candidate. Additions without this
   are rejected — v1 grew monotonically for twelve versions; v2 must not.
3. Cost claims about this workflow are made only from measured runs
   (see Measurement).

## Principles

1. **The deliverable is the running app, not the documents.** Any conflict
   between "the doc says done" and "the app doesn't do it" resolves in favor
   of the app.
2. **Done = demonstrated.** A unit is done when its behavior is exercised in
   the running app or by a test that actually drives it — not when the code
   passes tests it wrote for itself.
3. **One source of truth per fact.** A contract, value, or requirement lives in
   exactly one place; everything else references it by ID or path. This applies
   to the workflow itself: skills route to this document, never restate it.
4. **Scope cuts escalate, never archive.** Discovering mid-flight that a
   spec'd, user-visible behavior won't be built is a hard stop for the user's
   decision. Documenting a cut in a side file is laundering, not a decision.
   This is the workflow's one unconditional stop.
5. **Depth beats breadth.** v1 of an app is the smallest feature set that
   delivers the core promise, built well.
6. **Buy before build.** An established package beats hand-rolling unless the
   capability is trivial (< ~30 lines) or core domain logic.
7. **Assurance follows evidence.** Reviews are richest against concrete diffs
   and running behavior. Plan for product truth and irreversible decisions;
   decide low-level structure at implementation time.
8. **Ceremony activates by risk, never by default.** Controls load through
   risk modules (below); a project pays only for the risks it has.

## Artifacts

**One canonical plan per cycle: `specs/NNN-name/PLAN.md`.** It is enriched in
place and is the single authority for scope, requirements, contracts, units,
and verification. No separate SPEC/UX/PRD/TASKS/FILE_STRUCTURE documents exist.

PLAN.md structure (top-loaded so a heading scan answers most questions):

1. **Goal & kernel journey** — the product's core promise in one sentence, then
   the kernel journey: one end-to-end user story, numbered steps (KJ1, KJ2, …),
   exercising every kernel feature ("create an item → close app → reopen →
   item still there").
2. **Scope** — in / out / backlog. Convenience features (scheduling, theming,
   localization, power-user overrides) are backlog by default.
3. **Requirements** — stable IDs (R1, R2, …), each with a falsifiable
   acceptance example: observable behavior, never adjectives, never process
   facts ("tests pass"). An NFR carries a budget and the command that measures
   it, or it doesn't exist.
4. **Active risk modules** and their sections (see Risk Modules).
5. **Stack & dependencies** — one committed stack, no open "X or Y".
   Dependency list per the tiers below.
6. **Units** — U1, U2, … (see Units).
7. **Verification contract** — the verify command, the kernel e2e test path,
   and the definition of done.
8. **Walkthrough script** — the final-gate script: kernel journey steps plus
   the edge behaviors (restart, offline, invalid input) drawn from the
   requirements.

Progress, status, and evidence never live in PLAN.md — they live in the ledger
(see Execution). The plan describes intended and current work; it does not grow
with completion marks.

**Size budget (soft):** a PLAN.md drifting past ~2,500 words is a warning to
compress — decision density beats volume, and an unbounded single artifact
just recreates the v1 archive problem in one file. Not a gate; a signal.

**Living root docs (conditional, compact):**

- `CONVENTIONS.md` — ≤1 page: naming, error style, test strategy, commit
  style, the verify command. A convention a machine can check becomes a lint
  rule instead of prose.
- `ARCHITECTURE.md` — only when the system outgrows PLAN.md's stack section
  (multiple cycles, real module boundaries). Current truth only, compact;
  decisions with history go to `docs/adr/NNN-title.md`, loaded on demand.
  Never append cancelled work or per-cycle narrative here.
- `DESIGN.md` — only when the UI-heavy risk module is active.

`specs/` is append-only history; living root docs are patched, never
regenerated, never contradicted by a side ledger.

## Risk Modules

Risk is multidimensional; a binary full/lite profile bundles unrelated
controls. Instead, at planning time the agent proposes the modules the project
actually triggers, the user confirms, and PLAN.md lists them. Each module adds
its section to PLAN.md and its checks to review — nothing else does.

| Module | Trigger | Adds |
|---|---|---|
| **Money** | payments, balances, credits | integer money math, idempotency + concurrency requirements, reconciliation check, immediate independent review of money diffs |
| **External system** | a runtime third-party boundary — API, provider, service, webhook — regardless of how it will be tested | wire contract in PLAN.md (exact shapes, auth, error semantics) + failure behavior; immediate review of integration diffs. **When a fake stands in for it** (the usual case): verified fake — one shared contract suite runs against fake and real adapter; real side offline-assertable; live calls canary-only |
| **Migration** | schema change against existing data | up→down→up rehearsal against fixture data, data-survival assertion; rollback = down migration, never `git revert` |
| **UI-heavy** | the product's value is its interface | UX flows per screen (regions, states: empty/loading/error/focus) in PLAN.md §4; DESIGN.md with semantic tokens and a contrast table in the shape `brana-gate docs` parses (token rows `\| name \| #RRGGBB \|`; checked rows under a header naming fg/bg or contrast); self-review runs `brana-gate docs PLAN.md DESIGN.md`; a11y check in verify |
| **Auth / user data** | authentication or authorization, stored personal/sensitive data, or an identified hostile-input boundary (untrusted uploads, public write endpoints) — *not* ordinary input handling, which the base verification contract already covers | threat model section: trust boundaries, authZ per surface, validation at the hostile boundary, secrets handling; security review on auth diffs |
| **Operator surface** | CLI/daemon/pipeline as a primary interface | one operator note per surface: invocation, output format, exit convention (never screens/wireframes) |
| **Deployment** | the app ships as a composed service (containers, workers) | production-composition smoke: the real entry point boots with disposable config; gate launches always use the production entry point with fakes injected at seams — a bespoke gate-only assembly is a blocking finding |

No module triggered → the plan is Goal + Scope + Requirements + Stack + Units
+ Verification + Walkthrough, and nothing else.

## Units

A unit is one implementable outcome, sized by behavior and interface boundary —
not by line count (a line estimate may appear as a warning signal only).

Each unit: `id`, outcome (one observable behavior), deps (unit ids), proposed
files (a hint, not a contract — the repo tree is the authority), acceptance
criteria (falsifiable, referencing R-IDs), and — **only when its surface
crosses a module boundary or a wire contract** — an interfaces block quoting
the exact signatures it consumes/produces. Interior units carry outcome, deps,
files, criteria, nothing more. A contract is stated once, in the unit that
produces it (or the risk-module section); consumers reference the producing
unit's ID.

U1 is always the **walking skeleton**: the thinnest end-to-end slice that makes
the kernel journey pass in the real app — ugly is fine, fake is not. Everything
else deepens it. U0, when needed, is scaffold only (tree, configs, deps
installed frozen/locked, verify script wired, boot smoke documented in
CONVENTIONS.md).

## Flow

Six steps. One persistent controller session runs the whole cycle; subagents
provide isolation. Never flush the controller session as a ritual — context is
cached; flushing re-buys it cold.

### 1. Discover

Cheap model or the controller. Interview until requirements are clear — ask
what the user is already considering before offering ideas; challenge vague
requirements; suggest simpler alternatives. Then the **scope challenge**:
state the core promise in one sentence, identify the kernel (3–5 features
without which the product is pointless), write the kernel journey, push
everything else to backlog. A feature that undermines the promise if built
shallowly is kernel or cut, never "shallow v1".

- **Minimal-form rule (hard):** "just a flag" / "a simple X" commits to the
  minimal form. Elaborations are named backlog options with cost; they enter
  scope only by the user's explicit call.
- **Provenance:** every scope bullet traces to user-stated, kernel-derived, or
  process-derived; process-derived work is billed to the user by name, never
  smuggled in.
- Ideas spanning multiple subsystems or beyond ~15 units split into milestones
  first — each milestone its own cycle ending in a working app; later
  milestones get 2–3 lines in `specs/ROADMAP.md`, detailed only when their
  cycle starts.

### 2. Plan

Strong model, one session. Write PLAN.md per the structure above. Then the
**plan self-review**, inline, same session — this replaces v1's consistency
gate and task gate entirely:

1. Coverage: every requirement maps to a unit; every kernel-journey step has a
   serving unit; every acceptance example is falsifiable.
2. Placeholders: no `to-be-decided` markers, no "handle appropriately",
   no open "X or Y" (the gate script scans for the literal tokens).
3. Consistency: names, signatures, and shapes used by later units match where
   they were defined; every risk-module obligation has its section.
4. Deterministic remainder: run `tools/brana-gate docs PLAN.md` — plus
   `DESIGN.md` as a second argument whenever it exists (`tools/brana-gate
   docs PLAN.md DESIGN.md`): the contrast computation only runs on files it
   is actually passed, and only on DESIGN-named files.

Fix inline. Independent architecture review (fresh subagent, findings-only,
never the author's rationale) is triggered **only** by the money, external
system, migration, or auth modules — otherwise skipped.

The human reads PLAN.md §§1–3 at minimum: intent is the one thing no check can
verify, and ~15 minutes here is the cheapest QA in the workflow.

A genuinely unresolvable decision becomes `SPIKE: <question>` with a leading
candidate and the measurement that decides — a time-boxed spike unit at the
head of the unit list, never an open alternative.

### 3. Execute

Controller session persists; one subagent per unit (or small batch with
disjoint files). Git: never implement on main uninvited — create the cycle
branch first; commit per unit.

**Subagent packet — paths, not prose:** the unit's PLAN.md heading, the
interfaces it consumes (by producing-unit reference), CONVENTIONS.md path,
and — per active module — the relevant PLAN.md section paths. The subagent
reads files itself; nothing is pasted or re-narrated; it never reads the whole
plan. Writing touches only the unit's files (adjusted to the real tree);
reading roams freely.

**Subagent report:** ≤15 lines; `DONE | BLOCKED | NEEDS_CONTEXT`; commit SHA;
the verify output tail. The report is unverified until the controller sees
verify green.

Rules that stop a subagent (routed to the user, never guessed past):

- **Ambiguity:** internal (naming, private structure) → simplest
  interpretation, noted. Would change or drop user-visible behavior → stop.
- **Scope cut** → hard stop (Principle 4).
- **Dependency:** a needed *strategic-tier* capability outside the plan's
  approved list (§Dependencies) → propose, ask. Routine-tier picks never
  stop — the implementer selects and reports them.

**Verification while executing:** every unit ends with the verify command
green (build + lint + typecheck + suite; module additions like a11y or audit
ride in it). When U1 (walking skeleton) lands, write the **kernel e2e test**
once — the kernel journey on the stack's e2e harness — and add it to verify.
That is the entire crystallization concept: one test, written once, run on
every unit. Further e2e appears only when a module demands it or the final
walkthrough finds a bug (test what broke).

**Ledger, not bookkeeping:** progress lives in `.brana/ledger.md` —
one line per unit: id, status, date. The unit's commit subject carries its
U-ID (e.g. `feat: stream endpoint [U3]`), so `git log --grep` is the
authority for which commit completed which unit — the ledger never records
SHAs (a commit cannot contain its own hash). Ledger updates are never
committed into PLAN.md and never generate their own commits; the ledger line
rides along in the unit's commit. After compaction, state rebuilds from
git log + ledger, never from remembered conversation.

**Mid-cycle plan changes:** patch PLAN.md in place, re-run the self-review on
the patched section only, and update the interfaces of not-yet-done units that
quoted a changed contract. No stamp machinery — the diff is the record.

### 4. Review

Independent reviewer (fresh subagent, different model when available; gets
diff + contracts, never the implementer's rationale), **scoped by risk**:

- **Immediate, per diff:** money, auth, concurrency, migrations, external
  integrations, security boundaries, production composition.
- **Batched, once before release:** everything else, as one review of the
  branch diff.

Findings only: file:line, severity, one-line fix. A bug claim needs a repro
(failing test or concrete steps) before it becomes a fix unit; a finding that
fails reproduction goes to the human, never silently dropped or blindly fixed.
The repro test joins the suite. Same specific rule confirmed twice → its fix
also adds a lint rule or CONVENTIONS.md line so the class never needs a
reviewer again.

### 5. Release — the walkthrough closes the spec

The one mandatory human gate. Preflight first (agent): verify green, release
build, launch via the production entry point (deployment module: production
composition with disposable config), walkthrough entry reachable. Preflight
failure = fix units first; the user is only ever invited to walk an app that
provably runs.

Then the user walks PLAN.md §8: the kernel journey plus edge behaviors, on the
release build. Findings become fix units at the head of the queue; re-walk
after they land. NFR budgets are measured by their named commands here. The
cycle closes when the walkthrough passes — then the branch merges and the
spec dir is history.

**Pull gates (optional, zero ceremony):** at any time the user can say "show
me" — the agent launches the app and prints the current journey script. On
long cycles the agent posts a screenshot when a vertical slice lands; the user
glances async and replies only if something looks wrong. No scheduled mid
gates, no gate state machine, no per-gate coverage obligations.

### 6. Change (post-v1)

Two routes:

- **Fix** — bugfix, copy, config: branch → one unit → verify green (kernel e2e
  included) → merge. Review only if it touches a risk-module area.
- **Cycle** — anything user-visible or structural: new `specs/NNN-name/PLAN.md`
  scoped to the delta (Discover → … → Release on the delta; risk modules
  re-evaluated for the delta). Living docs are patched, never regenerated.

After any merged change: correct every statement in the living docs the diff
made false (amend the statement — never a "deviations" appendix), run
`tools/brana-gate claims` on them (every cited path must exist), and record
non-obvious decisions as one ADR line. Mechanical, cheap, non-optional.

A change that mid-flight turns out to cross a module boundary, schema, or wire
contract stops and re-enters as a cycle. A refactor that changes user-visible
behavior isn't a refactor — same stop.

## Dependencies

Two tiers:

- **Routine** — policy-compliant packages in the repo's existing stack:
  the implementer picks them, installs via the lockfile, reports in the unit
  report. The verify script's audit + secret scan covers them.
- **Strategic** — new frameworks, paid services, native/binary deps, unusual
  licenses, anything auth/money-adjacent: named in PLAN.md §5 with one line of
  why, approved by the user before implementation.

Versions come from the lockfile/resolver, never from memory; a resolver
conflict on a strategic pick goes back to the user, not into ad-hoc upgrades.

## Model & Session Economics

- One persistent controller session per cycle; subagents for isolation.
  Flushing the controller is allowed only when the context is genuinely
  poisoned, never as cadence.
- Strong model plans and reviews risk modules; mid-tier implements; cheap tier
  does boilerplate and doc sync. Two failed attempts on a unit → the
  controller takes it over directly.
- Delegation passes paths, not prose. Bulk output goes to files; paths return.
- No conversational filler in generated documents.

## Measurement

Cost claims require data. Per cycle, record in the ledger footer: planning
words generated, units, fix units, agent invocations, (when available)
billed tokens, **the risk modules that were active, and every hard stop or
exceptional rule that actually fired** (one line each) — absence is derived
for the named conditional controls, which is what makes the removal policy
auditable. Compare across cycles before tightening or loosening any rule.
Every proposed workflow change states: failure prevented, activation
condition, expected cost, removal condition. `COMPARISON.md`-style claims
("cheapest per feature") are banned unless backed by these numbers.
