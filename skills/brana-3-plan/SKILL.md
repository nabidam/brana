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

**Locating `brana-gate`:** every `brana-gate` invocation below resolves in order — (1) `scripts/brana_gate.py` bundled beside this SKILL.md (run `python3 <skill-dir>/scripts/brana_gate.py ...`); (2) `brana-gate` on PATH; (3) `tools/brana-gate` when the working directory is the Brana repo itself. None found -> state which locations were checked, then the full checklist runs as the LLM pass (copy-paste mode).

Read the current cycle's PRD.md and SPEC.md design direction (latest `specs/NNN-name/`) and root ARCHITECTURE.md + UX.md. **SPEC.md `profile: lite` → Route S deltas:** produce only item 2 (CONVENTIONS.md, ≤1 page) and — if UI-heavy — item 3 (DESIGN.md; otherwise CONVENTIONS.md carries ≤5 style rules: spacing scale, one accent, focus visible, WCAG AA); no PLAN.md, no FILE_STRUCTURE.md — chunking and gates are authored in Phase 4's TASKS.md directly. The consistency gate shrinks to `brana-gate docs` over SPEC/UX/ARCHITECTURE/CONVENTIONS(+DESIGN) plus a short LLM pass (contradictions, open decisions, kernel-journey steps with no serving contract) and flips SPEC.md to `gate-passed`. Act as a senior full-stack architect with strong product design taste. Produce four complete files:

1. **PLAN.md** — implementation plan in ordered chunks. Every ARCHITECTURE.md `SPIKE:` marker becomes a time-boxed **spike chunk** at the head of the plan: throwaway code allowed, its acceptance criterion is the marker's falsifiable measurement, its output is a Decision log entry replacing the marker. Dependent chunks are planned against the marker's leading candidate; a spike result that overturns it patches ARCHITECTURE.md and triggers the stale-plan and stale-interface-block rules — cheap at chunk 2, catastrophic at release. Then the FIRST MILESTONE is the **WALKING SKELETON**: the thinnest end-to-end slice that makes the kernel journey pass in the real app (ugly is fine, fake is not). Later chunks deepen it. Every 2–3 chunks, insert a **DEMO GATE** — cadence is the target, **runnability is the constraint**: a gate sits only where the app launches and its journey is walkable end-to-end in the running app. Chunks between gates are vertical slices (each gate interval ends runnable, like the skeleton), never horizontal layers whose UI lands chunks later. No walkable point within ~4 chunks is a plan smell — restructure the chunks, don't stretch the gate. Each gate entry names: the exact journey to walk, what must be observed, and its **runnability preconditions** — the launch command, seed/fixture data the journey needs, and which prior chunk serves each journey step. A journey that would otherwise touch production state names a disposable/fixture path (fail-closed against non-disposable targets) as its launch precondition. **Same-composition rule:** every gate launch command is the app's production entry point with disposable config/fakes injected at seams — a bespoke gate-only composition is a blocking finding (it lets every gate pass while the production path stays unbuilt). The **last entry is the RELEASE GATE** (the v1 exit bar as a plan entry): the kernel journey in a release build, same gate anatomy, each step served by a chunk through the production composition; when fakes stand in for an external system, one chunk before it is the **production-composition proof** — the production entry point composes fully and runs against a disposable target (live calls stay canary-only). For each chunk: files touched, exact requirements, falsifiable acceptance criteria, what NOT to do. Max ~300 lines of new code per chunk. Write to `specs/NNN-name/` with frontmatter `status: draft`.
2. **CONVENTIONS.md** — naming, error handling style, folder rules, test style, commit style, and **Test strategy**: which layer (`[unit]`/`[integration]`/`[contract]`/`[e2e@gate-N]`) verifies which criterion type, the frameworks for each, the e2e/journey-test harness named in ARCHITECTURE.md, and the verify command. Under 2 pages: every line is context each future task pays for. **Lint-over-prose rule:** a convention a machine can check becomes a lint rule at Task 0; prose is only for what lint can't see. **Package-before-custom rule:** implementing a capability ARCHITECTURE.md's dependency plan assigns to a package is a review finding. Repo root (living doc).
3. **DESIGN.md** — the design system contract, styling the screens UX.md already defined. Repo root (living doc). Include:
   - **Direction**: 3 adjectives, reference apps, one deliberate visual signature.
   - **Tokens**: semantic color tokens with exact values (light AND dark if applicable) and, for every fg/bg token pair used as text-on-background, the computed contrast ratio; type scale (max 2 typefaces); spacing on a 4/8px grid; radii; shadows; motion durations/easings. **Token-source handoff:** once Task 0 emits the token file (Phase 5), values live only there — DESIGN.md keeps roles + usage rules and refers to the file, never restates a value. The contrast ratios move with the values: once the token file is the source, ratios are maintained there (or its adjacent doc), never back in DESIGN.md prose, and the consistency/doc-sync checks read them from that file from then on.
   - **Component states**: default, hover, focus-visible, active, disabled for every interactive element; empty, loading, error for every data view.
   - **Layout**: grid/breakpoints, max widths, density rules.
   - **Hard rules**: tokens only in components — no raw hex/px/font values; WCAG AA contrast; visible focus states; no template clichés.
   - **SINGLE-SOURCE RULE**: exact values appear ONLY in the token table; all prose refers to tokens by name, never by value. No template placeholders may remain — every value resolved.

   With a **pre-built design system**, DESIGN.md becomes an **adoption map** instead: single source of truth stays in the system's own files (theme config, token package); DESIGN.md refers by token name only. Contents: semantic role → system token mapping; component inventory (which existing component serves which UX.md element); **gap list** — UX.md needs the system can't serve, flagged for the user's approval before inventing a substitute; usage rules. With a **reference pack**, run a style-extraction vision pass first ("extract the observable style facts: palette roles, type scale, spacing rhythm, radius language") and get the user's approval before token generation.
