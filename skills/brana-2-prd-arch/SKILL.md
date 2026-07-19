---
name: brana-2-prd-arch
description: "Use when a finalized SPEC.md exists and the user wants UX design, screens, wireframes, a PRD, product requirements document, system design, architecture, API contract, or database schema, mentions modules or components after a spec exists, or says next phase or phase 2."
---

# Phase 2 — UX.md + PRD.md + ARCHITECTURE.md

Three documents, in this order: UX → PRD → ARCHITECTURE (screens inform requirements; both inform architecture), then an independent architecture review before Phase 3. UX.md is the missing artifact most workflows skip — without it, implementers get tokens and adjectives but no screens, every task improvises its own interface, and the result is incoherent. ARCHITECTURE.md becomes the single "current truth" every future impact analysis reads.

## Modes

- **run** (default): execute below. The workflow wants a fresh session per document; if the user runs all three here, finish each fully before starting the next.
- **prompt** (argument contains `prompt`): output the paste-ready prompt block(s) from the templates below with actual file contents embedded. No other output. UX + PRD target Sonnet/Pro tier; architecture targets Opus-tier — say which block goes where.

## Run mode

Locate the current cycle's SPEC.md (latest `specs/NNN-name/SPEC.md`). **`profile: lite` in its frontmatter → Route S deltas apply:** skip Step 2 entirely (criteria live in SPEC.md); Step 1 produces the mini UX.md (screen list with ids, kernel flow step-by-step, one line per screen on empty/error states); Step 3 produces the lite ARCHITECTURE.md (stack commitment, dependency plan — same rules, same user approval, data model, API/contract surface — a well-known external integration gets its compact wire contract here (≤1 page: endpoints, shapes, error semantics; verified-fake rule stands), kernel-journey traceability, Decision log — no module ceremony; threat model still applies if its trigger does, which should instead fail the lite qualification — flag it); Step 4 becomes advisory — offer it once, and a skip is recorded in SPEC.md as an accepted-risk line.

**Step 1 — UX.md** (from SPEC.md). Act as a senior product designer. Produce:

1. Screen inventory: every screen/view/modal, each with an id (S1, S2…), purpose, entry points.
2. Navigation map (text diagram).
3. Per screen: a text wireframe — regions top-to-bottom/start-to-end, content per region, primary action, where the eye goes first. Include empty, loading, and error states.
4. Key flows: the kernel journey plus the 2–3 next-most-common journeys, step by step as "user sees X, does Y, system responds Z" — with exact screen ids.
5. Density & hierarchy notes per screen: what is one click away, what is deliberately buried behind disclosure.

**Screens are interactive UI only (hard rule).** A CLI command, log stream, or operator terminal output is never a screen: no S-id, no wireframe, no empty/loading/error-state ceremony, no navigation entry. Such surfaces get an **operator surface note** in a separate "Operator surfaces" UX.md section — per surface: name, invocation, output format in 1–2 lines, error/exit convention. Downstream, tasks touching only an operator surface reference the note and do **not** load DESIGN.md (terminal style rules live in CONVENTIONS.md, ≤5 lines). Wireframing `--help` output is the tell this rule was skipped.

No visual styling, no colors, no code. If SPEC names a reference pack, adapt its _patterns_ (navigation structure, disclosure, information density) — never clone layouts. Write to repo root — living doc, patched forever after.

**Tell the user to read UX.md and walk the flows before proceeding** — UX.md encodes intent no machine check can verify; a step that feels wrong on paper will be wrong in the app, and this is the cheapest moment to fix it.

**Step 2 — PRD.md** (from SPEC.md + UX.md). Include: functional requirements, non-functional requirements, user stories, acceptance criteria, validation rules, error cases, edge cases (offline, empty states), constraints, out-of-scope, future improvements. Acceptance criteria must be FALSIFIABLE: observable behavior a human can verify in the running app ("restart the app; saved items are listed"), never adjectives ("clean") and never process facts ("tests pass"). Every non-functional requirement carries a **budget and a measurement** — the observable number plus the command or procedure that produces it ("cold start under 2s, measured by X"); an NFR without a measurement is a placeholder. The consistency gate (Phase 3) flags any NFR with no serving mechanism, and the release gate measures every budget. Preserve the Kernel/v1/Backlog split — do not promote backlog items. Do not discuss implementation. Write to the same `specs/NNN-name/` dir with frontmatter `status: draft` (UX.md and ARCHITECTURE.md are living docs — no stamps).

**Step 3 — ARCHITECTURE.md** (from PRD.md + UX.md). Act as a principal software architect. Include: system overview, module responsibilities and boundaries, data model / DB schema (DDL with indices and constraints), API contract (endpoints, request/response shapes, status codes, errors, auth), component hierarchy mapped to UX.md screen ids, dependency graph, error handling strategy, configuration strategy. Rules:

- COMMIT to one concrete stack and one design per decision — no "e.g. X or Y", no alternatives left open.
- **Dependency plan (required section; buy is the default):** for every capability an established package serves, one line — `capability → package @ exact version → what it replaces` — with versions the **latest stable/LTS at writing time, verified against the package registry, never recalled from memory**. A hand-rolled capability names its reason: no credible package, trivial (< ~30 lines), or core domain logic (the thing the product *is*). Sprawl guard: a package must serve a *named* capability — no speculative utilities, no left-pad dependencies; selection bar per pick: actively maintained, license compatible, transitive tree proportionate to the need (non-obvious picks get a Decision-log line). **User approval (hard rule):** present the package list — one line each on what it does and why this one (AskUserQuestion for contested picks) — before finalizing ARCHITECTURE.md. No package enters the plan unapproved; no package enters the code that isn't in the plan (Phase 5 hard stop). Task 0 installs at pinned versions; 6a flags violations both directions.
- **Name the test harness per layer, including the e2e/journey harness** — the walking skeleton needs it and CONVENTIONS.md's Test strategy (Phase 3) and every gate's crystallization task (Phase 4) build on this name.
- **Traceability (load-bearing):** every UX.md flow must be traceable through the contract — for each kernel-journey step, name the API call or event that serves it; a step with no serving contract (e.g. "reopen app → data restored" needs a list/read endpoint) means add the contract. Implementers build only what the contract names.
- **Wire contracts (conditional):** when the kernel journey or a v1 flow depends on an external system (a paid API, third-party service — anything that will be faked in tests), that integration gets a versioned **wire contract** section: exact request/response shapes, auth, error semantics — precise enough that a fake can be validated against it. Traceability extends to those steps: each names its wire contract. No external system → omit. Without this, the fake's convenience shape becomes the de-facto contract and the first real request is built at release time.
- **Threat model (conditional):** when the app has auth, stores user data, or accepts external input, include a **threat model** section: trust boundaries (who can send what to which surface), authN/authZ model per surface, input-validation strategy at each boundary, secrets handling (where keys live, what is never logged). No such surface → omit. 6a's security category reviews against this section, not against vibes.
- **Spike markers:** a decision genuinely unresolvable by reasoning (novel integration, unproven performance) is not left open as "X or Y": mark it `SPIKE: <question>` with the candidate answers, the leading candidate (design against it), and the measurement that decides. Phase 3 turns each marker into a time-boxed spike chunk at the head of PLAN.md.

- **Forward constraints (only when `specs/ROADMAP.md` exists):** one line per future milestone naming what this design must not preclude — and nothing more; future milestones are never designed here.

Include an empty **Decision log** section at the end of the file — append-only, one line per future decision as `YYYY-MM-DD — decision — why`; Phase 7 doc sync and Route C patches append to it, never delete an earlier entry's why.

No implementation code. Write to repo root — living doc, patched forever after.

**Step 4 — Architecture review (blocks Phase 3).** The consistency gate checks that docs agree; nothing else checks the design is any good — wrong-but-consistent architecture passes every machine pass. One independent review, findings-only, 6a independence rules: the reviewer gets ARCHITECTURE.md + PRD.md + UX.md, never the author's rationale; fresh session, different model than the author where possible (cross-vendor via prompt mode preferred; a same-vendor fresh session is weaker independence, still better than none). Categories: (1) module/flow with no failure handling, (2) data-model flaws (missing constraint/index/key for a named flow), (3) concurrency/ordering hazards, (4) first thing that breaks at 10× data when a requirement implies growth, (5) over-engineering — a module serving no PRD requirement, (6) per major decision, the simplest credible alternative and why the chosen design beats it (no credible answer is a finding), (7) threat-model gaps when the section exists, (8) build-vs-buy — a designed module duplicating an established, maintained package (name the package), and any dependency-plan entry failing the selection bar. **The user arbitrates the findings** — accepting one is a product decision, not a mechanical fix; patch ARCHITECTURE.md before Phase 3 starts.

Do not proceed to planning — that is Phase 3, a fresh session.

## Prompt mode templates

UX (Sonnet / Gemini Pro, fresh session):

```
You are a senior product designer. From the SPEC below, produce UX.md:
1. Screen inventory: every screen/view/modal, each with an id (S1, S2…),
   purpose, and entry points.
2. Navigation map: how the user moves between screens (text diagram).
3. Per screen: a text wireframe — regions top-to-bottom/start-to-end,
   what content each region holds, what the primary action is, and where
   the eye goes first. Include empty, loading, and error states.
4. Key flows: the kernel journey plus the 2–3 next-most-common journeys,
   written step by step as "user sees X, does Y, system responds Z" —
   with the exact screen ids.
5. Density & hierarchy notes per screen: what is one click away, what is
   deliberately buried behind disclosure.
No visual styling, no colors, no code. Output Markdown only.
[embed SPEC.md; if a reference pack exists, embed the annotated
screenshots with: "adapt these patterns — navigation structure,
disclosure, information density — to my features; do not clone layouts"]
```

