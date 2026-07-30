# Changelog

## 2.0.0 — 2026-07-30

Ground-up token-efficiency redesign. Two independent audits of v1.12
(`docs/2026-07-30-brana-workflow-audit.md`, `ANALYSIS-brana-vs-superpowers.md`)
converged on the same root causes: nine planning artifacts re-expressing the
same facts (~3–4× the planning words of comparable workflows, ~12–15× the
document traffic), 45% instruction duplication between WORKFLOW.md and the
skills, a monotonic safety ratchet across twelve versions, front-loaded
assurance, gate/crystallization machinery dominating execution cost, and
mandated session flushes defeating prompt caching. Before/after verification:
`docs/2026-07-30-v2-review.md`; pre-fix numbers: `docs/2026-07-30-v2-baseline-metrics.md`.

- **One canonical plan.** `specs/NNN-name/PLAN.md` replaces SPEC + UX + PRD +
  ARCHITECTURE(per-cycle) + PLAN + TASKS + FILE_STRUCTURE. Eight top-loaded
  sections, stable R-/U-/KJ-IDs, contracts stated once. Living root docs are
  conditional and compact (CONVENTIONS ≤1 page; ARCHITECTURE only for mature
  multi-cycle systems, history in `docs/adr/`; DESIGN only with the UI module).
- **Risk modules replace full/lite.** Money, external system, migration,
  UI-heavy, auth/user data, operator surface, deployment — each activates its
  own planning section, verification, and review depth. No binary profile, no
  retro-lite valve, no delivery-contract vocabulary.
- **Gates rebuilt around cost.** Walking skeleton first (U1), one kernel e2e
  written once when the skeleton lands, and one mandatory human walkthrough
  that closes the spec. Scheduled mid gates, per-gate crystallization,
  coverage citations, evidence files, GATE BLOCKED/SKIPPED/UNWITNESSED
  bookkeeping, and status stamps are removed; mid gates are pull-based
  ("show me" + async slice screenshots).
- **Consistency gate and task gate deleted.** Replaced by an inline plan
  self-review (coverage, placeholders, cross-unit consistency) plus
  `brana-gate docs`; independent architecture review triggers only from the
  money/external/migration/auth modules.
- **Cache-friendly execution.** One persistent controller session per cycle;
  subagents get path-based packets and never read the whole plan; no
  per-phase or per-batch fresh-session mandates. Progress lives in
  `.brana/ledger.md`, never in the plan and never as bookkeeping commits.
- **Skills collapsed 7 → 3 thin routers** (`brana-plan`, `brana-build`,
  `brana-ship`) that sequence WORKFLOW.md instead of restating it; the five
  bundled `brana_gate.py` copies are removed (single copy in `tools/`).
- **Dependency approval tiered.** Routine policy-compliant packages resolve at
  implementation and are reported; strategic picks (frameworks, paid services,
  native deps, auth/money-adjacent) still need user approval before code.
- **Governance.** Removal policy (a rule that hasn't fired in three cycles is
  a removal candidate; every new rule states activation + removal conditions)
  and a measurement rule (cost claims require recorded cycle metrics).
  COMPARISON.md's unmeasured "cheapest" claims retracted.

Kept, unchanged in spirit: kernel journey + scope challenge, minimal-form and
provenance rules, scope-cut/ambiguity/dependency hard stops, verified fakes
and wire contracts, production-composition rule, migration up-down-up
rehearsal, reviewer independence + repro-before-fix, doc sync with
`brana-gate claims`, buy-before-build.

**2026-07-31 — post-independent-review fixes** (see
`docs/2026-07-30-brana-v2-independent-review.md`, all 8 findings accepted):
skill-only installs made self-contained (`brana-plan` bundles canon + gate,
`tools/check-dist.sh` guards drift; `sync-gate.sh` deleted); ledger protocol
made executable (no SHA in the committed ledger — U-ID in the commit
subject, `git log` authoritative); gate script rewritten without the
orphaned v1 `tasks` subcommand and contrast invocation corrected
(`docs PLAN.md DESIGN.md`); external-system and auth risk triggers
re-scoped (runtime boundary / authN-authZ+sensitive data+hostile input);
strategic-only dependency hard stop; measurement footer records active
modules + fired rules (removal policy now auditable); PLAN.md soft
~2,500-word budget; `examples/dally` archived as v1, `examples/notes-v2`
fixture added; plugin descriptions updated. Code-in-plan recorded as an
explicit unadopted trade-off pending measurement.

## 1.12.0 — 2026-07-27

