---
name: brana-2-prd-arch
description: "Use when a finalized SPEC.md exists and the user wants UX design, screens, wireframes, a PRD, product requirements document, system design, architecture, API contract, or database schema, mentions modules or components after a spec exists, or says next phase or phase 2."
---

# Phase 2 — UX.md + PRD.md + ARCHITECTURE.md

Three documents, in this order: UX → PRD → ARCHITECTURE (screens inform requirements; both inform architecture). UX.md is the missing artifact most workflows skip — without it, implementers get tokens and adjectives but no screens, every task improvises its own interface, and the result is incoherent. ARCHITECTURE.md becomes the single "current truth" every future impact analysis reads.

## Modes

- **run** (default): execute below. The workflow wants a fresh session per document; if the user runs all three here, finish each fully before starting the next.
- **prompt** (argument contains `prompt`): output the paste-ready prompt block(s) from the templates below with actual file contents embedded. No other output. UX + PRD target Sonnet/Pro tier; architecture targets Opus-tier — say which block goes where.

## Run mode

Locate the current cycle's SPEC.md (latest `specs/NNN-name/SPEC.md`).

**Step 1 — UX.md** (from SPEC.md). Act as a senior product designer. Produce:

1. Screen inventory: every screen/view/modal, each with an id (S1, S2…), purpose, entry points.
2. Navigation map (text diagram).
3. Per screen: a text wireframe — regions top-to-bottom/start-to-end, content per region, primary action, where the eye goes first. Include empty, loading, and error states.
4. Key flows: the kernel journey plus the 2–3 next-most-common journeys, step by step as "user sees X, does Y, system responds Z" — with exact screen ids.
5. Density & hierarchy notes per screen: what is one click away, what is deliberately buried behind disclosure.

No visual styling, no colors, no code. If SPEC names a reference pack, adapt its _patterns_ (navigation structure, disclosure, information density) — never clone layouts. Write to repo root — living doc, patched forever after.

**Tell the user to read UX.md and walk the flows before proceeding** — UX.md encodes intent no machine check can verify; a step that feels wrong on paper will be wrong in the app, and this is the cheapest moment to fix it.

**Step 2 — PRD.md** (from SPEC.md + UX.md). Include: functional requirements, non-functional requirements, user stories, acceptance criteria, validation rules, error cases, edge cases (offline, empty states), constraints, out-of-scope, future improvements. Acceptance criteria must be FALSIFIABLE: observable behavior a human can verify in the running app ("restart the app; saved items are listed"), never adjectives ("clean") and never process facts ("tests pass"). Preserve the Kernel/v1/Backlog split — do not promote backlog items. Do not discuss implementation. Write to the same `specs/NNN-name/` dir with frontmatter `status: draft` (UX.md and ARCHITECTURE.md are living docs — no stamps).

**Step 3 — ARCHITECTURE.md** (from PRD.md + UX.md). Act as a principal software architect. Include: system overview, module responsibilities and boundaries, data model / DB schema (DDL with indices and constraints), API contract (endpoints, request/response shapes, status codes, errors, auth), component hierarchy mapped to UX.md screen ids, dependency graph, error handling strategy, configuration strategy. Rules:

- COMMIT to one concrete stack and one design per decision — no "e.g. X or Y", no alternatives left open.
- **Traceability (load-bearing):** every UX.md flow must be traceable through the contract — for each kernel-journey step, name the API call or event that serves it; a step with no serving contract (e.g. "reopen app → data restored" needs a list/read endpoint) means add the contract. Implementers build only what the contract names.

No implementation code. Write to repo root — living doc, patched forever after.

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
pass"). Preserve the Kernel/v1/Backlog split — do not promote backlog
items. Do not discuss implementation. Output Markdown only.
[embed SPEC.md + UX.md]
```

Architecture (Opus-tier, fresh session):

```
Act as a principal software architect. Read the PRD and UX below. Produce
ARCHITECTURE.md: system overview, module responsibilities and boundaries,
data model / DB schema (DDL with indices and constraints), API contract
(endpoints, request/response shapes, status codes, errors, auth),
component hierarchy mapped to UX.md screen ids, dependency graph, error
handling strategy, configuration strategy.
Rules: COMMIT to one concrete stack and one design per decision — no
"e.g. X or Y", no alternatives left open. Every UX.md flow must be
traceable through the contract: for each kernel-journey step, name the
API call or event that serves it; if a step has no serving contract
(e.g. "reopen app → data restored" needs a list/read endpoint), add it.
Do not write implementation code. Output Markdown only.
[embed PRD.md + UX.md]
```
