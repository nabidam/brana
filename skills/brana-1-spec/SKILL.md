---
name: brana-1-spec
description: "Use when the user has a new app idea to plan, mentions writing a spec, requirements, features, or asks what should we build, wants a SPEC.md draft gap-checked, or says phase 1 or start the workflow. Use before any coding starts on a new project, even if the user says let's just code it."
---

# Phase 1 — SPEC.md + Scope Challenge

Turn an idea into a spec under 500 words plus a kernel section. The spec feeds every later phase, so ambiguity here is expensive; length is not a virtue. Depth beats breadth: v1 is the smallest feature set that delivers the core promise, built well — the scope challenge enforces this.

## Modes

- **run** (default): execute below.
- **prompt** (argument contains `prompt`): output paste-ready prompt block(s) for an external chat UI using the templates at the bottom, with the user's draft/idea embedded. No other output. Gap-check targets Haiku/Flash tier; interview targets Sonnet/Pro tier.

## Run mode

**Milestone map first (big ideas):** an idea spanning multiple independent subsystems ("a platform with chat, billing, and analytics") or estimated beyond ~15–20 tasks is decomposed into **milestones** before any detail questions. Each milestone is its own `specs/NNN-name/` cycle, ≤ ~15 tasks, ending in a working, release-gated version of the app at that stage — never a horizontal layer that only pays off later. M1 is the kernel milestone (smallest working version delivering the core promise): spec it now. Later milestones get 2–3 lines each (name, goal, rough scope) in `specs/ROADMAP.md` — coarse by design; detail is authored when that milestone's own cycle starts (Route C shape, delta qualification, so later milestones often run lite). ROADMAP.md is re-checked at each milestone's end. Single-cycle ideas need no ROADMAP.md. Don't spend questions refining a project that needs splitting.

Two paths — pick by what the user has:

**Has a draft** (even rough notes): gap-check it. List anything ambiguous or missing that a developer would need to know. Do not rewrite the draft, do not design, do not implement. Ask the user to resolve gaps.

**Starting from nothing**: act as a senior product manager. Interview the user until every important requirement is clear — one question at a time, no assumptions, challenge vague requirements, suggest simpler alternatives. **Ask what the user is already thinking before offering ideas** — surfaces hidden context, prevents fixation on your framing. Use AskUserQuestion with multiple-choice options when 2–4 genuinely distinct options exist; open-ended when they don't.

**Approaches (when multiple plausible directions remain):** propose 2–3 concrete approaches — each a 2–3-sentence description, pros/cons, key risks. Present all options **before** naming a recommendation — recommending first anchors the user. Drop or sharpen any approach generic enough to appear in a listicle for this problem category. One clearly-best direction → state it, skip the menu.

**Then the scope challenge (required — skipping it is how ten shallow features beat four good ones).** As a ruthless product owner:

1. State the product's core promise in one sentence.
2. Identify the **KERNEL**: the 3–5 features without which the product is pointless. Everything else goes to a ranked v1.1+ backlog. Convenience features (scheduling, power-user overrides, localization, theming and kin) are backlog by default — they enter v1 only by the user's explicit call.
3. Write the **KERNEL JOURNEY**: one end-to-end user story, step by step, exercising every kernel feature ("create an item → see the result → close app → reopen → the item is still there"). It becomes the walking-skeleton target (Phase 5) and the standing demo-gate script (Phase 6b).
4. Flag any spec'd feature that undermines the core promise if built shallowly — those are kernel or cut, never "shallow v1". Present flags to the user for the call.
5. **Provenance check:** every v1 bullet traces to user-stated, kernel-derived, or **process-derived** (workflow machinery wanting a deliverable: verification tooling, output/formatting modules, audit commands). Process-derived bullets go to the user as a named list with rough task cost each — they enter v1 only by explicit call, same standing as convenience features.
6. **Minimal-form rule (hard):** minimizing language from the user ("just a flag", "only a dry-run argument") caps the deliverable at the minimal form satisfying the stated need. Elaborations — a second mode, a dedicated module, a separate CLI, sentinel suites — are backlog by default, listed as named options with cost; silent inclusion is the amplification failure this rule exists to kill.

**Integration check (before writing SPEC.md):** combine the answers gathered so far and surface non-obvious consequences no single question covered ("X plus Y together means Z is lost on restart") — one open probe per genuine combination effect. An answer revealing genuine uncertainty is recorded as an explicit assumption in SPEC.md, never silently resolved.

The final SPEC.md covers:

