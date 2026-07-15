---
name: brana-3-plan
description: "Use when UX.md, PRD.md and ARCHITECTURE.md exist and the user wants an implementation plan, coding conventions, design system, folder structure, or file layout, mentions the consistency gate, says write the plan or next step after architecture, or says phase 3."
---

# Phase 3 — PLAN.md + CONVENTIONS.md + DESIGN.md + FILE_STRUCTURE.md, then the Consistency Gate

The workflow's most leveraged phase: every implementation token downstream is spent following what's written here. Opus-tier quality pays off — after this phase, the planner does not participate in implementation. No task is written until the consistency gate's machine pass is clean.

## Modes

- **run** (default): execute below, including the consistency gate.
- **prompt** (argument contains `prompt`): output the paste-ready prompt blocks from the templates below with actual PRD.md + ARCHITECTURE.md + UX.md + SPEC design direction embedded — the four-docs block (Opus-tier) and the consistency-gate machine pass (Haiku/Flash tier, run after). No other output.

## Run mode

Read the current cycle's PRD.md and SPEC.md design direction (latest `specs/NNN-name/`) and root ARCHITECTURE.md + UX.md. Act as a senior full-stack architect with strong product design taste. Produce four complete files:

1. **PLAN.md** — implementation plan in ordered chunks. FIRST MILESTONE is the **WALKING SKELETON**: the thinnest end-to-end slice that makes the kernel journey pass in the real app (ugly is fine, fake is not). Later chunks deepen it. Every 2–3 chunks, insert a **DEMO GATE** — cadence is the target, **runnability is the constraint**: a gate sits only where the app launches and its journey is walkable end-to-end in the running app. Chunks between gates are vertical slices (each gate interval ends runnable, like the skeleton), never horizontal layers whose UI lands chunks later. No walkable point within ~4 chunks is a plan smell — restructure the chunks, don't stretch the gate. Each gate entry names: the exact journey to walk, what must be observed, and its **runnability preconditions** — the launch command, seed/fixture data the journey needs, and which prior chunk serves each journey step. A journey that would otherwise touch production state names a disposable/fixture path (fail-closed against non-disposable targets) as its launch precondition. For each chunk: files touched, exact requirements, falsifiable acceptance criteria, what NOT to do. Max ~300 lines of new code per chunk. Write to `specs/NNN-name/` with frontmatter `status: draft`.
2. **CONVENTIONS.md** — naming, error handling style, folder rules, test style, commit style. Under 2 pages: every line is context each future task pays for. Repo root (living doc).
3. **DESIGN.md** — the design system contract, styling the screens UX.md already defined. Repo root (living doc). Include:
   - **Direction**: 3 adjectives, reference apps, one deliberate visual signature.
   - **Tokens**: semantic color tokens with exact values (light AND dark if applicable); type scale (max 2 typefaces); spacing on a 4/8px grid; radii; shadows; motion durations/easings.
   - **Component states**: default, hover, focus-visible, active, disabled for every interactive element; empty, loading, error for every data view.
   - **Layout**: grid/breakpoints, max widths, density rules.
   - **Hard rules**: tokens only in components — no raw hex/px/font values; WCAG AA contrast; visible focus states; no template clichés.
   - **SINGLE-SOURCE RULE**: exact values appear ONLY in the token table; all prose refers to tokens by name, never by value. No template placeholders may remain — every value resolved.

   With a **pre-built design system**, DESIGN.md becomes an **adoption map** instead: single source of truth stays in the system's own files (theme config, token package); DESIGN.md refers by token name only. Contents: semantic role → system token mapping; component inventory (which existing component serves which UX.md element); **gap list** — UX.md needs the system can't serve, flagged for the user's approval before inventing a substitute; usage rules. With a **reference pack**, run a style-extraction vision pass first ("extract the observable style facts: palette roles, type scale, spacing rhythm, radius language") and get the user's approval before token generation.
4. **FILE_STRUCTURE.md** — the full file tree, every file that will exist, including the token definition file DESIGN.md implies. Repo root (living doc).

Do not write implementation code. Then run the consistency gate below. Do not split into tasks — that is Phase 4, a fresh session, and it is blocked until the machine pass is clean.

## Consistency Gate (blocks Phase 4)

Generated contracts routinely ship with the same fact stated two ways, unfilled placeholders, and open decisions — implementers don't halt on contradictions, they pick a clause arbitrarily per file.