PRD (Sonnet / Gemini Pro, fresh session):

```
Create a production-quality PRD from SPEC.md and UX.md below. Include:
functional requirements, non-functional requirements, user stories,
acceptance criteria, validation rules, error cases, edge cases (offline,
empty states), constraints, out-of-scope, future improvements.
Acceptance criteria must be FALSIFIABLE: observable behavior a human can
verify in the running app ("restart the app; saved items are listed"),
never adjectives ("clean", "minimalist") and never process facts ("tests
pass"). Every non-functional requirement carries a BUDGET and a
MEASUREMENT: the observable number plus the command or procedure that
produces it ("cold start under 2s, measured by <command>"); an NFR
without a measurement is a placeholder. Preserve the Kernel/v1/Backlog
split — do not promote backlog items. Do not discuss implementation.
Output Markdown only.
[embed SPEC.md + UX.md]
```

Architecture (Opus-tier, fresh session):

```
Act as a principal software architect. Read the PRD and UX below. Produce
ARCHITECTURE.md: system overview, module responsibilities and boundaries,
data model / DB schema (DDL with indices and constraints), API contract
(endpoints, request/response shapes, status codes, errors, auth),
component hierarchy mapped to UX.md screen ids, dependency graph, error
handling strategy, configuration strategy, and an empty Decision log
section at the end of the file — append-only, one line per future
decision as `YYYY-MM-DD — decision — why`; Phase 7 doc sync and Route C
patches append to it, never delete an earlier entry's why.
Rules: COMMIT to one concrete stack and one design per decision — no
"e.g. X or Y", no alternatives left open. Name the e2e/journey-test
harness as part of the stack commitment — CONVENTIONS.md's Test
strategy (Phase 3) and every gate's crystallization task (Phase 4)
build on this name. Include a DEPENDENCY PLAN section — buy is the
default: for every capability an established package serves, one line
`capability → package @ exact latest-stable/LTS version → what it
replaces` (I will verify versions against the registry); hand-rolled
capabilities name their reason (no credible package, trivial < ~30
lines, or core domain logic). No speculative utilities; trivial
helpers stay hand-rolled. I approve this list before the doc is
final. Every UX.md flow must be traceable through the
contract: for each kernel-journey step, name the API call or event
that serves it; if a step has no serving contract (e.g. "reopen app →
data restored" needs a list/read endpoint), add it.
When the kernel journey or a v1 flow depends on an EXTERNAL SYSTEM (a
paid API, third-party service — anything that will be faked in tests),
give that integration a versioned WIRE CONTRACT section: exact
request/response shapes, auth, error semantics — precise enough that a
fake can be validated against it. Extend traceability to those steps:
each names its wire contract. No external system → omit the section.
When the app has AUTH, STORES USER DATA, or ACCEPTS EXTERNAL INPUT,
include a THREAT MODEL section: trust boundaries (who can send what to
which surface), authN/authZ model per surface, input-validation
strategy at each boundary, secrets handling (where keys live, what is
never logged). No such surface → omit.
A decision genuinely unresolvable by reasoning (novel integration,
unproven performance) is not left open as "X or Y": mark it
`SPIKE: <question>` with the candidate answers, the leading candidate
(design against it), and the measurement that decides.
Do not write implementation code. Output Markdown only.
[embed PRD.md + UX.md]
```

Architecture review (fresh session, different model/vendor than the author — cross-vendor preferred):

```
Review ARCHITECTURE.md against the PRD and UX below. You did not write
it; judge the design, not the prose. Report only findings:
(1) a module or flow with no failure handling — what happens when this
call fails, times out, returns partial data?
(2) data-model flaws: a missing constraint, index, or key for a named
flow; a shape that breaks a stated requirement,
(3) concurrency/ordering hazards: two flows racing on the same state;
an event order the design assumes but nothing enforces,
(4) scale: the first thing that breaks at 10x data or users, when any
stated requirement implies growth,
(5) over-engineering: a module, layer, or abstraction serving no PRD
requirement — name the requirement or flag it,
(6) per major decision: the simplest credible alternative and why the
chosen design beats it — no credible answer is itself a finding,
(7) threat-model gaps (when the section exists): a trust boundary
crossed without validation; an authZ check missing for a named flow,
(8) build-vs-buy: a designed module duplicating an established,
maintained package (name the package), and any dependency-plan entry
failing the selection bar — unmaintained, license conflict, or a
transitive tree out of proportion to the need.
Each finding: section, severity, one-line consequence. No rewrites, no
style opinions, no praise.
[embed ARCHITECTURE.md + PRD.md + UX.md]
```

The user arbitrates the findings; ARCHITECTURE.md is patched before Phase 3.