Closes the seam v1.11's coverage-first crystallization reopened: "journey covered by existing tests" was a model assertion no script verified — the exact self-certification class v1.8 existed to close — and the skip path (the one path with no human witness) was the only path with no machine check at all. Plus three smaller integrity fixes from the same review.

- **Coverage is a citation, never an assertion (`brana-gate` done-mark integrity):** a merged-form gate's completion mark — `WALKED — PASS` **and** `SKIPPED` alike — must quote its coverage test path(s) (`` coverage `tests/...` ``), and each cited path must exist on disk (pytest-style `::node` suffixes accepted); a `SKIPPED` mark now also requires its evidence path — the coverage run is mandatory on skip, only the walkthrough is deferred. Legacy gates (separate adjacent crystallization task) are exempt: that task's own Done mark is the coverage evidence, already checked. Doc side: the rotated unglamorous step means gate N's journey differs from gate N−1's by design, so a "full coverage" claim must name the test serving *this* gate's rotated step.
- **Cadence warning (non-blocking):** more than ~5 feature tasks with zero mid demo gates warns — the fold-into-release-gate valve only covers ≤ ~5; previously a 20-feature TASKS.md with only a release gate passed `brana-gate tasks` clean.
- **Feature-task counting aligned:** every feature-task count (downgrade valve, caps, new cadence check) now excludes scaffold and spike tasks alongside gate/crystallization/proof — Task 0 exists in every cycle and spikes answer process questions; fix tasks still count (real scope a finding surfaced). Same off-by-category class v1.10 fixed, one layer down; prose and script now name the same set (`OVERHEAD_TYPES`).
- **Dependency re-approval leaves a trace:** a Task 0 resolver conflict that patches the dependency plan now records an ARCHITECTURE.md Decision-log line (what changed, why the resolver forced it), so 6a's version-drift check always compares against a plan whose amendments are visible.
- Verified: dally 001-core (legacy layout) passes clean — no regression; fixtures confirm merged-form WALKED/SKIPPED marks without coverage citations block, with citations pass, nonexistent cited paths block, and 7 feature tasks with no mid gate warns.
- Doc set: WORKFLOW.md (gate-linter bullet, milestone map, Phase 4 crystallization + downgrade valve, Phase 5 Task 0 + completion grammar), brana-1/4/5/6 skills, brana-gate + bundles, USAGE.md, READMEs, manifests.

## 1.11.0 — 2026-07-22

- **Compatibility-first dependency selection:** removed the requirement to choose every package's latest stable/LTS release. Dependency plans now select one mutually compatible exact set using an existing lockfile/current set, official scaffold/BOM and support/peer matrices, or a clean resolver result. Task 0 freezes that approved resolution and stops for plan re-approval on conflicts instead of burning attempts on ad-hoc upgrades/downgrades; 6a flags resolved direct-version drift.
- **Coverage-first demo gates + one cadence:** crystallization now proves cumulative journey-suite coverage instead of creating one e2e test per gate — reuse complete coverage, extend only uncovered behavior, create only when needed. Human walkthroughs remain mandatory unless waived; skipped gates still require green automation and carry only `UNWITNESSED` human debt. All current docs now use Phase 3's canonical cadence: roughly one mid gate per 8–10 feature tasks' worth of chunks (~3–4 chunks), minimum one and placed where runnable; 6a's independent 2–3-task review cadence remains.

## 1.10.0 — 2026-07-20

Token-diet release, from the first v1.9 field cycle (losein M1): the milestone map capped M1 at ~15 tasks, the split landed at 29 — 18 feature + 11 workflow-mandated tasks (3 demo gates, 3 crystallization tasks, release gate, scaffold, proofs). Nothing malfunctioned; the cap and the split counted different things, and gate ceremony was priced per-gate-plus-task. Three cheap upstream fixes; the considered Phase 4 oversize valve was rejected as the costly path (re-split at Phase 4 invalidates sunk docs and usually has no legal cut point that keeps the kernel journey served).