1. **Machine pass (mandatory, blocking)** — across SPEC, UX, PRD, ARCHITECTURE, PLAN, DESIGN, CONVENTIONS, FILE_STRUCTURE, list: every internal contradiction (same fact, different values in two places), every unresolved placeholder or template variable, every decision left open ("X or Y"), every UX.md flow step with no serving ARCHITECTURE.md contract, and — in PLAN.md — every DEMO GATE journey step with no serving chunk before the gate, plus every gate missing its runnability preconditions (launch command, seed data). Pre-built design system attached → also list every token/component name DESIGN.md cites that doesn't exist in the system files. Fix all findings before proceeding. Machine pass clean → flip the `status:` stamp on SPEC.md, PRD.md, and PLAN.md from `draft` to `gate-passed` (Phase 4 refuses a `draft` PLAN.md).
2. **Human pass (advisory)** — present the machine findings plus per-doc summaries and remind the user: read SPEC.md and UX.md at minimum (~20 min each — they encode intent, which no machine check verifies; wrong-but-consistent docs pass every machine pass). "Continue" proceeds.

## Prompt mode templates

Four docs (Opus-tier, fresh session):

```
You are a senior full-stack architect with strong product design taste.
Using PRD.md, ARCHITECTURE.md, UX.md and the design direction below,
produce four complete markdown files:

1. PLAN.md — implementation plan in ordered chunks. FIRST MILESTONE is
   the WALKING SKELETON: the thinnest end-to-end slice that makes the
   kernel journey pass in the real app (ugly is fine, fake is not).
   Later chunks deepen it. Every 2–3 chunks, insert a DEMO GATE —
   cadence is the target, runnability the constraint: a gate sits only
   where the app launches and its journey is walkable end-to-end in the
   running app. Chunks between gates are vertical slices (each gate
   interval ends runnable), never horizontal layers whose UI lands
   chunks later. No walkable point within ~4 chunks is a plan smell —
   restructure the chunks, don't stretch the gate. Each gate entry
   names: the exact journey to walk, what must be observed, and its
   runnability preconditions — launch command, seed/fixture data, and
   which prior chunk serves each journey step; a journey that would
   otherwise touch production state names a disposable/fixture path
   (fail-closed against non-disposable targets). For each chunk: files
   touched, exact requirements, falsifiable acceptance criteria, what
   NOT to do. Max ~300 lines of new code per chunk.
2. CONVENTIONS.md — naming, error handling style, folder rules, test
   style, commit style. Keep it under 2 pages: every line here is a line
   of context each future task pays for.
3. DESIGN.md — the design system contract, styling the screens UX.md
   already defined. Include:
   a. Direction: 3 adjectives, reference apps, one deliberate visual
      signature.
   b. Tokens: semantic color tokens with exact values (light AND dark if
      applicable); type scale (max 2 typefaces); spacing on a 4/8px
      grid; radii; shadows; motion durations/easings.
   c. Component states: default, hover, focus-visible, active, disabled
      for every interactive element; empty, loading, error for every
      data view.
   d. Layout: grid/breakpoints, max widths, density rules.
   e. Hard rules: tokens only in components — no raw hex/px/font values;
      WCAG AA contrast; visible focus states; no template clichés.
   SINGLE-SOURCE RULE: exact values appear ONLY in the token table;
   all prose refers to tokens by name, never by value. No template
   placeholders may remain — every value is resolved.
4. FILE_STRUCTURE.md — the full file tree, every file that will exist.

Output the four files completely. No conversational text.
[embed PRD.md + ARCHITECTURE.md + UX.md + design direction]
```

With a pre-built design system, item 3 switches to adoption-map mode: embed the system's token/component files and ask for mapping, inventory, and gap list instead of new tokens. With a reference pack, run the style-extraction vision pass first and approve it before this prompt.

Consistency-gate machine pass (Haiku/Flash tier, fresh session):

```
Here are this project's contract docs: [embed SPEC, UX, PRD, ARCHITECTURE,
PLAN, DESIGN, CONVENTIONS, FILE_STRUCTURE]. List every internal contradiction
(same fact stated with different values in two places), every unresolved
placeholder or template variable, every decision left open ("X or Y"),
every UX.md flow step with no serving ARCHITECTURE.md contract, and —
in PLAN.md — every DEMO GATE journey step with no serving chunk before
the gate, plus every gate missing its runnability preconditions
(launch command, seed data).
If a pre-built design system is attached, also list every token or
component name DESIGN.md cites that does not exist in the system files.
Report only findings with doc + quote. No rewrites.
```