1. Core promise (one sentence)
2. **Kernel** — the 3–5 features, with the kernel journey verbatim
3. **v1** / **Backlog** (ranked) split
4. Edge cases
5. Non-functional requirements + tech constraints
6. Suggested Tech Stack (user's preference wins; propose one if they have none)
7. Design direction (3–5 lines, required — feeds UX.md and DESIGN.md): product personality as 3 adjectives, 2–3 reference apps whose look is the target, platform density, accessibility floor (WCAG AA). If the user has a pre-built design system or an annotated reference-screenshot pack, name them here instead ("Design system: X. Deltas: [any]" / "Reference pack: references/"). No answer → propose a direction and confirm; never leave "clean and modern".
8. Out-of-scope

**Profile choice (last step, user confirms):** check the Route S qualification (WORKFLOW.md, Route S — Lite v1 Profile): single subsystem, ≤ ~15 estimated tasks, no **novel** external integration — a well-known API via an official/established SDK does *not* disqualify (its wire contract ships compact, ≤1 page, verified-fake rule still applies); only a bespoke/undocumented integration does — low stakes (no multi-user data, no payments). Route C change cycles use the **delta qualification** instead — same four criteria against the delta only; an existing integration already in ARCHITECTURE.md does not disqualify. All four hold → propose `profile: lite`: PRD folds into a SPEC acceptance-criteria section (falsifiable; NFR budgets+measurements if any), UX.md/ARCHITECTURE.md ship mini/lite, PLAN.md/FILE_STRUCTURE.md are cut, DESIGN.md only if UI-heavy; ≤ ~5 estimated tasks additionally folds the mid demo gate into the release gate (one gate, full anatomy). Any criterion fails → `profile: full` **plus `profile-reason: <the failing criterion>`** — an unjustified `profile: full` is a `brana-gate docs` finding, because it means this qualification never ran. Downstream phases read the stamp; mid-flight outgrowth is a hard stop + upgrade, and Phase 4's downgrade valve catches the reverse (full profile whose real split fits lite).

**Speed signal (hard rule):** the user saying "fast delivery", "no demo gates", "just ship it so I can test" or kin makes two things mandatory *before drafting SPEC.md*: (1) run the profile qualification and propose lite if it holds; (2) propose an explicit **delivery contract** — frontmatter line `delivery: demo_gates=waived walkthrough=waived canary=required` (closed keys: `demo_gates`, `walkthrough`, `canary`; values `required`|`waived`; see WORKFLOW.md, Delivery Contract). A waiver names its substitute from machinery the cycle already has (verify script, test suite, crystallized journeys) — a substitute requiring *new tooling* is process-derived scope for the provenance check, never a waiver by-product. Waivers invented later in TASKS.md frontmatter are a gate finding.

Keep it under 500 words plus the kernel section (lite: ~700 words including the acceptance-criteria section). Write to `specs/001-core/SPEC.md` for a new app (later cycles: next `specs/NNN-name/`) with frontmatter `status: draft` plus `profile: lite`, or `profile: full` + `profile-reason: <failing criterion>` (and the `delivery:` line when chosen) — the Phase 3 consistency gate flips status to `gate-passed`.

**Spec self-review (after writing, before handing over):** re-read the file fresh — (1) placeholders/TBDs, (2) internal contradictions, (3) scope: fits one cycle or needs decomposition, (4) ambiguity: any requirement readable two ways → pick one and make it explicit. Fix inline, then ask the user to read it. Catches at zero cost what the Phase 3 consistency gate would catch two phases later.

Do not proceed to UX/PRD/architecture — that is Phase 2, a fresh session.

## Prompt mode templates

Gap-check (Haiku/Flash tier):

```
I'm drafting a spec for [app]. Here's what I have so far: [embed draft].
List anything ambiguous or missing that a developer would need to know.
Do not rewrite the spec. Do not design or implement anything.
```

Interview (Sonnet/Pro tier):

```
You are a senior product manager. I want to build [embed the user's one-paragraph app description]. Interview me until every important requirement is clear. First ask what I'm already considering, before offering ideas of your own. Do not make assumptions. Ask questions one by one. Challenge vague requirements. Suggest simpler alternatives. When finished, produce SPEC.md: core features & user stories, edge cases, suggested tech stack, UI/UX guidelines. Do not proceed to architecture.
```

Approaches (Sonnet/Pro tier, when multiple plausible directions remain):

```
Here is what we know so far: [embed notes/draft]. Propose 2–3 concrete
approaches to this product: each with a 2–3 sentence description, pros,
cons, key risks. Present all options first; only then name your
recommendation and why. Drop any approach generic enough to appear in a
listicle for this problem category. Do not write the spec.
```

Scope challenge (required, after either path):

```
Here is my spec: [embed]. You are a ruthless product owner.
1. State this product's core promise in one sentence.
2. Identify the KERNEL: the 3–5 features without which the product is
   pointless. Everything else goes to a ranked v1.1+ backlog.
3. Write the KERNEL JOURNEY: one end-to-end user story, step by step,
   that exercises every kernel feature ("create an item → see the
   result → close app → reopen → the item is still there").
4. Flag any spec'd feature that undermines the core promise if built
   shallowly — those are kernel or cut, never "shallow v1".
5. Mark every v1 bullet's provenance: user-stated, kernel-derived, or
   process-derived (tooling the process wants, not the user). List the
   process-derived ones separately with a rough cost — they need my
   explicit call to stay in v1.
6. Where I used minimizing language ("just", "only a"), hold the
   deliverable to its minimal form; list elaborations as options, do
   not fold them in.
Do not add features. Do not design.
```

Fold the result back into SPEC.md as Kernel / v1 / Backlog.