- **Feature-task counting (Phase 1 + valves):** every ~15-task cap — milestone map, Route S/lite qualification, Route C delta qualification, Phase 4 downgrade valve — now counts **feature tasks only**; gates, crystallization, and proof tasks are workflow overhead, not scope (~3–6 per full-profile milestone, noted in the milestone map so a ~15-feature milestone landing ~20 total reads as ceremony, not overshoot). `brana-gate tasks --spec` retro-lite valve counts the same way (excludes gate/crystallization/proof types).
- **Crystallization merged into the gate task (Phase 4/5/6):** a demo-gate task now *contains* its crystallization step — an `[e2e@gate-N]` criterion requiring the walked journey encoded as an e2e test **in the gate session itself**, while the journey is loaded context; the separate follow-up task (which re-loaded that context in a fresh session) is gone. Gate task is Done only when the walkthrough result is recorded and the journey test is green; `GATE SKIPPED` still encodes immediately (`UNWITNESSED` mark unchanged). Legacy layout (separate `crystallization`-type task immediately after its gate) still passes `brana-gate` — never authored for new cycles. Saves one task header, one interfaces/context-pack block, and one session spin-up per gate.
- **Gate cadence scales with milestone size (Phase 3):** mid demo gates at roughly one per 8–10 feature tasks' worth of chunks (~3–4 chunks), minimum one — replacing the flat "every 2–3 chunks", which priced 3 mid gates into an 18-feature milestone. Runnability stays the constraint; lite scaling (fold into release gate at ≤ ~5 feature tasks) unchanged.
- **`brana-gate` v1.10:** crystallization adjacency check replaced by the merged-form check (gate task carries an e2e criterion with its own gate n; legacy adjacent task accepted); the e2e journey-membership exemption extends to the gate task's own criteria; retro-lite valve counts feature tasks only. Schema help documents the merged form.
- Doc set: WORKFLOW.md (title, gate-linter bullet, journey suite, Route S/lite scaling, delivery contract, milestone map, Phases 3/4 templates, task gate checklist, v1 exit bar), skills 1–6, brana-gate + bundles, USAGE.md, READMEs, manifests.

## 1.9.0 — 2026-07-19

Right-sizing release, from a six-project field audit: across every real cycle (begirex, together, quick_pipeline, s2orc, befrest, zbuzzy) **zero SPEC.md files ever stamped `profile: lite`** — the off-ramp existed and was never taken (quick_pipeline: 14 tasks, under the lite cap, still full profile, 819-line TASKS.md). Root causes fixed where they live, plus the other volume driver the audit surfaced: the workflow builds everything from zero.

- **Dependency plan (build vs buy — new WORKFLOW.md section):** buy is the default. ARCHITECTURE.md gets a required section — `capability → package @ exact latest-stable/LTS version (registry-verified, never from memory) → what it replaces`; hand-rolls name their reason (no credible package / trivial < ~30 lines / core domain logic). **The user approves the package list before the doc is final**; an unlisted import at Phase 5 is a hard stop, same as a contract gap. Sprawl guard: packages serve *named* capabilities, trivial helpers stay hand-rolled. Architecture review category 8 (module duplicating a maintained package; selection-bar failures) and 6a category 9 (hand-rolling a plan package; unlisted import) enforce both directions. Task 0 installs at pinned versions.
- **Lite qualification fixed (why it never fired):** criterion 3 "no external system" disqualified every API-glue project; now "no *novel* external integration" — a well-known API via an official/established SDK qualifies, with a compact ≤1-page wire contract (verified-fake rule stands); only bespoke/undocumented integrations disqualify. Same wording in the Route C delta form.
- **Justified full (stamp integrity):** the profile stamp is always explicit — `profile: lite`, or `profile: full` + `profile-reason: <failing criterion>`. Bare `profile: full` = `brana-gate docs` finding (the qualification never ran); docs with no profile key are grandfathered.
- **Downgrade valve (Phase 4):** the real task count exists after the split; `profile: full` with ≤ ~15 tasks, one subsystem, no novel integration → stop and offer retro-lite (docs stay, downstream ceremony shrinks, stamp amended with a Decision-log line). `brana-gate tasks --spec` prints a non-blocking `retro-lite candidate` warning — fires on the quick_pipeline cycle that motivated it.
- **Risk-scaled task ceremony (Phase 4):** boundary tasks (cross-module CONSUMES/PRODUCES, wire contracts, Task 0, gates, crystallization) keep the full interfaces block + context pack; interior tasks carry objective/files/deps/criteria only, and a PRODUCES consumed inside its own module needs no `[contract]` criterion. Boundary-without-block blocks; interior-with-full-ceremony is a token-waste warning.
- **Scaling inside lite (no third tier):** ≤ ~5 tasks folds the mid demo gate into the release gate (one gate, full anatomy + crystallization); non-UI tools' mini UX.md reduces to operator-surface notes + kernel flow.
- **Milestone map (Phase 1, big ideas):** an idea beyond ~15–20 tasks or multiple subsystems decomposes into milestones — each its own `specs/NNN-name/` cycle ≤ ~15 tasks ending in a working, release-gated version; M1 is the kernel milestone, spec'd now. Future milestones live as 2–3 coarse lines in `specs/ROADMAP.md` (detail waits for that milestone's own cycle — Route C shape, delta qualification, often lite); ARCHITECTURE.md carries one-line forward constraints per future milestone; doc sync marks completed milestones.
- **`brana-gate` v1.9:** warning tier (printed, never blocks exit); `docs` checks profile-stamp integrity; `tasks --spec` runs the downgrade valve.
- Doc set: WORKFLOW.md (title, Route S, Dependency Plan section, Phases 1/2/3/4/5/6a/7, spec-dir convention), all seven skills, brana-gate + bundles, USAGE.md, READMEs, manifests.