4. **FILE_STRUCTURE.md** — the full file tree, every file predicted to exist this cycle, including the token definition file DESIGN.md implies. A **per-cycle artifact** written to `specs/NNN-name/`: a prediction for the planner and Task 0, archived after — never a living doc, no status stamp. The repo tree and code map are the living truth once code exists.

Do not write implementation code. Then run the consistency gate below. Do not split into tasks — that is Phase 4, a fresh session, and it is blocked until the machine pass is clean.

## Consistency Gate (blocks Phase 4)

Generated contracts routinely ship with the same fact stated two ways, unfilled placeholders, and open decisions — implementers don't halt on contradictions, they pick a clause arbitrarily per file.

1. **Machine pass (mandatory, blocking)** — script-first: run `brana-gate docs` over all eight docs (unresolved placeholders; every DESIGN.md contrast ratio computed — never computed by an LLM — with stated-vs-computed mismatches flagged) and fix to a clean exit. Then the LLM judgment pass — across SPEC, UX, PRD, ARCHITECTURE, PLAN, DESIGN, CONVENTIONS, FILE_STRUCTURE, list: every internal contradiction (same fact, different values in two places), every unresolved placeholder or template variable, every decision left open ("X or Y"), every UX.md flow step with no serving ARCHITECTURE.md contract, and — in PLAN.md — every DEMO GATE journey step with no serving chunk before the gate, every gate missing its runnability preconditions (launch command, seed data), every gate launch command that is not the production entry point with disposable inputs (a bespoke gate-only composition), a missing RELEASE GATE entry, and every RELEASE GATE journey step with no serving chunk through the production composition. Also flag: every external system in SPEC.md's kernel journey or a v1 flow that ARCHITECTURE.md gives no wire contract; every PRD.md acceptance criterion that would be tagged `[e2e@gate-N]` (behavior only observable end-to-end in the running app) with no corresponding gate journey step in PLAN.md; every fg/bg contrast ratio listed in DESIGN.md's token table that falls below WCAG AA; every ARCHITECTURE.md `SPIKE:` marker with no spike chunk at the head of PLAN.md, and every spike chunk missing its falsifiable answer criterion or time box; and every PRD.md non-functional requirement with no serving mechanism — a verify-script check, a tagged acceptance criterion, or a release-gate observation step naming its measurement. Pre-built design system attached → also list every token/component name DESIGN.md cites that doesn't exist in the system files. Fix all findings before proceeding. Machine pass clean → flip the `status:` stamp on SPEC.md, PRD.md, and PLAN.md from `draft` to `gate-passed` (Phase 4 refuses a `draft` PLAN.md).
2. **Human pass (advisory)** — present the machine findings plus per-doc summaries and remind the user: read SPEC.md and UX.md at minimum (~20 min each — they encode intent, which no machine check verifies; wrong-but-consistent docs pass every machine pass). "Continue" proceeds.

## Prompt mode templates

Four docs (Opus-tier, fresh session):

