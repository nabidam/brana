# Brana — App Development Workflow (v1.4)

Consolidated from 5 agent proposals, revised after a v1 post-mortem. Optimized for token efficiency + output quality. Works for any app idea. Folds in tested patterns from two public workflows ([superpowers](https://github.com/obra/superpowers), [compound-engineering](https://github.com/EveryInc/compound-engineering)): path-based delegation, task interface blocks, live verification evidence, reviewer independence, and doc status stamps. Pre-release lineage (internal v2.0–v2.2) is in CHANGELOG.md.

Maintenance rule for this doc and the skills: every line must change agent behavior — if deleting it would not change the output, delete it. Adjectives earn their place only when operationalized by a concrete rule.

Execution medium: copy-paste is canon — a human moving prompts between chat UIs, no agent tooling assumed; every prompt in this doc works that way. When run inside agent tooling (Claude Code), the Agent Adaptation Layer below translates the copy-paste rules. Phases 1–3 may also run in another vendor's chat UI (e.g. Gemini), outputs committed as files. Phases 1–6 build v1. Phase 7 is the change loop for everything after. After v1, `ARCHITECTURE.md`, `CONVENTIONS.md`, `DESIGN.md`, `UX.md` are living artifacts: commit them, patch them, never regenerate from scratch and never append "deviations" ledgers — when code legitimately diverges, the doc is amended. `SPEC.md`, `PRD.md`, `PLAN.md`, `TASKS.md`, `FILE_STRUCTURE.md` are per-cycle artifacts, archived under `specs/NNN-name/`. FILE_STRUCTURE.md is a per-cycle prediction (planner + Task 0 input), not a living doc — the repo tree and code map are the living truth for structure. Per-cycle artifacts carry a `status:` frontmatter stamp — `draft` on write, flipped to `gate-passed` when their gate clears (consistency gate for SPEC/PRD/PLAN; Route B impact analysis for a mini-spec), and to `ready` on TASKS.md when the task gate clears; a consuming phase refuses a doc whose stamp hasn't cleared. Stamps never store progress — task completion is derived from git and TASKS.md task marks, nowhere else.

## Reality Rules (these outrank everything below)

The failure mode this workflow guards against: every task green, every doc consistent-looking, app unusable. These rules are the countermeasure.

1. **The deliverable is the running app, not the documents.** A phase whose output is only markdown is scaffolding; it earns nothing on its own. Any conflict between "the doc says done" and "the app doesn't do it" resolves in favor of the app's reality.
2. **Done = demonstrated.** A task is Done when its behavior has been exercised in the running app (or via a test that actually drives it), not when the code it wrote passes the tests it wrote for itself. Per-task visual verification (launch-and-look + screenshot) is **opt-in**: the agent does it only when the human asks for it on that task or in CONVENTIONS.md; otherwise UI tasks pass on tests + acceptance behavior, and visual quality is caught by the human at the next demo gate (rule 3).
3. **Demo gate every 2–3 tasks.** You (human) launch the build and walk one scripted user journey from UX.md. Findings become tasks before new features proceed. This is Phase 6b. Before the stop, the agent preflights the gate — builds, launches, confirms the journey is reachable; a failed preflight is `GATE BLOCKED` (fix tasks first, walk later), never an invitation to walk a broken app. Soft stop: at a gate the agent halts, prints the journey script plus the launch command, and reminds you; you may reply "continue" to skip — the skip is logged as `GATE SKIPPED` against the gate task in TASKS.md and every skipped gate is surfaced at the v1 exit bar. Skipping is visible debt, never silence.
4. **Scope cuts escalate, never archive.** If an implementer or planner discovers mid-flight that a spec'd, user-visible behavior won't be built (e.g. "user data doesn't survive a restart"), that is a stop-the-line event requiring your explicit decision. Documenting a cut in a gotchas file is not a decision — it's laundering. This is the one hard stop in the workflow: gates soften (rule 3), scope cuts never do — verification is delegable, product decisions are not. The agent states the cut and ends its turn; there is no "continue" default.
5. **One source of truth per fact.** A value (color, name, payload shape) lives in exactly one place; every other doc references it, never restates it. Contradictions between docs fail the _documents_ and block the next phase.
6. **Unread intent docs are the residual risk you accept.** A generated doc nobody has read is not a contract. The machine pass of the Consistency Gate catches the mechanical failure class (placeholders, contradictions, open decisions, unserved flow steps) and is mandatory; human reading is advisory — but SPEC.md and UX.md encode _intent_, which no machine check can verify: wrong-but-consistent docs pass every machine pass. Read those two at minimum; ~20 minutes each is the cheapest QA in the whole workflow.
7. **Depth beats breadth.** v1 is the smallest feature set that delivers the product's core promise, built well. Everything else is v1.1. The scope challenge in Phase 1 enforces this.
8. **A passed human check compiles into a machine check.** The first time a human verifies something by hand — walking a journey, checking a seam, spotting a convention violation — the pass is encoded: walked journeys become e2e tests, PRODUCES blocks become contract tests, recurring review findings become lint rules or CONVENTIONS.md lines. Human judgment is reserved for what machines can't check (intent, taste); spending it twice on the same check is the workflow failing.

## Git Rules

1. **Never implement on main uninvited.** Phase 5 begins by checking the
   current branch: on main/master, create the cycle branch (named after the
   spec dir, e.g. `001-core`) before any code. Direct-to-main only when the
   human explicitly says so — per instance, or as a standing rule in
   CONVENTIONS.md.
2. **Commit after each task** passes its gate — per-task rollback beats
   re-pasting a whole feature. (Schema changes roll back via down
   migration, never git revert — see Phase 5.)
3. **Branch per feature** in Phase 7: Routes B/C/R work on a feature
   branch, merged only after Phase 6 review + doc sync. Route A uses a
   short-lived branch merged after verify is green; the human may waive
   the branch per instance.
4. **Diffs come from git.** Phase 6a "review after 2–3 tasks" = diff of
   those commits; "feature diff" = the branch diff.

## Token Rules

1. **Expensive model plans, cheap model codes.** Opus-tier only for Phases 2–3 and impact analysis. Sonnet-tier implements. Haiku/Flash-tier for boilerplate, checklists, doc sync. Concrete bindings in the Model Bindings table below.
2. **Fresh session per phase; per task-batch in Phase 5.** One session per 2–3-task batch, cleared at each demo gate (the gate is the natural flush point). Batch size starts at 2–3 and is tuned per project; record the tuned number in CONVENTIONS.md. Never carry chat history across phases — carry only the output files.
3. **Paste only what the phase needs** (copy-paste mode). Per task: the task spec + conventions + only the files it touches. Never the whole codebase. In agent mode this rule relaxes — see Agent Adaptation Layer.
4. **Small tasks.** Each task ≤ ~50–300 lines of new code, completable in one prompt.
5. **Reviewer reports, never rewrites.** Findings with file:line + one-line fix. Diffs only, no full-project review.
6. **No conversational output.** Every generation prompt ends with "Output the Markdown/code directly, no pleasantries."
7. **Screenshots are cheap context, not a requirement.** A screenshot of the running app pasted into a review or fix prompt beats three paragraphs describing it — use them when you have them, but capturing is always the human's choice, never a mandated step. Gate screenshots, when taken, are archived under `specs/NNN-name/screenshots/`.

## Verification Machinery

- **Verify script:** one documented command running build + lint + typecheck + full test suite (+ the journey suite once it exists). UI stacks: verify also runs an automated a11y check (axe or equivalent), wired at Task 0 alongside the rest of the script. Created in Task 0, recorded in CONVENTIONS.md. Every task completion runs it; demo-gate preflight runs it.
- **Journey suite:** the automated e2e tests produced by crystallization tasks — each demo gate's walked journey, encoded after its first witnessed pass (Reality Rule 8). Part of verify once it exists.
- **Evidence file:** `specs/NNN-name/evidence/task-N.txt` — the exercised command plus the last ~30 lines of its output, captured live at task completion. The TASKS.md done-mark references its path.
- **Production composition:** the app's real entry point with its production wiring. Disposable/fixture modes inject config, seams, and fakes _inside_ that composition — never a parallel gate-only assembly. A gate's launch command is the production entry point with disposable inputs; a bespoke gate runtime is a blocking finding (it lets every gate pass while the production path stays unbuilt).
- **Wire contract** (conditional — only when the kernel journey or a v1 flow depends on an external system that will be faked): a versioned, exact request/response contract for that integration — shapes, auth, error semantics — specified in ARCHITECTURE.md. Every fake of that system is a **verified fake**: one shared contract suite runs against both the fake and the real adapter, and the fake must reject what the contract rejects. The real-adapter side is offline-assertable (request-shape assertions, recorded fixtures); live provider calls happen only in a bounded canary routed through the production composition.
- **Gate linter:** `tools/brana-gate` (single-file Python 3.11+, stdlib only) — the deterministic half of both machine gates. `brana-gate tasks TASKS.md --plan PLAN.md --arch ARCHITECTURE.md` runs every cross-referencing task-gate check (chunk coverage, dep cycles, skeleton ordering, layer tags, `[e2e@gate-N]`↔journey membership, PRODUCES→`[contract]`, gate preflight fields, crystallization adjacency, release gate, CONSUMES exact-match, wire-contract obligations); `brana-gate docs` scans for unresolved placeholders and **computes** WCAG contrast from DESIGN.md's tables — a contrast ratio is never an LLM's to compute. Where the tool is present its clean exit is the mandatory blocking half of the gate; the LLM pass shrinks to the judgment checklist (contradictions, open decisions, semantic serving). Copy-paste mode keeps the full LLM prompts as fallback. This applies Reality Rule 8 to the workflow itself: gate checks that are mechanical run as code, not as a cheap model's recall.
- **Release gate:** the v1 exit bar written as PLAN.md's final gate entry, with full demo-gate anatomy — journey (the kernel journey in a release build, unglamorous steps included), observations, runnability preconditions, and a serving chunk per step _through the production composition_. It gets a preflight and `GATE BLOCKED` semantics like any gate; discovering at the release gate that a kernel-journey step has no production-composition path is the failure this entry exists to move to Phase 3.

## Model Bindings

Tier language elsewhere in this doc stays for portability; these are the current concrete bindings. Default is all-Anthropic (agent mode); fallback column is for copy-paste runs in chat UIs.

| Step | Default (Anthropic) | Fallback (chat UI) |
| --- | --- | --- |
| P1 gap-check / interview | Haiku 4.5 / Sonnet 5 | Gemini Flash / Pro |
| P2 UX.md + PRD.md | Sonnet 5 | Gemini Pro |
| P2 ARCHITECTURE.md, P3 (all four docs), P7 impact analysis | Opus 4.8 | Gemini Pro |
| Consistency-gate + task-gate judgment passes (structural half is `tools/brana-gate`, zero tokens), doc sync, code map | Haiku 4.5 | Gemini Flash |
| 6a finding confirmation | Sonnet 5 | Gemini Pro |
| P4 task split, P5 implementation, 6a fixer | Sonnet 5 | Gemini Pro |
| P5 pure boilerplate | Haiku 4.5 | Gemini Flash |
| P5 escalation (failed twice) | Opus 4.8 | Gemini Pro |
| 6a reviewer | Opus 4.8 | Gemini Pro |
| 6b vision pass | Sonnet 5 | Gemini Pro |

6a review rule: a **different model than the implementer** reviews (Opus reviews Sonnet's code); cross-vendor review preferred when you're in chat UIs anyway — a different vendor catches more.

## Agent Adaptation Layer

Copy-paste is canon; this section translates it when the workflow runs inside agent tooling (Claude Code):

- **"Paste X" means the agent reads X.** Context packs in TASKS.md remain as hints and as the copy-paste fallback.
- **Reading roams, writing doesn't.** The agent may read any file in the repo (task-named files plus whatever it needs), but "only modify files listed in the task" stays a hard rule.
- **Sessions:** fresh conversation per phase; in Phase 5, one session per 2–3-task batch, cleared at each demo gate.
- **Gates are soft stops:** at a demo-gate task the agent preflights (build, launch, journey entry reachable — failure is `GATE BLOCKED`, fixed before the walk), then halts its turn, prints the journey script plus launch command, and waits; "continue" skips and logs `GATE SKIPPED`. At the consistency gate and the task gate the machine pass hard-blocks and the agent fixes its findings; the consistency gate's human read is advisory (SPEC.md + UX.md flagged).
- **Machine gates run script-first:** where `tools/brana-gate` is present (copy it into the repo at Task 0, or run it from the Brana checkout), the agent runs it and fixes its findings to a clean exit before the LLM judgment pass; the LLM pass covers only what the script can't parse.
- **Scope cuts are hard stops:** the agent states the cut and ends its turn. No default-proceed.
- **Phase 7:** the agent self-triages A/B/C/R, announces the route + one-line reason, and proceeds; you override by replying. The agent applies doc-sync corrections directly and creates `specs/NNN-name/` dirs itself.
- **Escalation counting:** "failed twice" = two failed attempts within the batch session; then the human switches the session to Opus.
- **Delegation passes paths, not prose.** A dispatched subagent gets file paths — its task's TASKS.md entry, CONVENTIONS.md, the contract sections it must obey — and reads them itself. Never pasted contents, never a re-narrated summary: everything pasted into a dispatch stays resident in the parent context for the rest of the session, and re-narration compresses lossily. Bulk subagent output (diffs, findings, review packages) is written to a file; only the path + a short gist returns.
- **Subagent reports:** ≤15 lines; status is one of `DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`; includes the evidence file path. `BLOCKED`/`NEEDS_CONTEXT` route to the ambiguity/scope-cut rules — never guessed past. The report is unverified claims until the parent checks suite, behavior, and TASKS.md mark.
- **Recovery after compaction or session flush:** rebuild state from git log + TASKS.md marks (SHAs live there), never from remembered conversation — re-running a completed task is the classic post-compaction failure.
- **Branch check is automatic:** the agent runs Git Rule 1's main/master check itself at the start of Phase 5, with no human prompt needed.
- **CI wiring:** when the repo has a remote, Task 0 adds a CI config that runs the verify script on push — the same command a human would run locally.
- **Parallel subagent delegation** is allowed only for tasks with disjoint file sets and no dependency edge between them; anything else runs sequentially in one session.

## External Design Inputs (optional)

Two kinds of pre-existing design input slot into the workflow as phase inputs — no extra phases. A design system replaces _generation_; reference apps ground _judgment_. Neither replaces UX.md: a design system is vocabulary, not sentences, and a fully themed component kit arranged badly is still a bad app.

### Pre-built design system (tokens/components already exist)

- **Phase 1:** design direction shrinks to one line — "Design system: X. Deltas: [any]."
- **Phase 3:** DESIGN.md becomes an **adoption map**, not an invention. The single source of truth moves into the system's own files (theme config, token package, Figma variables); DESIGN.md never restates a value — it refers by token name only. Contents: semantic role → system token mapping; component inventory (which existing component serves which UX.md element); **gap list** — UX.md needs the system can't serve, flagged for your approval before anyone invents a substitute; usage rules.
- **Consistency gate:** extra check — every token/component name DESIGN.md cites must exist in the actual system files.
- **Phase 5:** Task 0 installs the system. UI task context packs paste the relevant component signatures/docs instead of DESIGN.md prose. Conventions rule: system component before custom — hand-rolling what the system provides is a review finding.
- **Phase 6a:** add violation category: bypassed the system.

### Reference apps (learn from existing apps' look/UX)

Agents cannot open a reference app; "make it like X" from text yields a fuzzy training-data imitation. References only work as **screenshots + annotations**.

- **Reference pack (build once):** a `references/` dir of screenshots of the specific screens/states you admire, each with a one-line annotation naming _what to take_ ("this sidebar's density", "how progress rows read", "empty-state tone"). The annotation is load-bearing — unannotated, the model copies the wrong thing.
- **Phase 2 (UX.md):** paste the pack into the UX prompt — "adapt these _patterns_ (navigation structure, disclosure, information density) to my features; do not clone layouts." Highest-leverage insertion point: references shape the floor plan, not the paint.
- **Phase 3 (DESIGN.md):** vision pass first — "extract the observable style facts from these screenshots: palette roles, type scale, spacing rhythm, radius language." You approve the extraction before it feeds token generation; catching a wrong reading here beats discovering it in the contract.
- **Phase 6b:** put the reference screenshot next to your app's screenshot at every gate. Comparative judgment ("mine vs. the reference, side by side") is easier and more honest than absolute judgment.
- **Boundary rule:** adapt patterns and quality bar, never clone trade dress — the product must be recognizable as itself.

---

## Phase 1 — SPEC.md + Scope Challenge

**Model:** You (human) + Haiku / Gemini Flash for Q&A gap-checking. Optionally a strong model in interview mode.
**Inputs:** Your idea.
**Output:** `SPEC.md` (kernel-first, ranked)

**Scope decomposition first:** an idea spanning multiple independent subsystems ("a platform with chat, billing, and analytics") is decomposed into sub-products before any detail questions — each gets its own `specs/NNN-name/` cycle; spec the first one now. Don't spend questions refining a project that needs splitting.

Write the rough spec yourself — cheapest possible start. Then run one gap-check:

```
I'm drafting a spec for [app]. Here's what I have so far: [paste SPEC.md draft].
List anything ambiguous or missing that a developer would need to know.
Do not rewrite the spec. Do not design or implement anything.
```

Alternative (interview mode, if starting from nothing):

```
You are a senior product manager. I want to build [one-paragraph app
description]. Interview me until every important requirement is clear.
First ask what I'm already considering, before offering ideas of your
own. Do not make assumptions. Ask questions one by one. Challenge vague
requirements. Suggest simpler alternatives. When finished, produce
SPEC.md: core features & user stories, edge cases, suggested tech stack,
UI/UX guidelines. Do not proceed to architecture.
```

The ask-first line is load-bearing: it surfaces hidden context and prevents the user fixating on the model's framing. In agent mode, interview questions use the blocking question tool (AskUserQuestion) with multiple-choice options when 2–4 genuinely distinct options exist; open-ended when they don't.

**Approaches (when multiple plausible directions remain):** propose 2–3 concrete approaches — for each, a 2–3-sentence description, pros/cons, key risks. Present all options **before** naming a recommendation — recommending first anchors the user. Drop or sharpen any approach generic enough to appear in a listicle for this problem category. One clearly-best direction → state it, skip the menu.

```
Here is what we know so far: [paste notes/draft]. Propose 2–3 concrete
approaches to this product: each with a 2–3 sentence description, pros,
cons, key risks. Present all options first; only then name your
recommendation and why. Drop any approach generic enough to appear in a
listicle for this problem category. Do not write the spec.
```

**Scope challenge (required — skipping this pass is how ten shallow features beat four good ones):**

```
Here is my spec: [paste]. You are a ruthless product owner.
1. State this product's core promise in one sentence.
2. Identify the KERNEL: the 3–5 features without which the product is
   pointless. Everything else goes to a ranked v1.1+ backlog.
3. Write the KERNEL JOURNEY: one end-to-end user story, step by step,
   that exercises every kernel feature ("create an item → see the
   result → close app → reopen → the item is still there").
4. Flag any spec'd feature that undermines the core promise if built
   shallowly — those are kernel or cut, never "shallow v1".
Do not add features. Do not design.
```

Fold the result back into SPEC.md: **Kernel** (with the kernel journey verbatim), **v1**, **Backlog**. The kernel journey is the walking-skeleton target (Phase 5) and the standing demo-gate script (Phase 6b). Convenience features (scheduling, power-user overrides, localization, theming and their kin) are backlog by default — they enter v1 only by your explicit call.

**Integration check (before writing SPEC.md):** combine the answers gathered so far and surface non-obvious consequences no single question covered ("X plus Y together means Z is lost on restart") — one open probe per genuine combination effect. An answer revealing genuine uncertainty is recorded as an explicit assumption in SPEC.md, never silently resolved.

**Design direction (required, 3–5 lines):** product personality as 3 adjectives, 2–3 reference apps whose look is the target, platform density, accessibility floor (WCAG AA). Feeds UX.md and DESIGN.md. If you have a pre-built design system or a reference pack, name them here instead — see External Design Inputs.

Keep SPEC.md under 500 words plus the kernel section. Write it with frontmatter `status: draft`.

**Spec self-review (after writing, before handing over):** re-read the file fresh — (1) placeholders/TBDs, (2) internal contradictions, (3) scope: fits one cycle or needs decomposition, (4) ambiguity: any requirement readable two ways → pick one and make it explicit. Fix inline, then ask the human to read it. Catches at zero cost what the Phase 3 consistency gate would catch two phases later.

---

## Phase 2 — UX.md + PRD.md + ARCHITECTURE.md

**Model:** Strong general model for UX and PRD; Opus-tier for ARCHITECTURE. Fresh session each, in this order: UX → PRD → ARCHITECTURE (screens inform requirements; both inform architecture).
**Inputs:** `SPEC.md`.
**Outputs:** `UX.md`, `PRD.md`, `ARCHITECTURE.md`

### UX.md — the missing artifact

Without this document, implementers get tokens and adjectives but no screens — every task improvises its own interface, and the result is incoherent. UX.md is the floor plan that DESIGN.md later paints. Component hierarchies and token sheets do not substitute for it.

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
[paste SPEC.md; if you have a reference pack, paste the annotated
screenshots with: "adapt these patterns — navigation structure,
disclosure, information density — to my features; do not clone layouts"]
```

**Read it and walk the flows yourself before proceeding.** If a step feels wrong to _you_ on paper, it will be wrong in the app. This is the cheapest moment to fix UX; iterate here, in prose, not in Phase 7.

### PRD.md

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
[paste SPEC.md + UX.md]
```

### ARCHITECTURE.md

```
Act as a principal software architect. Read the PRD and UX below. Produce
ARCHITECTURE.md: system overview, module responsibilities and boundaries,
data model / DB schema (DDL with indices and constraints), API contract
(endpoints, request/response shapes, status codes, errors, auth),
component hierarchy mapped to UX.md screen ids, dependency graph, error
handling strategy, configuration strategy, and an empty **Decision log**
section at the end of the file — append-only, one line per future
decision as `YYYY-MM-DD — decision — why`; Phase 7 doc sync and Route C
patches append to it, never delete an earlier entry's why.
Rules: COMMIT to one concrete stack and one design per decision — no
"e.g. X or Y", no alternatives left open. Name the e2e/journey-test
harness as part of the stack commitment — CONVENTIONS.md's Test
strategy (Phase 3) and every gate's crystallization task (Phase 4)
build on this name. Every UX.md flow must be
traceable through the contract: for each kernel-journey step, name the
API call or event that serves it; if a step has no serving contract
(e.g. "reopen app → data restored" needs a list/read endpoint), add it.
When the kernel journey or a v1 flow depends on an EXTERNAL SYSTEM (a
paid API, third-party service — anything that will be faked in tests),
give that integration a versioned WIRE CONTRACT section: exact
request/response shapes, auth, error semantics — precise enough that a
fake can be validated against it. Extend traceability to those steps:
each names its wire contract. No external system → omit the section.
Do not write implementation code. Output Markdown only.
[paste PRD.md + UX.md]
```

That traceability rule is load-bearing: a contract can silently lack the read/list operation a journey step depends on, and nothing downstream will ever notice — implementers build only what the contract names. The wire-contract rule is the same failure at the external boundary: without it, the fake's convenience shape becomes the de-facto contract, every test passes against it, and the first real request is built at release time.

PRD.md is written with frontmatter `status: draft` (UX.md and ARCHITECTURE.md are living docs — no stamps).

---

## Phase 3 — PLAN.md + CONVENTIONS.md + DESIGN.md + FILE_STRUCTURE.md, then the Consistency Gate

**Model:** Opus-tier. Fresh session. Opus does not implement after this.
**Inputs:** `PRD.md`, `ARCHITECTURE.md`, `UX.md` (+ SPEC design direction)
**Outputs:** `PLAN.md`, `CONVENTIONS.md`, `DESIGN.md`, `FILE_STRUCTURE.md`

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
   style, commit style, and **Test strategy**: which layer
   (`[unit]`/`[integration]`/`[contract]`/`[e2e@gate-N]`) verifies which
   criterion type, the frameworks for each, the e2e/journey-test harness
   named in ARCHITECTURE.md, and the verify command. Keep it under 2
   pages: every line here is a line of context each future task pays
   for. **Lint-over-prose rule:** a convention a machine can check
   becomes a lint rule at Task 0; prose is only for what lint can't see.
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
   exist this cycle. A per-cycle artifact written to
   `specs/NNN-name/`: a prediction for the planner and Task 0, archived
   after — never a living doc. The repo tree and code map are the
   living truth once code exists.

Output the four files completely. No conversational text.
[paste PRD.md + ARCHITECTURE.md + UX.md + design direction]
```

With a pre-built design system, item 3 switches to adoption-map mode (see External Design Inputs): paste the system's token/component files and ask for the mapping, inventory, and gap list instead of new tokens. With a reference pack, run the style-extraction vision pass first and approve it before this prompt.

### Consistency Gate (blocks Phase 4)

Generated contracts routinely ship with the same fact stated two different ways, unfilled template placeholders, and decisions left open — proof nobody read them. Agents don't halt on contradictions; they pick a clause arbitrarily, per file. Two checks, both cheap:

1. **Machine pass** — script-first in agent mode: run `brana-gate docs` over all eight docs (unresolved placeholders; every DESIGN.md contrast ratio computed, stated-vs-computed mismatches flagged) and fix to a clean exit; then the LLM pass (Haiku/Flash tier) covers the judgment remainder — contradictions, open decisions, unserved flow steps, gate/composition checks. Copy-paste mode: the full prompt below is the whole pass.

```
Here are this project's contract docs: [paste SPEC, UX, PRD, ARCHITECTURE,
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
If a pre-built design system is attached, also list every token or
component name DESIGN.md cites that does not exist in the system files.
Report only findings with doc + quote. No rewrites.
```

The machine pass is mandatory and blocking; in agent mode the agent applies fixes for its own findings before proceeding.

2. **Human pass (advisory):** read SPEC.md and UX.md at minimum — they encode intent, which no machine check can verify; wrong-but-consistent docs pass every machine pass. Reading the rest end to end is recommended, not blocking. In agent mode the agent presents the machine findings plus per-doc summaries and reminds you; "continue" proceeds.

No task is written until the machine pass is clean. A clean machine pass flips the `status:` stamp on SPEC.md, PRD.md, and PLAN.md from `draft` to `gate-passed`. Mechanical contradictions found later mean the machine pass was skipped; intent failures found later are the residual risk of an unread SPEC/UX.

---

## Phase 4 — TASKS.md

**Model:** Sonnet-tier. Fresh session. Refuse a PLAN.md still stamped `status: draft` — the consistency gate hasn't cleared; point back to Phase 3.
**Inputs:** `PLAN.md`, `ARCHITECTURE.md`, `UX.md`, `PRD.md` (error/edge-case list)
**Output:** `TASKS.md`

```
Split PLAN.md into small, isolated, sequential implementation tasks.
Each task: id, title, objective, inputs, outputs, dependencies (task
ids), files to create/modify, acceptance criteria, estimated difficulty,
an interfaces block, and a context pack (exact files to paste + the
ARCHITECTURE.md sections to obey; UI tasks also name their UX.md screen
ids and get DESIGN.md).
The interfaces block has two parts, quoted from ARCHITECTURE.md:
CONSUMES — the exact signatures, payload shapes, or endpoints this task
uses from other tasks' output; PRODUCES — the exact signatures later
tasks may rely on. An isolated implementer must learn neighboring types
from this block, never by reading neighbor code. A task with a PRODUCES
block gets one additional acceptance criterion, tagged `[contract]`:
a test that calls the produced signature/endpoint exactly as specified
and asserts the shape — catching drift before a consumer task ever
reads it.
Rules:
- Acceptance criteria are observable behaviors in the running app or a
  test that drives one. "Compiles", "check passes", "renders" are gates,
  never the criterion. Tag every criterion with the layer that verifies
  it: `[unit]`, `[integration]`, `[contract]`, or `[e2e@gate-N]`. A
  `[e2e@gate-N]` criterion must appear as a step of gate N's journey —
  if it doesn't, add it there, not just here (the gate N task's journey
  as copied into TASKS.md is the amendable copy — PLAN.md is not
  re-edited here).
- Preserve PLAN.md's DEMO GATE entries as explicit tasks: journey to
  walk, observations required, a preflight block (exact build/launch
  command — a disposable/fixture path, fail-closed against
  non-disposable targets, when the journey would otherwise touch
  production state; seed/fixture command if the journey needs data;
  and the task ids whose output the journey walks — the gate depends
  on all of them), the human's walkthrough result as the completion artifact
  (screenshots optional). A journey step with no implementing task
  before the gate is a blocking finding — reorder or add the wiring
  task; never emit a gate that isn't walkable at its position. Every
  gate launch command is the production entry point with disposable
  inputs (same-composition rule) — a bespoke gate-only composition is
  the same blocking finding. PLAN.md's RELEASE GATE becomes a gate
  task too, same anatomy: its journey is the kernel journey in a
  release build, each step traced to a task exercised through the
  production composition, the production-composition proof task among
  its dependencies. A
  skipped gate is marked GATE SKIPPED on the task, never deleted. Append
  one unglamorous step to every gate journey, drawn from PRD.md's
  error/edge-case list, rotating across gates: restart → offline →
  invalid input → restart → ... — a gate never ships checking only the
  happy path.
- Every DEMO GATE task is immediately followed by a **crystallization
  task**: it encodes the gate's scripted journey (including its
  unglamorous step) as an automated e2e test on the harness named in
  CONVENTIONS.md's Test strategy; the new test joins the journey suite.
  No feature task may start before its preceding gate's crystallization
  task is done. A `GATE SKIPPED` gate does NOT defer the encoding —
  writing the e2e needs only the scripted journey, not a walkthrough:
  the crystallization task runs immediately and its test is marked
  `UNWITNESSED` (same visible-debt mark as the gate) until the journey
  is eventually walked, at latest the v1 exit bar. Feature work
  proceeds once the unwitnessed test is green — a skip costs human
  attention debt, never automation debt.
- Verified-fake rule (only when ARCHITECTURE.md has wire contracts):
  a task producing a fake of an external system gets a `[contract]`
  criterion running ONE shared suite against both the fake and the
  real adapter, asserting the wire contract — the fake must reject
  what the contract rejects. The real-adapter side is offline
  (request-shape assertions, recorded fixtures); live provider calls
  happen only in a bounded canary task routed through the production
  composition.
- The walking-skeleton milestone tasks come first and may not be
  reordered after feature tasks.
- Tasks tiny: ~50–300 lines of code, one prompt each.
Output TASKS.md as a numbered list. Do not write any code.
[paste PLAN.md + UX.md flow section + PRD.md error/edge-case list]
```

**Task schema (agent mode):** each task is a heading plus one fenced ```toml block — `id`, `type` (scaffold/feature/gate/crystallization/fix/proof/spike), `chunk`, `deps`, `files`, `consumes`/`produces` (exact quotes), `skeleton`, `fake_of`, `[[criteria]]` (text + layer, `gate` on e2e), and for gate tasks a `[gate]` table (`n`, `release`, `launch`, `seed`, `unglamorous`, `[[gate.journey]]` step + serving task id); full schema in `tools/brana-gate --help`. The format exists so the task gate's structural half runs as a program, not as a model's recall; prose around the blocks stays free-form.

Write TASKS.md with frontmatter `status: draft` — the task gate below flips it. Context packs are predictions made before code exists — treat them as hints. At implementation time paste what actually exists. Interfaces blocks are firmer than packs: they quote the contract, and contract changes route through the docs, not through a task improvising. Isolation is for token budgets, not for truth: the demo gates exist precisely because bugs live in the seams between well-tested tasks.

### Task Gate (blocks Phase 5)

The consistency gate checks Phase 3's output; without this gate, Phase 4's output is self-certified — the splitter stamps its own TASKS.md and the first integrity check is a gate preflight *during* implementation, the most expensive moment to learn a journey step has no serving task. Every check below is cross-referencing, not judgment; machine pass only — intent was already checked at the consistency gate, and TASKS.md is a mechanical derivation of PLAN.md.

**Machine pass** — script-first in agent mode: `brana-gate tasks TASKS.md --plan PLAN.md --arch ARCHITECTURE.md` covers every structural check in the list below; fix to a clean exit, then the LLM pass (Haiku/Flash tier, fresh session) covers only the judgment remainder — is a journey step *semantically* served by the task that claims it, does a criterion actually restate its PLAN.md requirement. Copy-paste mode: the full prompt below is the whole pass.

```
Here are TASKS.md, PLAN.md, and ARCHITECTURE.md's interface and wire-
contract sections: [paste]. Findings in TASKS.md only — list:
- every PLAN.md chunk with no task implementing it, and every task
  serving no chunk;
- every dependency cycle, and every walking-skeleton task ordered
  after a feature task;
- every gate-task journey step with no implementing task earlier in
  the order, and every such serving task missing from the gate's
  dependency ids;
- every CONSUMES quote with no earlier task whose PRODUCES matches it
  and no ARCHITECTURE.md section stating it;
- every acceptance criterion missing its layer tag; every
  `[e2e@gate-N]` criterion absent from gate N's journey; every task
  with a PRODUCES block missing its `[contract]` criterion;
- every gate task missing a preflight field (launch command; seed/
  fixture command when the journey needs data; dependency ids) or not
  immediately followed by its crystallization task; every gate journey
  missing its unglamorous step;
- a missing RELEASE GATE task; and — when ARCHITECTURE.md has wire
  contracts — a production-composition proof absent from the release
  gate's dependencies, plus every fake-producing task missing its
  shared-suite `[contract]` criterion.
Report only findings with task id + quote. No rewrites.
```

The machine pass is mandatory and blocking; in agent mode the agent applies fixes for its own findings before proceeding. A clean pass flips TASKS.md `status: draft` → `ready` (Phase 5 refuses a draft TASKS.md). A gate that is unwalkable on paper here is the same gate that would go `GATE BLOCKED` mid-implementation — this pass moves that discovery to the cheapest possible moment.

---

## Phase 5 — Implementation

**Model:** Sonnet-tier; one session per 2–3-task batch, cleared at each demo gate (copy-paste mode: fresh session per task). Haiku/Flash for pure boilerplate. Opus only as escalation when Sonnet fails twice.
**Inputs per task:** the task + `CONVENTIONS.md` + only the files it touches (copy-paste mode; agent mode reads freely, writes only task-listed files). UI tasks additionally get `DESIGN.md` and their UX.md screen section; backend tasks get neither.
**Outputs:** source + tests per task, demonstrated.

Refuse a TASKS.md not stamped `status: ready` — the task gate hasn't cleared; point back to Phase 4. **Step 0, before Task 0:** check the current branch (Git Rule 1) — on main/master, create the cycle branch (named after the spec dir) before any code; direct-to-main only when the human explicitly says so. Task 0 is always the scaffold: file tree from FILE_STRUCTURE.md, configs, data migrations (if any), no feature logic; its smoke test is the app booting via a documented run command, recorded in CONVENTIONS.md. Then the walking skeleton — the kernel journey passes in the real app before any feature deepening begins.

**Migration tasks:** a task that adds or alters a schema migration must apply-rollback-reapply against fixture data — up, then down, then up again — with an assertion that the fixture data present before the up survives the round trip (not just that each step exits zero). Rollback in this workflow always means running the down migration, never `git revert` (Git Rule 2) — a reverted commit leaves the schema changed underneath a codebase that no longer expects it.

Per-task prompt:

```
Implement Task N of TASKS.md.
Task spec: [paste task].
Conventions: [paste CONVENTIONS.md].
Current relevant files: [paste ONLY the files this task touches].

Rules:
- Only modify files listed in the task.
- Follow ARCHITECTURE.md contracts and CONVENTIONS.md exactly.
- UI task: follow DESIGN.md (tokens only, no raw values) and match the
  UX.md screen section pasted — regions, hierarchy, and all states
  (hover, focus, disabled; empty, loading, error), not just the happy
  path.
- Write the implementation plus unit tests covering the acceptance
  criteria, at the layer(s) tagged on each criterion. The full existing
  suite must still pass.
- Migration task: run up, then down, then up again against fixture
  data; assert the pre-up fixture data is intact after the round trip.
- Output complete files with exact paths. No placeholders, no TODOs,
  no truncation. No refactoring unrelated code, no future tasks.
- Ambiguity rule: if the ambiguity is internal (naming, private
  structure), choose the simplest interpretation and note it in a
  comment. If resolving it would CHANGE OR DROP USER-VISIBLE BEHAVIOR
  the spec implies, STOP and output the question instead of code.
```

That last rule exists because a blanket "choose the simplest interpretation — do not ask" turns silent feature cuts into code comments instead of alarms.

**Completing a task:** run the **verify script** (Verification Machinery) _and_ its acceptance behavior. UI tasks: launch-and-look + screenshot only if the human asked for it (per task or in CONVENTIONS.md) — otherwise visual quality waits for the demo gate. Then commit, capture the **evidence file** at `specs/NNN-name/evidence/task-N.txt` (the exercised command — verify script, test, or journey step — plus the last ~30 lines of its output), and mark the task done in TASKS.md with the commit SHA plus the evidence file's path. Evidence is captured live — it is not reconstructable from the diff afterward, and a done-mark without it doesn't pass the demo gate or the v1 exit bar. Marking Done on green tests alone is the classic failure — don't reintroduce it.

Escalation prompt (only when stuck twice):

```
Sonnet has failed this task twice. Task spec: [paste]. Current code:
[paste]. Failing output: [paste]. Attempts: [summarize]. Diagnose the
root cause, then either provide corrected code or, if the plan itself is
wrong, rewrite the affected PLAN.md section.
```

**Stale-plan rule:** any mid-cycle PLAN.md section rewrite — an escalation verdict, a spawn-route patch, a human edit — flips PLAN.md's stamp back to `draft` and TASKS.md's with it, until a scoped re-gate is clean: the consistency-gate checks re-run on the patched section, the task gate (`brana-gate tasks`) re-runs on every task serving the patched chunk, and affected tasks/gate journeys are updated — all before the next implementation session. A plan edited mid-flight without re-gating is the same self-certification seam the task gate exists to close. (Contract patches additionally trigger the stale-interface-block rule, Phase 7.)

Run/verify each task yourself; fix env issues manually (don't burn tokens on `npm install` problems).

---

## Phase 6 — Review: Code (6a) + Product (6b)

Code review alone lets everything a compiler can't see — bad flows, bad layouts, integration bugs — ship unexamined. 6b is the half most workflows are missing.

### 6a — Code review

**Model:** a different model than the implementer — default Opus 4.8 reviewing Sonnet's code; cross-vendor when running in chat UIs anyway (a different vendor catches more). After every 2–3 tasks, on diffs only.
**Inputs:** diff + relevant ARCHITECTURE.md section + CONVENTIONS.md + the reviewed tasks' acceptance criteria from TASKS.md (+ DESIGN.md and UX.md screen section when the diff touches UI).

**Precondition:** lint and typecheck must be green before a 6a review starts — a finding a linter could catch is a lint-config gap, not a review finding; fix the config, not the code, and re-run.

**Reviewer independence:** the reviewer gets the diff and the contracts — never the implementer's report, self-review, or rationale; those are unverified claims that anchor the review. Never pre-judge the review ("do not flag X", "at most low severity") — a stated rationale never downgrades a finding. Findings that conflict with the plan itself escalate to the human ("which governs?"), never get silently resolved either way.

```
Review this diff against the attached contracts and acceptance criteria.
Report only:
(1) bugs/logic errors, (2) security issues, (3) race conditions,
(4) contract violations, (5) convention violations, (6) UI-only: design
contract violations (raw values where tokens exist, missing states,
contrast/focus failures) and UX contract violations (screen structure or
flow steps that diverge from UX.md), (7) test adequacy: an acceptance
criterion with no test at its declared layer, a test that asserts
nothing meaningful (runs without checking the outcome), or a test that
mocks away the exact behavior the criterion requires, (8) composition
and fake integrity: a runtime or gate path that composes bespoke
wiring instead of the production entry point with injected seams, or a
fake of an external system that diverges from its wire contract
(accepts what the contract rejects, or lacks the shared contract
suite). Each finding:
file:line, severity, one-line fix. Objective checks only — no style
opinions, no praise, no rewrites.
[paste diff + contract sections + acceptance criteria]
```

**Findings are unverified claims.** Before findings become fix tasks, a confirmation pass (fixer-tier model) runs: a bug, logic error, or race condition gets a reproduction — a failing test or concrete repro steps; a contract, convention, or design violation gets both sides quoted (code line + contract line). A finding that fails confirmation escalates to the human with the failed-confirmation note — never silently dropped, never blindly fixed; an LLM reviewer's false positive turned into a fix task is churn plus regression risk. The reproduction test lands with the fix and joins the suite.

Write findings to `specs/NNN-name/reviews/REVIEW_N.md` with each finding's confirmation status. Each confirmed finding becomes a TASKS.md fix task quoting file:line and referencing the review file's path — findings are never fixed off the review output directly.

**Compound rule:** when the same specific rule or pattern — not the same numbered category — repeats a second time in one review cycle, its fix task also adds a CONVENTIONS.md line or a lint rule closing that class — the same class never needs a reviewer's eyes again.

Fixer prompt (feed findings back to the implementation model):

```
A senior engineer reviewed your code; these findings are confirmed with
reproductions: [paste confirmed findings + repros]. Apply these fixes;
each repro test must now pass and join the suite. All existing tests
must still pass. Output only the changed files.
```

### 6b — Product review (the demo gate)

**Model:** you, plus the running app. Zero tokens for the walkthrough itself. Cadence: every demo-gate task (every 2–3 tasks), and always before a feature branch merges.

Preflight first (agent): before the soft stop, the agent runs the **verify script**, builds, launches via the gate task's preflight block (launch command + seed data), and confirms the journey's entry point is reachable. Preflight fails → `GATE BLOCKED` on the task (a defect, not a choice — distinct from `GATE SKIPPED`), breakage becomes fix tasks at the head of the queue, preflight re-runs after they land; you are only invited to walk an app that provably runs.

Soft stop: in agent mode the agent halts at the gate task, prints the journey script plus its launch command, and waits for your walkthrough result (screenshots optional but recommended — cheap context for fixes). "Continue" skips the gate — logged as `GATE SKIPPED` on the task and surfaced at the v1 exit bar.

1. Launch the app with the gate's launch command (the agent's preflight has already proven it boots).
2. Walk the scripted journey from the gate task (kernel journey at minimum, once it exists).
3. Check each step against its falsifiable criterion — did the observable thing happen?
4. Optional: screenshot screens touched (archive under `specs/NNN-name/screenshots/`) — they make fix prompts and the vision pass possible, but the walkthrough result alone passes the gate.
5. Judge the screens against UX.md (structure) and DESIGN.md (styling) — and against your own eyes. If you have a reference pack, put the reference screenshot next to yours; comparative judgment beats absolute judgment. "Passes contracts but looks wrong" is a valid finding; contracts are floors, not ceilings.
6. Every finding becomes a task at the head of the queue. Feature work does not resume past a failed gate.

Optional token-assisted pass — paste screenshots to a vision-capable model:

```
Here are screenshots of the app and the UX.md + DESIGN.md contracts:
[paste]. Report divergences from the contracts and the three changes
that would most improve clarity and hierarchy. Findings only.
```

**v1 exit bar:** the exit bar is the **release gate** task (Verification Machinery) and runs like any gate — the agent preflights it (verify script, release build, launch via the production entry point, journey entry reachable; failure is `GATE BLOCKED`, fix tasks first). The bar: the kernel journey passes end-to-end in a release build through the production composition, witnessed by you, including the unglamorous steps (restart, offline, error paths named in the PRD), _and_ the kernel journey's crystallization-task e2e test is green in the release build, _and_ — when fakes stood in for an external system — the production-composition proof task and the verified-fake contract suites are Done/green. Every `GATE SKIPPED` entry in TASKS.md is listed here with its `UNWITNESSED` journey test, and each is either walked now or explicitly accepted (the automation exists — the missing human witness is the recorded, accepted debt); an unresolved `GATE BLOCKED` fails the bar outright — a gate that never became runnable is a defect, not debt. Every crystallization task across every gate must be Done — a gate walked but never crystallized is an untested journey by the next change. "All tasks Done" is not the bar; this is.

**Spawn route (pre-v1):** when fixing a `GATE BLOCKED` — any gate, including the release gate — reveals a missing subsystem or a new/changed contract (more than a few fix tasks, or a new ARCHITECTURE.md section), do not wedge it into the current TASKS.md: spawn a scoped child cycle in a new `specs/NNN-name/` dir (Phase 1→6 on the delta, Route C shape, ARCHITECTURE.md patched not regenerated). The parent gate stays `GATE BLOCKED` referencing the child spec; the stale-interface-block rule (Phase 7) and the stale-plan rule (Phase 5) run on the parent's not-done tasks and patched PLAN.md sections; the parent preflight re-runs only after the child cycle completes.

---

## Phase 7 — Change Loop (post-v1)

Every change enters through triage, routed by size. Living docs stay accurate (see Doc sync) or every future impact analysis is poisoned.

### Triage

Who routes: in agent mode the agent self-triages, announces the chosen route + one-line reason, and proceeds; you override by replying. In copy-paste mode you route. Wrong-way-cheap mistakes are caught by the escalation rules below.

| Route                 | Change type                                                      | Path                                                                                                                                                                                                                    |
| --------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **A — trivial**       | Bugfix, copy change, config tweak                                | Short-lived branch (Git Rule 3, human may waive per instance) → hand-write one task → Phase 5 → verify (incl. journey suite) green before merge. No doc updates unless a behavior contract changed. Styling still obeys DESIGN.md tokens. |
| **B — small feature** | Fits existing architecture, no schema/API/module-boundary change | Mini-spec → impact analysis → Phase 4 on the delta → Phase 5/6 (incl. 6b).                                                                                                                                              |
| **C — big feature**   | New module, schema migration, new integration                    | Full Phase 1→6 scoped to the delta: new `specs/NNN-name/` dir; Opus patches ARCHITECTURE.md/UX.md, never regenerates.                                                                                                    |
| **R — refactor**      | Refactor, dependency upgrade, debt paydown; no user-visible behavior change intended | Feature branch → verify + journey suite green BEFORE, as baseline → chunked tasks (~300-line cap, one green commit each) → verify green after each chunk → 6a on the full diff → doc sync (append Decision log entry if a boundary moved) → 6b only if UI touched → merge. |

No verify script / journey suite yet (pre-v1.1 app, or all gates were skipped) → Route R's and Route A's baseline preconditions are unsatisfiable as written; the route's first task is the backfill: create the verify script and crystallize the kernel journey, before any chunked/behavior work starts.

**Escalation rules:**

- Any change that mid-flight touches a schema/API/module boundary stops and re-enters as Route C. (Pre-v1, the same discovery inside a blocked gate routes through the Spawn route in Phase 6b.)
- Any change that mid-flight would drop or degrade user-visible behavior stops for your decision — same stop-the-line rule as Phase 5. This stays a hard stop in every medium. Route R additionally freezes on ANY user-visible change discovered mid-flight, not just a drop — a refactor that changes behavior isn't a refactor; same hard stop.
- **Stale-interface-block rule:** any mid-cycle contract patch (CONSUMES/PRODUCES section of ARCHITECTURE.md changes) triggers a cheap pass that diffs old vs. new contract and updates the CONSUMES/PRODUCES blocks of every not-done TASKS.md task quoting the changed section — before the next implementation session starts. An implementer working from a stale interfaces block is the seam-bug failure mode rule 8 exists to close.
- **Stale-plan rule (Phase 5) applies here too:** a mid-cycle PLAN.md section rewrite reverts PLAN.md and TASKS.md to `draft` until the scoped re-gate (consistency checks on the patched section, task gate on the tasks serving the patched chunk) is clean.

**Review policy:** Routes B/C get one 6a review of the full feature diff plus one 6b walkthrough before merge. Route A gets 6a only if it touches logic, auth, or data handling. Route R gets one 6a review of the full diff always (6a category 7 — test adequacy — matters most on a refactor) and 6b only if the diff touched UI.

**Redesigns:** a visual/UX rework is driven by observed failures — your usage notes and screenshots of what is bad and why — feeding a UX.md patch first. Re-specifying tokens and animation parameters without touching UX.md repaints the same wrong rooms.

### Spec directory convention

```
specs/
  001-core/        SPEC.md PRD.md PLAN.md TASKS.md FILE_STRUCTURE.md
                   evidence/ reviews/ screenshots/   (v1, Route C scale)
  002-reminders/   SPEC.md PLAN.md TASKS.md FILE_STRUCTURE.md
                   evidence/ reviews/                (Route C)
  003-dark-mode/   SPEC.md TASKS.md evidence/         (Route B mini-spec)
ARCHITECTURE.md    (single, patched per change; ends in an append-only Decision log)
UX.md              (single, patched per change)
CONVENTIONS.md     (single, patched per change)
DESIGN.md          (single, patched per change)
```

`specs/` is append-only history. Living docs in root are current truth — patched, never contradicted by a side ledger. `FILE_STRUCTURE.md` lives per-cycle under each `specs/NNN-name/` — it's a prediction, archived with its cycle, never a root doc.

### Mini-spec (Route B)

5–15 lines, hand-written: what, why, falsifiable acceptance criteria, out-of-scope.

### Impact analysis (Routes B and C)

**Model:** Opus-tier. Fresh session.

```
Here are ARCHITECTURE.md, UX.md, and a feature request: [paste].
Answer only: (1) does this fit the existing architecture, or does a
module boundary/schema/API contract need to change? (2) which screens/
flows in UX.md does it touch or add? (3) which existing files are
affected? (4) which doc sections need edits (quote them)?
Do not write code or a plan.
```

"Fits" → Route B continues; stamp the mini-spec `status: gate-passed` (impact analysis is Route B's gate). "Needs change" → Route C; the quoted sections are patched before any tasks are written.

### Doc sync (after every merged feature)

**Model:** Haiku/Flash tier. Stale docs are the failure mode that kills this workflow at scale.

```
Here are ARCHITECTURE.md / UX.md / DESIGN.md and the diff of the last
feature: [paste]. List every statement in the docs now false, with the
correction (include new screens, tokens, or components the feature
added that the docs don't list). If a module boundary moved or a
non-obvious decision was made, also draft one Decision log line:
`YYYY-MM-DD — decision — why`. Output only the corrections and the log
line.
```

Apply corrections to the source docs directly — the agent applies them itself in agent mode; you apply them in copy-paste mode. Never record divergence as a "deviations" appendix or a gotchas list; amend the statement that became false. Append the drafted line to ARCHITECTURE.md's Decision log — append-only, a patch never deletes an earlier entry's why. FILE_STRUCTURE.md is out of scope here — it's per-cycle, archived with its `specs/NNN-name/` dir, never corrected in place. Cheap, mechanical, non-optional.

### Scaling note: context selection

"Paste only files the task touches" works at 20 files, fails at 200. When the task splitter starts guessing context packs wrong, feed it a code map first — one-paragraph summary per module, regenerated by a cheap model after each Route C change.