## 1.8.0 — 2026-07-18

Grounding release, from a survey of script-backed skill systems (superpowers, compound-engineering): the two seams where the workflow still trusted a model asserting what a script could prove. Both land as `brana-gate` extensions — no new tools, no new install surface; every check follows the existing contract (stdlib-only, findings + exit codes, bundled per-skill).

- **Done-mark integrity (`brana-gate tasks`, fires only when done-marks exist):** the done-mark grammar is now machine-checked — every `- **Done:**` line must quote a backticked commit SHA and an evidence-file path, every `GATE n WALKED — PASS` line its evidence path, the evidence file must exist and be non-empty, and no task may be Done before its deps are resolved (Done, or gate WALKED/SKIPPED). Runs at Phase 5 re-runs, stale-plan re-gates, and the v1 exit bar preflight. An evidence-less done-mark was previously only prose ("doesn't pass the exit bar") — a reviewer's recall; now it's a finding. First run caught two real drifts in the shipped dally example (gate 2 walked without an evidence path; task 9 Done without a SHA) — both fixed.
- **`brana-gate claims` (new subcommand):** grounds a doc against the working tree — every backticked repo-relative path it cites must exist. Post-implementation only (planning docs legitimately cite future files): closes Phase 7 doc sync (living docs after every merged B/C/R feature) and joins the v1 exit bar. Path-shaped tokens only (known code extension, or first segment is an existing directory); branch names, routes, and signatures are skipped, as are fenced code blocks — measured false-positive rate on the repo's own docs: one, an illustrative example path.
- **Evaluated and rejected** (keeping the no-unnecessary-addons rule): a task-state engine (no concurrent writers in Brana — folded the real gap into the gate instead), project-type/port resolvers (no observed demo-gate false verdicts yet; add scoped, on evidence), subagent handoff packagers (Phase 5's pass-paths-not-prose delegate protocol already prevents paraphrase loss), session-transcript miners (crystallization tasks capture lessons deliberately; transcript formats are an unstable dependency).
- Doc set: WORKFLOW.md (gate-linter bullet, Completing a task grammar, v1 exit bar, Doc sync), brana-5/6/7 skills, USAGE.md, README badge, manifests; `sync-gate.sh` now bundles into brana-6-review too (five skills).

## 1.7.0 — 2026-07-18

Closes the scope-discipline gap found by the quick_pipeline post-mortem: the workflow had execution discipline (gates, evidence, contracts) but no scope discipline — a user's "fast delivery, just a dry-run argument" produced a full-profile Route C cycle with ad-hoc waiver frontmatter invented at Phase 4, UX screens for a CLI, ~900 lines of process-invented tooling, mergeable task pairs, and a catch-all gap-sweep task. Every fix lands where the fat entered, not where it surfaced.

- **Provenance check (Phase 1, part of the scope challenge):** every v1 bullet traces to user-stated, kernel-derived, or **process-derived** (verification tooling, output modules, audit commands the workflow itself wants). Process-derived bullets are listed to the user with rough task cost and enter v1 only by explicit call — same standing as convenience features.
- **Minimal-form rule (hard):** user minimizing language ("just a flag", "only a dry-run argument") caps the deliverable at its minimal form; elaborations (second mode, dedicated module, separate CLI, sentinel suites) are backlog by default, listed as priced options, never silently included.
- **Delivery contract (first-class):** a speed signal at cycle entry mandates two proposals *before drafting*: the lite profile if the qualification holds, and a `delivery:` frontmatter line in SPEC.md with a closed vocabulary (`demo_gates`/`walkthrough`/`canary` = `required`|`waived`). A waiver's substitute verification reuses existing machinery — a substitute needing new tooling is provenance-checked scope, never a waiver by-product. TASKS.md frontmatter may only echo the contract verbatim; ad-hoc waiver/exception keys are a gate finding.
- **Route C delta qualification:** change cycles run the Route S four-criteria check against the *delta* (one subsystem, ≤ ~15 tasks, no *new* external system — existing documented integrations don't disqualify, low delta stakes); a qualifying delta takes `profile: lite` regardless of the app's own profile. Waiving gates at Phase 4 after paying full-profile ceremony was the backwards form this replaces.
- **Operator surface rule (Phase 2):** screens are interactive UI only. CLI/log/terminal surfaces get an operator surface note (name, invocation, output format, error/exit convention) in UX.md — no S-ids, no wireframes, no DESIGN.md in their tasks' context packs; terminal style lives in CONVENTIONS.md.
- **Splitter merge bias + catch-all ban (Phase 4):** task count is a cost — emit the fewest tasks respecting the 50–300-line cap; consecutive linear-dependency tasks sharing a primary file merge. A final "fill remaining gaps" task depending on (nearly) everything is a blocking finding — criteria belong to the tasks owning the behavior; only gate/crystallization tasks depend wide.
- **`brana-gate` v1.7:** `tasks` gains `--spec SPEC.md` — validates the delivery contract's closed vocabulary in SPEC.md, requires TASKS.md's `delivery:` to echo it verbatim, and flags any ad-hoc waiver/exception frontmatter key; new deterministic `catch-all` check (non-gate/non-crystallization task with ≥80% of other tasks as deps and no PRODUCES). Both fire on the quick_pipeline TASKS.md that motivated them.
- Doc set: WORKFLOW.md (Delivery Contract section, Route C delta qualification, Phases 1/2/4/7), brana-1/2/4/7 skills, brana-gate + per-skill bundles, USAGE.md, README, manifests.

## 1.6.0 — 2026-07-16

Closes the process-weight gap from the v1.3 expert critique: Phase 7 routed changes by size (A/B/C/R) but Phases 1–6 were one-size — a weekend tool paid eight documents and full gate ceremony, so users improvised skips, and the workflow's guarantees are chain-shaped: one silently skipped link collapses the chain. Route S is the sanctioned off-ramp.

- **Route S — lite v1 profile:** chosen at Phase 1 end by four explicit criteria (single subsystem; ≤ ~15 estimated tasks; no external system in the kernel journey or a v1 flow; low stakes — no multi-user data, no payments), recorded as `profile: lite` in SPEC.md frontmatter; downstream phases read the stamp.
- **Kept in every profile (the load-bearing links):** SPEC with kernel journey + scope challenge, falsifiable criteria, verify script + evidence files, same-composition rule, scope-cut/ambiguity hard stops, git rules, ≥1 mid demo gate plus the release gate, crystallization tasks, the task gate (`brana-gate tasks` without `--plan`; chunk checks skip, everything else stands), the v1 exit bar.
- **Folded or cut:** PRD folds into a SPEC acceptance-criteria section (~700-word cap total); UX.md ships mini (screen ids, kernel flow, one line per screen on empty/error); ARCHITECTURE.md ships lite (stack, data model, contract surface, traceability, Decision log) and stays a living root doc so Phase 7 works unchanged; PLAN.md and FILE_STRUCTURE.md are cut — chunking and both gates are authored directly in TASKS.md with full gate anatomy; DESIGN.md only if UI-heavy (else ≤5 style rules in CONVENTIONS.md); architecture review advisory, with a skip recorded in SPEC.md as an accepted-risk line; consistency gate shrinks to `brana-gate docs` + a short LLM pass, stamping SPEC.md.
- **Escalation is a hard rule:** mid-flight discovery of a second subsystem, an external system, or a boundary change beyond the lite architecture stops the line and upgrades to the full shape (Route C-style delta docs, consistency gate re-run) — outgrowing lite silently is the same self-certification seam the gates close.
- Doc set: WORKFLOW.md (Route S section, Phase 1 profile choice, Phase 2/3/4 delta lines), brana-1/2/3/4 skills, USAGE.md, README, manifests.

## 1.5.0 — 2026-07-16

Closes the design-correctness gap from the v1.3 expert critique: the pipeline was Opus-writes → mechanical consistency check → implementation — nobody ever reviewed the design itself, and wrong-but-consistent architecture passes every machine pass by definition. Plus NFR/security traceability, which functional flows had and non-functional requirements didn't.

- **Architecture review (blocks Phase 3):** one independent, findings-only review of ARCHITECTURE.md against PRD + UX at Phase 2 exit, under 6a's independence rules (no author rationale; fresh session; different model/vendor preferred). Fixed categories: missing failure handling, data-model flaws, concurrency/ordering hazards, first-thing-that-breaks at 10×, over-engineering (a module serving no requirement), simplest-credible-alternative per major decision (no credible answer is itself a finding), threat-model gaps. The human arbitrates — accepting a design finding is a product decision — and ARCHITECTURE.md is patched before Phase 3.
- **Spike escape valve:** ARCHITECTURE.md still forbids open "X or Y" decisions, but a decision genuinely unresolvable by reasoning now gets a `SPIKE: <question>` marker (candidates, leading candidate, deciding measurement) instead of a guess. Phase 3 turns each marker into a time-boxed spike chunk at the head of PLAN.md — throwaway code allowed, falsifiable answer criterion, Decision log entry replaces the marker; an overturning result triggers the stale-plan and stale-interface-block rules. Consistency gate flags markers with no spike chunk and spike chunks with no answer criterion.
- **NFR traceability (same shape as flow traceability):** every PRD non-functional requirement carries a budget + measurement (the command or procedure producing the number); the consistency gate flags any NFR with no serving mechanism (verify-script check, tagged criterion, or release-gate observation step); the release gate measures every budget in the release build — at or under, or explicitly accepted over with the number recorded.
- **Threat model (conditional):** apps with auth, user data, or external input get a threat-model section in ARCHITECTURE.md — trust boundaries, authN/Z per surface, input-validation strategy, secrets handling. 6a's security category now reviews against it instead of against vibes; the architecture review checks it for gaps. No such surface → omit, pay nothing.
- **Verify-script hardening:** every stack wires a dependency audit (npm audit / pip-audit / equivalent) and a secret scan at Task 0, both failing the script — alongside the existing a11y check for UI stacks.
- Doc set: WORKFLOW.md (Verification Machinery, model bindings, Phases 2/3/5/6), brana-2/3/5/6 skills, USAGE.md, README, manifests.

## 1.4.0 — 2026-07-16

Closes two guarantee-breaking seams found by an expert critique of v1.3, plus two cheap rule fixes. Theme: the workflow's own Reality Rule 8 applied to the workflow itself — gate checks that are mechanical now run as code, not as a cheap model's recall.

- **Deterministic gate core — `tools/brana-gate`** (single-file Python 3.11+, stdlib only): the machine gates were LLM prompts doing exhaustive cross-referencing over long context — exactly what cheap models fail at, silently, with an unmeasured false-negative rate. Now TASKS.md tasks are heading + fenced TOML blocks (schema in `--help`), and `brana-gate tasks` runs every structural task-gate check deterministically: chunk coverage both ways, dependency cycles, walking-skeleton ordering, layer tags, `[e2e@gate-N]`↔journey membership, PRODUCES→`[contract]`, gate preflight fields, crystallization adjacency, release-gate presence/position, CONSUMES exact-match against ARCHITECTURE.md or an earlier PRODUCES (also catching splitter paraphrase drift), and wire-contract obligations (production-composition proof on the release gate, shared-suite criterion on fakes). `brana-gate docs` covers the consistency gate's scriptable checks: unresolved placeholders and **computed** WCAG contrast from DESIGN.md tables with stated-vs-computed mismatch flagging — a contrast ratio is never an LLM's to compute. Where the tool is present its clean exit is the mandatory blocking half of each gate; the LLM pass shrinks to the judgment checklist (contradictions, open decisions, semantic serving). Copy-paste mode keeps the full prompts as fallback.
- **Stale-plan rule:** a mid-cycle PLAN.md section rewrite — escalation verdict, spawn-route patch, human edit — previously escaped re-gating entirely: the stamp stayed `gate-passed` while downstream tasks were derived from a chunk that no longer existed. Now any such rewrite reverts PLAN.md and TASKS.md to `draft` until a scoped re-gate is clean (consistency checks on the patched section, task gate on the tasks serving the patched chunk, affected tasks/gate journeys updated) — before the next implementation session. Referenced from Phase 5 escalation, the Phase 6b spawn route, and Phase 7's escalation rules, parallel to the stale-interface-block rule.
- **Finding confirmation (6a):** review findings were applied blind — an LLM reviewer's false positive became a fix task, churn, and regression risk. Findings are now unverified claims until a confirmation pass (fixer-tier) reproduces each bug/logic-error/race (failing test or concrete repro) and quotes both sides of each contract/convention violation; unconfirmable findings escalate to the human with the failed-confirmation note — never silently dropped, never blindly fixed. Repro tests land with the fix and join the suite. REVIEW_N.md records confirmation status; only confirmed findings become fix tasks.
- **Crystallize on skip:** `GATE SKIPPED` previously deferred the gate's crystallization task, so a run of skipped gates accumulated *automation* debt and concentrated one giant integration surprise at the exit bar. Writing the e2e needs only the scripted journey, not a walkthrough — so the crystallization task now runs immediately on skip, its test marked `UNWITNESSED` (same visible-debt mark) until the journey is walked, at latest the v1 exit bar. A skip now costs human attention debt only; `DEFERRED` is retired. The exit bar lists each skipped gate with its unwitnessed test: walked now or explicitly accepted.
- Doc set: WORKFLOW.md (Verification Machinery, model bindings, agent layer, Phases 3–7), skills 3–7, USAGE.md, README, manifests.

## 1.3.0 — 2026-07-16

Closes the last unchecked phase seam: Phase 4's output was self-certified — the splitter stamped its own TASKS.md `status: ready`, and the first integrity check of the task list was a gate preflight *during* Phase 5, the most expensive moment to learn a journey step has no serving task.

- **Task gate (blocks Phase 5):** a mandatory machine pass (Haiku/Flash tier, fresh session) at Phase 4 exit, mirroring the consistency gate's anatomy. Cross-references TASKS.md against PLAN.md and ARCHITECTURE.md's interface/wire-contract sections: chunk coverage in both directions, dependency cycles and walking-skeleton ordering, gate journey steps with no earlier serving task (walkable on paper — the static version of the Phase 5 preflight), CONSUMES quotes with no matching upstream PRODUCES or ARCHITECTURE.md section, untagged criteria / `[e2e@gate-N]` criteria absent from their gate journey / PRODUCES tasks missing their `[contract]` criterion, incomplete preflight blocks and missing crystallization tasks and unglamorous steps, missing RELEASE GATE task, and (when wire contracts exist) a release gate without its production-composition proof dependency or fake tasks without the shared-suite criterion. Every check is cross-referencing, not judgment; no human pass — intent was already checked at the consistency gate.
- TASKS.md is now written `status: draft` and flipped to `ready` only by a clean task-gate pass; Phase 5's refusal of a draft TASKS.md is unchanged but the stamp is no longer self-issued.
- Scope note: the gate guarantees *structural* closure (every step traced, every seam matched, every gate walkable on paper). Semantic gaps — a concept nobody wrote down — remain the release gate's and spawn route's job (v1.2).
- Doc set: WORKFLOW.md (Phase 4 Task Gate section, stamp semantics, model bindings, agent layer), brana-4/brana-5 skills, USAGE.md.

## 1.2.0 — 2026-07-16

Closes the production-seam gap class, found by a live-use post-mortem of a pipeline project (s2orc): every demo gate passed on fixtures while the production daemon composition was never planned, the fake provider's convenience shape stood in for the real wire contract, and both surfaced only at the final release gate — forcing two improvised mid-cycle specs. Four fixes; new terms defined once in WORKFLOW.md's Verification Machinery:

- **Wire contracts + verified fakes (conditional):** when the kernel journey or a v1 flow depends on an external system that will be faked, Phase 2 ARCHITECTURE.md gives it a versioned **wire contract** (exact request/response shapes, auth, error semantics) with traceability extended to those journey steps; Phase 4 gives any fake of that system a `[contract]` criterion running one shared suite against both fake and real adapter — the fake must reject what the contract rejects; real-adapter side offline (request-shape assertions, recorded fixtures), live calls only in a bounded canary through the production composition. Consistency gate flags an external system with no wire contract. Projects without external systems pay nothing.
- **Same-composition rule:** a gate's disposable/fixture launch path is the production entry point with config/fakes injected at seams — never a bespoke gate-only assembly (which lets every gate pass while the production path stays unbuilt). Blocking finding at Phases 3/4 and the consistency gate; 6a gains finding category 8 (composition and fake integrity). When fakes stand in for an external system, one pre-release-gate chunk is the **production-composition proof**: the production entry point composes fully against a disposable target.
- **Release gate:** the v1 exit bar is now PLAN.md's mandatory final gate entry with full demo-gate anatomy — kernel journey in a release build, each step traced to a serving chunk through the production composition — checked at the consistency gate, preserved as a gate task in Phase 4, preflighted with `GATE BLOCKED` semantics in Phases 5/6. A kernel-journey step with no production path is now a Phase 3 finding, not a release-day discovery.
- **Spawn route (pre-v1):** fixing a blocked gate that reveals a missing subsystem or new/changed contract spawns a scoped child `specs/NNN-name/` cycle (Route C shape, ARCHITECTURE.md patched); parent gate stays `GATE BLOCKED` referencing the child, stale-interface re-sync runs on the parent's not-done tasks, parent preflight re-runs after the child completes. Codifies what the post-mortem project improvised.
- Doc set: skills 2–7 mirrored to canon.

## 1.1.0 — 2026-07-15

Closes all 15 gaps (G1–G15): fourteen found by a senior-engineer concept review of v1.0.0, plus one live-use finding (G15); full findings record and gap→fix map at `docs/history/2026-07-15-v1-gap-review.md`. Governing question: what makes apps built by this workflow hard to maintain or test? The fixes compile human checks into machine checks — the workflow's own Reality Rule 8, added by this release.

- **Machine-check compilation (G1, G2, G3, G7, G14):** demo-gate journeys crystallize into automated e2e tests via a new crystallization task, joining a **journey suite** that's part of the verify script from then on; Phase 4 tags every acceptance criterion with its verifying layer (`[unit]`/`[integration]`/`[contract]`/`[e2e@gate-N]`); any task with a PRODUCES block gets a `[contract]` test asserting the exact produced shape; migration tasks run up→down→up against fixture data with a data-preservation assertion.
- **Verification integrity (G5, G6):** verification evidence is now a captured artifact — `specs/NNN-name/evidence/task-N.txt` (command + last ~30 lines of output), captured live, referenced by path from the TASKS.md done-mark, never self-reported prose. Task 0 creates one documented **verify script** (build+lint+typecheck+suite, +journey suite once it exists) and, in agent mode, wires CI to run it on push when the repo has a remote.
- **Review depth (G4, G8, G9):** 6a gains finding category 7 — test adequacy (missing test, an assertion-free test, a test that mocks away the behavior under review); lint and typecheck green is now a precondition to starting a 6a review; a **compound rule** turns any finding class (the same specific rule or pattern, not the same numbered category) that repeats twice in one review cycle into a CONVENTIONS.md line or lint rule, closing that class for good.
- **Maintainability (G10, G11, G12, G13):** new **Route R** in Phase 7 for refactors and dependency upgrades (verify + journey suite green before and after, behavior-change freeze, mandatory 6a, doc sync); `FILE_STRUCTURE.md` demoted from a root living doc to a per-cycle archived prediction under `specs/NNN-name/` — the repo tree and code map are the living truth for structure, closing the doc/code duplication Reality Rule 5 forbids; ARCHITECTURE.md gains an append-only **Decision log** (`YYYY-MM-DD — decision — why`), appended by Route C patches and doc sync, never trimmed; a **stale-interface-block rule** re-syncs every not-done task's CONSUMES/PRODUCES quotes after a mid-cycle contract patch.
- **Git discipline (G15, found by the user in live use):** Phase 5's Step 0 now checks the current branch before any code — on main/master it creates the cycle branch, direct-to-main only on explicit instruction; Route A moves off "commit to main" onto a short-lived branch merged after verify is green (waivable per instance).
- Smaller (G14): `REVIEW_N.md` now lives at `specs/NNN-name/reviews/`, in the spec-dir convention; parallel subagent dispatch is restricted to tasks with disjoint file sets and no dependency edge.
- **Also folded in** — demo gates made runnable by construction: gate placement is now cadence-as-target + runnability-as-constraint, every DEMO GATE entry carries runnability preconditions (launch command, seed data, serving chunk per journey step, a disposable/fixture path when the journey would otherwise touch production state); the agent preflights every gate before the soft stop, and a failed preflight is the new `GATE BLOCKED` state (fix tasks first, walk later) — distinct from `GATE SKIPPED`, and unresolved `GATE BLOCKED` fails the v1 exit bar outright; Task 0's scaffold smoke test is "app boots via documented run command."
- Doc set: skills mirrored to canon; self-consistency pass across WORKFLOW.md, all 7 skills, README.md, skills/README.md, skills/USAGE.md, and COMPARISON.md corrected stale references (`FILE_STRUCTURE.md` still listed as a living root doc, `Route A commits to main` leftovers, evidence described as an inline prose line instead of a captured file, route lists missing R, and the per-cycle/living doc counts).

## 1.0.0 — 2026-07-12

First public release as **Brana**. Skills renamed `wf-N-*` → `brana-N-*`. Added README, LICENSE (MIT), CONTRIBUTING, Claude Code plugin manifest, and a public-facing COMPARISON.md.

### Pre-release lineage (internal versions)

- **v2.2** — folded in five tested patterns from [Superpowers](https://github.com/obra/superpowers) and [Compound Engineering](https://github.com/EveryInc/compound-engineering): path-based delegation, task interface blocks (CONSUMES/PRODUCES), live verification evidence + commit-SHA ledger, reviewer independence, and `status:` frontmatter stamps with downstream refusals. Plus Phase 1 brainstorming moves (decomposition, ask-first interviewing, multi-approach proposals, integration check, spec self-review). Made per-task visual verification opt-in.
- **v2.1** — added DESIGN.md as the fourth Phase 3 living doc (design-system contract; fixes incoherent AI-generated UIs); synced skills to canon.
- **v2.0** — consolidated from 5 agent proposals after a v1 post-mortem: 7-phase structure, kernel journey, demo gates, consistency gate, living-doc model, model-tier bindings, copy-paste canon.