```
You are a senior full-stack architect with strong product design taste.
Using PRD.md, ARCHITECTURE.md, UX.md and the design direction below,
produce four complete markdown files:

1. PLAN.md — implementation plan in ordered chunks. Every
   ARCHITECTURE.md `SPIKE:` marker becomes a time-boxed SPIKE CHUNK at
   the head of the plan: throwaway code allowed, its acceptance
   criterion is the marker's falsifiable measurement, its output is a
   Decision log entry replacing the marker. Dependent chunks are
   planned against the marker's leading candidate; a spike result that
   overturns it patches ARCHITECTURE.md and triggers the stale-plan
   and stale-interface-block rules — cheap at chunk 2, catastrophic at
   release. Then the FIRST MILESTONE is
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
   (fail-closed against non-disposable targets). SAME-COMPOSITION RULE:
   every gate launch command is the app's production entry point with
   disposable config/fakes injected at seams — a bespoke gate-only
   composition is a blocking finding. The LAST entry is the RELEASE
   GATE: the kernel journey in a release build, same gate anatomy, each
   step served by a chunk through the production composition; when
   fakes stand in for an external system, one chunk before it is the
   production-composition proof — the production entry point composes
   fully and runs against a disposable target (live calls stay
   canary-only). For each chunk: files
   touched, exact requirements, falsifiable acceptance criteria, what
   NOT to do. Max ~300 lines of new code per chunk.
2. CONVENTIONS.md — naming, error handling style, folder rules, test
   style, commit style, and Test strategy: which layer
   (`[unit]`/`[integration]`/`[contract]`/`[e2e@gate-N]`) verifies which
   criterion type, the frameworks for each, the e2e/journey-test harness
   named in ARCHITECTURE.md, and the verify command. Keep it under 2
   pages: every line here is a line of context each future task pays
   for. Lint-over-prose rule: a convention a machine can check becomes a
   lint rule at Task 0; prose is only for what lint can't see.
   Package-before-custom rule: implementing a capability the dependency
   plan assigns to a package is a review finding.
3. DESIGN.md — the design system contract, styling the screens UX.md
   already defined. Include:
   a. Direction: 3 adjectives, reference apps, one deliberate visual
      signature.
   b. Tokens: semantic color tokens with exact values (light AND dark if
      applicable) and, for every fg/bg token pair used as text-on-
      background, the computed contrast ratio; type scale (max 2
      typefaces); spacing on a 4/8px grid; radii; shadows; motion
      durations/easings. Token-source handoff: once Task 0 emits the
      token file (Phase 5), values live only there — DESIGN.md keeps
      roles + usage rules and refers to the file, never restates a
      value. The contrast ratios move with the values: once the token
      file is the source, ratios are maintained there (or its adjacent
      doc), never back in DESIGN.md prose, and the consistency/doc-sync
      checks read them from that file from then on.
   c. Component states: default, hover, focus-visible, active, disabled
      for every interactive element; empty, loading, error for every
      data view.
   d. Layout: grid/breakpoints, max widths, density rules.
   e. Hard rules: tokens only in components — no raw hex/px/font values;
      WCAG AA contrast; visible focus states; no template clichés.
   SINGLE-SOURCE RULE: exact values appear ONLY in the token table;
   all prose refers to tokens by name, never by value. No template
   placeholders may remain — every value is resolved.
4. FILE_STRUCTURE.md — the full file tree, every file predicted to
   exist this cycle. A per-cycle artifact written to `specs/NNN-name/`:
   a prediction for the planner and Task 0, archived after — never a
   living doc. The repo tree and code map are the living truth once
   code exists.

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
(launch command, seed data), every gate launch command that is not the
production entry point with disposable inputs (a bespoke gate-only
composition), a missing RELEASE GATE entry, and every RELEASE GATE
journey step with no serving chunk through the production composition.
Also flag: every external system in SPEC.md's kernel journey or a v1
flow that ARCHITECTURE.md gives no wire contract; every PRD.md
acceptance criterion that would be tagged `[e2e@gate-N]` (behavior only
observable end-to-end in the running app) with no corresponding gate
journey step in PLAN.md; and every fg/bg contrast ratio listed in
DESIGN.md's token table that falls below WCAG AA.
Also: every ARCHITECTURE.md SPIKE marker with no spike chunk at the
head of PLAN.md, and every spike chunk missing its falsifiable answer
criterion or time box; every PRD.md non-functional requirement with no
serving mechanism — a verify-script check, a tagged acceptance
criterion, or a release-gate observation step naming its measurement.
If a pre-built design system is attached, also list every token or
component name DESIGN.md cites that does not exist in the system files.
Report only findings with doc + quote. No rewrites.
```
