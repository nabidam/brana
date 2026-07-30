# Brana Workflow Token-Efficiency Audit

**Date:** 2026-07-30  
**Scope:** Workflow instructions, skills, reference workflows, and generated planning artifacts  
**Code review:** Excluded by request  
**Repositories sampled:** Brana, FAI Toolkit, Astryxs RTL Dashboard, Chillify, BegireX, and S2ORC

## Executive conclusion

The concern is valid. Brana contains several strong engineering and product controls, but its current packaging works against its original goals of lower token use, simplicity, professionalism, and clear coordination between agents.

The main problem is not that Brana tasks are unusually verbose. The main problem is the document graph around those tasks. The same product facts move through SPEC, UX, PRD, ARCHITECTURE, PLAN, FILE_STRUCTURE, CONVENTIONS, DESIGN_SYSTEM, and TASKS. Each phase rereads prior artifacts, changes their representation, adds another gate, and preserves more status or evidence. This creates substantial context amplification before implementation begins.

The sampled Brana projects generated roughly three to four times as many initial planning words as the Superpowers project in the full workflow. A conservative document-traffic estimate, which counts generated planning words and workflow-mandated rereads but excludes coding, reviews, interviews, prompts, and tool output, puts the full Brana examples at roughly twelve to fifteen times the Superpowers example.

Brana Lite is a meaningful improvement. Astryxs is much closer to Superpowers than the full-profile projects. It still used six initial artifacts and more planning words for fewer tasks and a narrower product. This suggests that Lite reduces the symptom but retains the underlying multi-artifact information architecture.

The strongest parts of Brana should remain:

- Kernel-first scope and a concrete kernel journey
- Explicit approval for user-visible scope cuts
- Production-composition verification
- Verified fakes where external systems require them
- Independent review for risky work
- Human judgment on a running release
- Small, isolated implementation packets
- A concise current architecture record for mature systems

The workflow itself should become smaller. Most projects need one canonical plan, optional risk-specific sections, transient task briefs, and review effort concentrated near implementation.

## Method and limitations

This audit read only documentation and repository history metadata. It did not inspect application source code. The material included:

- Brana's `WORKFLOW.md`, phase skills, usage guides, comparison document, changelog, and history documents
- Planning artifacts and task documents in the five project repositories
- Superpowers design, plan, and SDD progress/report artifacts in FAI Toolkit
- The two workflow references under `references/`
- Commit subjects and file history where they revealed documentation or evidence behavior

For a fairer comparison, the quantitative tables use the earliest committed planning snapshots available before later task status, evidence, remediation, and historical material inflated the documents. Current totals are shown separately.

The document-traffic estimate is a lower-bound proxy, not an API billing measurement. It adds generated document words and the words in documents that later phases are instructed to reread. It does not model tokenizer differences, provider caching, prompt boilerplate, tool output, interviews, source-code reads, implementation, review discussions, or retries. Its value is comparative: repeated canonical documents still impose context cost even when exact billed-token behavior varies.

## Quantitative comparison

### Initial planning artifacts

| Project and workflow | Initial artifacts | Tasks | Lines | Words |
|---|---:|---:|---:|---:|
| FAI Toolkit, Superpowers | 2 | 21 | 1,210 | 6,963 |
| Astryxs, Brana Lite v1.12 | 6 | 17 | 1,124 | 8,702 |
| BegireX, early Brana | 9 | 22 | 1,908 | 20,463 |
| S2ORC, early Brana | 9 | 33 | 3,299 | 24,990 |
| Chillify, Brana full | 9 | 21 | 3,324 | 26,802 |

The FAI Toolkit split was:

| Artifact | Words |
|---|---:|
| Design | 1,015 |
| Implementation plan | 5,948 |

The Brana splits were:

| Artifact | Astryxs | BegireX | S2ORC | Chillify |
|---|---:|---:|---:|---:|
| SPEC | 796 | 635 | 653 | 702 |
| UX | 672 | 4,162 | 4,303 | 3,197 |
| PRD | Not separate | 2,687 | 4,497 | 2,963 |
| ARCHITECTURE | 2,069 | 3,274 | 5,491 | 7,809 |
| PLAN | Not separate | 3,161 | 2,510 | 4,141 |
| CONVENTIONS | 396 | 546 | 756 | 1,040 |
| DESIGN_SYSTEM | 787 | 1,252 | 1,458 | 2,481 |
| FILE_STRUCTURE | Not separate | 676 | 801 | 1,590 |
| TASKS | 3,982 | 4,070 | 4,521 | 2,879 |

### Important interpretation

Brana's initial task documents are not the primary source of bloat. Their approximate density ranged from 137 to 234 words per task, while the FAI implementation plan averaged about 283 words per task. Brana's higher cost comes from the surrounding documents and from repeatedly translating the same facts between them.

This distinction matters. Simply shortening `TASKS.md` would not solve the core problem.

### Current planning-document totals

Later status, evidence, remediation, and historical sections increased the current document sets:

| Project | Current words |
|---|---:|
| Astryxs | 8,908 |
| S2ORC | 25,633 |
| BegireX | 31,464 |
| Chillify | 38,628 |

BegireX is the clearest task-document inflation example. Its initial `TASKS.md` contained 4,070 words. The current file contains 15,008 words, an increase of about 269 percent.

### Lower-bound document traffic

The following proxy counts initial generated words plus workflow-mandated rereads:

| Project and workflow | Approximate document traffic |
|---|---:|
| FAI Toolkit, Superpowers | 8,000 words |
| Astryxs, Brana Lite | 26,000 words |
| BegireX, Brana full | 94,000 words |
| S2ORC, Brana full | 118,000 words |
| Chillify, Brana full | 123,000 words |

These estimates do not prove an exact token multiplier. They do show why full Brana sessions can feel much more expensive before source code is touched. Every extra authoritative artifact is paid for once when written and again whenever later phases need its content.

## Findings

### 1. Artifact fan-out is the primary cost driver

The full workflow creates nine planning artifacts. Their nominal responsibilities differ, but their information boundaries are not clean enough to prevent repetition:

- `SPEC.md` defines the kernel, scope, edge cases, stack, and design direction.
- `UX.md` restates the kernel as journeys, screens, states, and interaction rules.
- `PRD.md` restates scope, journeys, errors, and acceptance criteria.
- `ARCHITECTURE.md` maps those journeys and requirements to systems and contracts.
- `PLAN.md` maps the architecture to implementation chunks.
- `TASKS.md` maps those chunks again to executable work.
- `FILE_STRUCTURE.md` predicts where that work will live.
- `CONVENTIONS.md` and `DESIGN_SYSTEM.md` add cross-cutting constraints that are then repeated in tasks.

The documents are not exact copies, but token cost follows semantic repetition as well as verbatim repetition. A kernel flow represented five times is still five context payloads. It also creates multiple places where a change must be synchronized.

This is the central architectural issue in the workflow.

### 2. The workflow and its skills duplicate authority

The core instruction surface is already large:

| Source | Lines | Words |
|---|---:|---:|
| `WORKFLOW.md` | 908 | 14,687 |
| Seven Brana skills combined | 923 | 16,962 |
| Combined | 1,831 | 31,649 |

This excludes `skills/USAGE.md`, `README.md`, `COMPARISON.md`, prompts, and historical guidance.

Text comparison found that roughly 45 percent of distinct eight-word sequences overlap between `WORKFLOW.md` and the skills. About 55 percent of normalized substantive skill lines also appear verbatim in `WORKFLOW.md`.

The repository's own maintenance rule says that every line should change behavior and redundant lines should be deleted. The current instruction packaging does not satisfy that standard. It has at least two operational authorities plus supporting documents that restate them.

The practical costs are:

- Larger context whenever a phase skill is loaded with workflow context
- More opportunities for rules to drift between copies
- Higher maintenance effort for every process change
- Repeated behavioral guidance that does not improve the agent's decision

One source should be canonical. Skills should route to compact, relevant instructions instead of reproducing the manual.

### 3. Brana has developed a safety ratchet

The changelog shows a consistent pattern: a project exposes a real failure, and the response adds a global field, gate, artifact rule, task type, or tool check. The safeguard is then copied into the workflow, skills, usage material, and future outputs.

Examples include:

- S2ORC led to production-composition checks, wire contracts, release gates, and spawn-route controls.
- Quick Pipeline led to provenance, delivery contracts, operator surfaces, and a catch-all-route ban.
- A six-project audit led to Lite qualification, dependency approval, and retro-Lite logic.
- Losein led to feature-task counting and changes to gate or crystallization behavior.
- Later revisions added coverage citations, evidence-integrity rules, and stale-plan gates.

These additions often address genuine problems. The issue is that controls are rarely retired, combined, or activated only for the risks that need them. The workflow therefore grows monotonically.

A professional workflow needs a removal policy as much as an addition policy. A failure in one project should not automatically become permanent context for every project.

### 4. Too much certainty is demanded before implementation

Full Brana can require all of the following before implementation:

- Detailed screens and states
- Database definitions
- API contracts
- Exact dependency versions
- Component hierarchy
- Full file-tree predictions
- Task-level file lists
- Fixture topology
- Function or interface signatures

Some of this is useful for high-risk areas. Requiring it globally creates predictive artifacts that are most likely to become stale in existing or integration-heavy systems.

The workflow partly acknowledges this by treating file structures and context packs as predictions, then adds stale-plan and interface reconciliation rules to repair the predictable drift. That is a costly loop:

1. Predict implementation details early.
2. Encode them in several artifacts.
3. Discover reality during implementation.
4. Detect staleness.
5. Update every affected artifact.

The simpler approach is to specify stable behavior and risk contracts early, then decide low-level structure close to the implementation unit.

### 5. Quality spending is front-loaded

The Superpowers project demonstrates a different error budget. Its plan was imperfect, but immediate task work and independent review exposed concrete problems near implementation:

- A wallet lost-update hazard
- Proxy and metering issues
- A contradiction in the plan's no-floating-point rule
- A payment-poisoning vulnerability
- Gateway error handling gaps
- An admin-name uniqueness issue

These findings appear in FAI Toolkit's SDD progress log. They support an important point: a detailed plan does not remove implementation discoveries. Superpowers assumes the plan will be imperfect and spends review effort against working changes, tests, and diffs.

Brana spends 20,000 to 27,000 initial words on full-profile projects before code, then still pays for implementation verification and review. Better product planning can prevent waste, but the sampled artifact volume is beyond what these outcomes justify.

Review tokens generally carry more evidence after implementation because the reviewer can inspect concrete behavior. Brana should keep early planning for product truth and irreversible decisions, then move more of its assurance budget to the risky implementation units.

### 6. Evidence bookkeeping pollutes normal project history

Phase 5's sequencing can create an implementation commit, an evidence update, and a task completion mark. When evidence includes the implementation SHA, the documentation update naturally follows the implementation and often needs another commit or amend.

In sampled matching history:

- Astryxs had 17 task or evidence bookkeeping commits in the first 80 relevant entries.
- Chillify had 28.

This makes history noisier without necessarily improving the product. It also increases agent work because status and evidence become content that must be maintained, reviewed, and committed.

Superpowers keeps much of its controller state and reports under `.superpowers/sdd`. The feature history remains more centered on feature work. Brana should similarly separate execution telemetry from durable product documentation.

Good alternatives include:

- CI artifacts
- A local `.brana/` execution ledger
- Git notes
- One final verification report
- External run records

Evidence should remain available without forcing each status transition into the main planning documents and commit stream.

### 7. Living documents are becoming history archives

Chillify's current `ARCHITECTURE.md` contains 13,779 words. From line 873 onward, historical or cancelled-cycle material and the decision log account for 5,299 words, about 38 percent of the file.

This conflicts with the idea that the architecture document represents current truth. Future agents performing impact analysis must pay to read past states alongside the current system.

Current state and history have different access patterns:

- Current architecture should be compact and routinely loaded.
- Historical decisions should be stored as ADRs or solution notes and loaded only when the relevant decision is questioned.
- Cancelled work should not remain in the primary current-state document.

Appending history is easy, but it steadily increases every future context window.

### 8. Full and Lite are too blunt as the main routing decision

Brana Lite materially reduces output, but the qualification rules remain conservative. Projects involving common concerns such as authentication, user data, external input, or integrations can be pushed into the full profile and then pay for every document and gate.

Risk is multidimensional. A project can be:

- UI-heavy but architecturally simple
- Integration-heavy but visually trivial
- Payment-sensitive but otherwise small
- Migration-heavy without a new user interface
- Security-sensitive without complex deployment

A binary profile bundles unrelated controls. Conditional modules would be more precise:

- Payments activate money, idempotency, and concurrency checks.
- External dependencies activate wire-contract and verified-fake checks.
- Migrations activate rehearsal and rollback.
- UI-heavy work activates UX and design-system depth.
- Authentication activates threat-model and session checks.
- Operator tools activate command, observability, and recovery flows.

The current Phase 4 retro-Lite valve can discover that a full profile was unnecessary, but only after the expensive documents have already been generated. It recognizes the classification problem after the sunk cost.

### 9. Line-count task sizing is a weak proxy

The 50 to 300 line task cap does not reliably represent cognitive complexity or reviewability. A task can be small in lines but span many components, interfaces, and deployment surfaces.

Chillify's first task touched more than 20 files. That is not naturally a compact one-prompt unit even if the expected code count fits the range.

Better task boundaries are behavioral and dependency-based:

- One observable outcome
- One primary risk
- A bounded set of interfaces
- An independently verifiable completion condition
- Minimal cross-unit coordination

Line estimates can remain a warning signal, but should not be the defining constraint.

### 10. Interface blocks are useful but over-replicated

Superpowers uses interface blocks to make a task concrete. Brana adopted this useful mechanism, then often repeated the same contracts through ARCHITECTURE, PLAN, and TASKS.

This creates three costs:

- Repeated context
- Drift between versions of the same contract
- Tests that protect prematurely chosen implementation details rather than stable behavior

A contract should have one authoritative location. Task briefs should reference or extract it, not restate and transform it multiple times.

### 11. Fresh sessions plus copied canon amplify context

Fresh task or phase contexts can improve isolation. They become expensive when each fresh context receives large copies of upstream documents and duplicated workflow instructions.

Isolation and compression must work together:

- Give the worker only the relevant unit, contracts, and acceptance criteria.
- Keep a compact ledger for the controller.
- Extract context mechanically where possible.
- Do not send the whole plan or document set to every worker.

Without bounded packets, fresh sessions repeat the workflow's largest cost.

### 12. The gate stack is cumulative

The workflow can apply:

- Architecture review
- Consistency gate
- Task gate
- Per-task verification and evidence
- Review every two or three tasks
- Demo gate
- Crystallization
- Release gate

Each gate has a defensible purpose in isolation. The full stack is expensive, particularly when several gates inspect overlapping product and integration concerns.

The default should be one release-level product gate through production composition. An intermediate product gate should exist only when there is a meaningful runnable vertical slice, a high-risk decision needs early validation, or the user asks for it.

Deterministic checks should run through one tool or script. The skills need to say when to run it, not reproduce the complete checklist at every phase.

### 13. Dependency approval is more controlled than routine work requires

Architecture-stage approval for each package and exact version, followed by reapproval if resolution changes it, front-loads package decisions before the actual dependency graph is resolved.

This is appropriate for sensitive or strategic dependencies. It is excessive for ordinary packages already consistent with the repository's stack and policy.

A better rule would classify dependencies:

- Routine, already-policy-compliant packages can be selected during implementation and reported.
- New strategic frameworks, paid services, unusual licenses, native dependencies, or high-risk packages require approval.
- Lockfiles and automated license or vulnerability checks verify resolved versions.

This keeps user authority where it matters without turning normal resolution into a planning loop.

### 14. Status and evidence can consume the task document

Older BegireX artifacts show the failure mode clearly. The task file grew from 4,070 to 15,008 words as status, evidence, remediation, and completion material accumulated. Eight remediation tasks were appended after the initial plan.

The current workflow's move toward separate evidence files is a partial improvement. The deeper rule should be that the canonical plan describes intended and current work, while high-volume execution evidence lives elsewhere.

### 15. Some current comparison claims are stale or unsupported

`COMPARISON.md` is dated 2026-07-12 and identifies Brana v1.3. It states:

- Five per-cycle plus four living artifacts
- About 600 lines total
- Brana is the cheapest workflow to run
- Brana is cheapest per feature

The current core workflow and seven phase skills contain 1,831 lines and about 31,649 words before usage and supporting documents. The sampled project outputs also do not support a categorical cheapest-per-feature claim.

These statements should be treated as historical or unmeasured, not as current evidence. Workflow claims about cost should be backed by repeatable measurements on comparable tasks.

## Project-specific observations

### FAI Toolkit with Superpowers

FAI Toolkit used one design document and one implementation plan for 21 tasks. The plan was detailed and sometimes code-heavy, but it formed a single task sequence instead of a graph of transformed artifacts.

Its SDD execution model has several efficient properties:

- A fresh worker receives one exact task brief.
- A script extracts the brief from the plan.
- The worker receives relevant context, not the entire plan.
- The reviewer receives the brief, report, and diff package.
- A compact controller ledger tracks progress.
- Spec compliance and code-quality review happen immediately.
- Whole-plan reads by task workers are explicitly discouraged.

The reference material records a prior 42,000-character dispatch where about 99 percent of the payload was pasted history. The workflow corrected this with bounded packets. That is directly relevant to Brana.

Superpowers is not free of token cost. After the first 11 FAI tasks, saved SDD documents contained about 20,244 words:

| SDD material | Words |
|---|---:|
| Extracted briefs | 4,126 |
| Reports | 14,284 |
| Ledger | 1,834 |

The briefs are mechanically extracted and not necessarily newly generated. More importantly, this cost is incurred against real task execution, diffs, and failures rather than paid almost entirely before code.

Superpowers' weaknesses are also worth retaining in the comparison:

- Plans can be overprescriptive.
- Plans may embed too much implementation code.
- It has less built-in product and UX validation than Brana.
- Per-task implementer and reviewer loops can still be expensive.

The lesson is not to copy Superpowers wholesale. The useful lesson is bounded context and immediate evidence-based review.

### Astryxs with Brana Lite v1.12

Astryxs is the best evidence that recent Brana revisions helped:

- Initial planning fell to 8,702 words.
- It used six documents rather than the full nine.
- Its current total remained close to the initial total.

It still exceeded FAI Toolkit's 6,963 initial words despite having fewer tasks and a narrower product. This indicates remaining structural overhead.

The task document also needed a prose waiver around Task 0 audits and checks. That is a small but revealing symptom: the workflow first mandates broad setup work, then needs a special exception to explain why the task does not fit its normal shape.

### Chillify with full Brana

Chillify is the strongest example of a mature full-profile Brana run:

- 26,802 initial planning words
- 38,628 current planning words
- 21 tasks, the same task count as FAI Toolkit
- 13,779 words in the current architecture document

Its gates found genuine integration and deployment problems. This supports the value of production-composition and delivery checks. It does not establish that nine artifacts and the complete gate stack were necessary to obtain those benefits.

Chillify demonstrates the central recommendation: keep the safeguards that found real runtime failures, but decouple them from a large permanent planning package.

### BegireX with early Brana

BegireX was created on 2026-07-08, before the public Brana 1.0 release. It should not be used as direct evidence against every current rule.

It remains useful as evidence of an early structural tendency:

- 20,463 initial planning words
- Nine initial artifacts
- Task document growth from 4,070 to 15,008 words
- Eight later remediation tasks

The newer workflow has addressed parts of this behavior, particularly evidence separation. The project still shows why plans, status, evidence, and remediation should not share one ever-growing canonical file.

### S2ORC with early Brana

S2ORC was created on 2026-07-14 and directly motivated several later workflow fixes.

Its UX document models command-line and console operations as screens with screen identifiers and wireframes. The newer operator-surface rule corrects this category mistake. This is a good example of Brana learning from use.

The broader lesson is about scope. The right fix was a conditional operator-interface rule. It did not need to increase the default burden for unrelated projects.

## Reference workflow comparison

### Superpowers: strong bounded execution

Superpowers' most relevant design choice is that the implementation plan remains the task source. It does not generate a second full task document that re-expresses the plan.

Its worker packet contains the current task and the context needed for that task. Its reviewer packet contains the task, implementation report, and concrete change. This makes context local and review evidence-rich.

Brana already adopted parts of this model, including interface blocks, explicit paths, and independent review. It did not adopt the same compression boundary. Contracts are still propagated through multiple planning layers.

### Compound Engineering: strong unified-artifact direction

Compound Engineering is not generally small. Its planning and work skills are themselves long. Its recent artifact redesign is still highly relevant.

The June 18 unified-plan proposal identifies:

- Requirements drift caused by artifact splitting
- Weak shareability
- Inefficient traceability
- The need for one canonical artifact enriched in place
- Stable requirement and work-unit identifiers
- A top-loaded goal capsule and definition of done
- Heading scans instead of full-plan reads
- Bounded active-unit packets
- Progress stored outside the plan

Its February 8 token-reduction plan also records context descriptions overflowing limits by roughly three times and moves toward progressive disclosure.

Brana adopted stamps and traceability ideas from this family of workflows, but retained the multi-artifact split that Compound Engineering later identified as a source of drift.

The best elements to borrow are:

- One canonical artifact
- Stable IDs
- Progressive reading
- Bounded unit packets
- Progress outside the plan

The persona and plugin bulk should not be copied.

## Root-cause synthesis

Brana's token problem is not caused by one verbose template. It emerges from four interacting design choices:

1. **Multiple authoritative documents.** The same facts are translated across phases.
2. **Duplicated operating instructions.** Workflow and skills restate one another.
3. **Monotonic safeguard growth.** Every failure adds permanent global process.
4. **Front-loaded assurance.** Detailed predictions are produced before implementation evidence exists.

These choices multiply:

```text
large instruction surface
    × many planning artifacts
    × full-document rereads
    × fresh phase/task contexts
    × status and evidence updates
    = high document traffic and synchronization cost
```

Brana copied valuable safety mechanisms from other workflows without consistently copying their compression and information-boundary mechanisms.

Its distinctive value is product verification. The value does not depend on having seven phases or nine documents.

## Recommended redesign

### Priority 0: change the information architecture

#### 1. Use one canonical plan for most projects

The plan should be enriched in place and contain:

- Goal and scope
- Kernel journey
- Product requirements and acceptance examples
- UX flows only where they add value
- Architecture decisions and risk contracts
- Stable implementation units
- Verification contract
- Definition of done

This removes translation layers while preserving traceability.

#### 2. Make visual design optional

Use a separate design document only for UI-heavy projects where a visual system, interaction specification, or asset direction deserves its own artifact. Do not create it for console tools, backend services, or minor interface changes.

#### 3. Stop generating a separate full `TASKS.md`

Implementation units should live in the canonical plan. A script can extract the active unit into a transient worker brief. This prevents PLAN-to-TASKS repetition and supports fresh, bounded contexts.

#### 4. Remove generated `FILE_STRUCTURE.md`

The real repository tree is the authority. Each work unit can list proposed new or changed files. A full predicted tree becomes stale quickly and duplicates discoverable information.

#### 5. Replace Full versus Lite with risk modules

Select controls based on present risks:

| Risk | Activated planning or verification |
|---|---|
| Payments or balances | Money representation, idempotency, concurrency, reconciliation |
| External systems | Wire contract, verified fake, failure behavior |
| Data migration | Rehearsal, rollback, compatibility window |
| UI-heavy product | UX flows, visual design, accessibility |
| Authentication or authorization | Threat model, session and permission checks |
| Operator surface | Commands, observability, recovery, delivery contract |
| Deployment composition | Production-path smoke test |

This preserves safety without loading unrelated policy.

### Priority 1: reduce execution overhead

#### 6. Use one default release product gate

The default product gate should evaluate the running release through its production composition. Add an intermediate gate only for a meaningful vertical slice, a high-risk decision, or an explicit user request.

#### 7. Move execution evidence out of normal planning history

Use a local ledger, CI artifacts, Git notes, external run records, or a final verification report. The canonical plan should not grow with every command result and status transition.

#### 8. Concentrate independent review on risky work

Review immediately and independently for:

- Payments
- Authentication and authorization
- Concurrency
- Migrations
- External integrations
- Security boundaries
- Production composition

Lower-risk interior work can use batch or final review. Review depth should follow consequence, not a fixed every-two-or-three-task rhythm.

#### 9. Size units by outcome and interface boundary

Keep units independently verifiable and cognitively bounded. Use expected line count only as a heuristic.

### Priority 2: shrink the workflow implementation

#### 10. Separate current truth from history

If an architecture document remains, keep it short and current. Move historical decisions to ADRs or solution notes loaded on demand.

#### 11. Use progressive skill disclosure

Create one small router or orchestrator skill. Load concise conditional references only when the selected risk or activity requires them.

`WORKFLOW.md` can remain the human-readable guide. Phase skills should not copy it. They should contain the minimum operational delta needed for that phase.

#### 12. Centralize deterministic checks

Put repeatable validation in one script or tool. Skills should invoke the check and interpret its result instead of restating the checklist in every instruction surface.

#### 13. Narrow dependency approvals

Require explicit approval for strategic, paid, unusually licensed, native, or high-risk dependencies. Let routine policy-compliant packages resolve during implementation, then verify them through the lockfile and automated checks.

### Priority 3: establish measurement before adding more rules

Track the following for comparable projects:

- Generated artifact words or tokens
- Mandated reread words or tokens
- Number of model turns and agent invocations
- Time from idea to first runnable slice
- Defects found before code
- Defects found during implementation and review
- Rework caused by stale generated documents
- Documentation-only commits
- Tokens spent per accepted feature

Run the same small and medium project through two workflow variants. Claims such as "cheapest per feature" should be made only after this measurement.

Every new workflow rule should state:

- The failure it prevents
- Which project risks activate it
- Its expected context and execution cost
- How its value will be measured
- When it should be removed or consolidated

## Suggested compact target workflow

A smaller Brana could use this sequence:

1. **Discover:** Clarify goal, kernel journey, boundaries, and open decisions.
2. **Plan:** Create one canonical plan with stable requirements, risk modules, implementation units, and definition of done.
3. **Execute:** Extract one bounded unit brief, implement it, verify it, and update a compact external ledger.
4. **Review:** Apply independent review proportional to risk, using the unit brief and concrete diff.
5. **Release:** Run one production-composition product gate and record the final result.
6. **Change:** Amend the canonical plan only where current truth changes; store historical decisions separately.

This keeps agent handoffs structured without making each handoff carry the full project history.

## What should not be removed

Reducing the workflow should not mean removing the controls that produced real value. The audit supports retaining:

- Kernel journey as the product anchor
- Explicit in-scope and out-of-scope boundaries
- User approval for visible scope cuts
- Acceptance examples for important behavior
- Production-composition checks
- Wire-level verification for external fakes
- Independent review of consequential changes
- Human inspection of the actual running release
- Stable requirement and work-unit identifiers
- A compact definition of done

These controls can fit inside a much smaller artifact and context model.

## Evidence map

### Brana repository

- Maintenance rule and workflow canon: `/home/dev/Documents/VAULT/WORKFLOW.md`
- Phase skills: `/home/dev/Documents/VAULT/skills/`
- Skill usage guide: `/home/dev/Documents/VAULT/skills/USAGE.md`
- Stale cost comparison: `/home/dev/Documents/VAULT/COMPARISON.md`
- Workflow history and audit documents: `/home/dev/Documents/VAULT/docs/history/`

Relevant workflow locations observed during the audit:

- `WORKFLOW.md:5`, maintenance rule
- `WORKFLOW.md:39`, token rules
- `WORKFLOW.md:98`, Route S
- `WORKFLOW.md:240`, Phase 2
- `WORKFLOW.md:388`, Phase 3
- `WORKFLOW.md:523`, Phase 4
- `COMPARISON.md:11`, artifact count
- `COMPARISON.md:20`, size claim
- `COMPARISON.md:27`, cheapest-to-run claim
- `COMPARISON.md:43`, cheapest-per-feature claim

### FAI Toolkit and Superpowers

- Design: `/home/dev/projects/fai-toolkit/docs/superpowers/specs/2026-07-30-api-management-platform-design.md`
- Plan: `/home/dev/projects/fai-toolkit/docs/superpowers/plans/2026-07-30-api-management-platform.md`
- SDD progress: `/home/dev/projects/fai-toolkit/.superpowers/sdd/2026-07-30-api-management-platform/progress.md`

Relevant SDD findings:

- `progress.md:50`, wallet lost-update hazard
- `progress.md:67`, proxy and metering issues
- `progress.md:76`, no-float plan contradiction
- `progress.md:96`, payment-poisoning vulnerability
- `progress.md:100`, gateway error handling
- `progress.md:133`, admin-name uniqueness

### Brana project artifacts

- Astryxs: `/home/dev/projects/astryxs-rtl-dashboard/`
- Chillify: `/home/dev/projects/chillify/`
- BegireX: `/home/dev/projects/begirex/`
- S2ORC: `/home/dev/projects/forgpt/codes/2026/files/s2orc/`

Relevant locations:

- Astryxs Task 0 waiver: `/home/dev/projects/astryxs-rtl-dashboard/specs/001-core/TASKS.md:5`
- Chillify historical architecture section: `/home/dev/projects/chillify/ARCHITECTURE.md:873`
- BegireX appended remediation tasks: `/home/dev/projects/begirex/specs/001-core/TASKS.md:402`
- S2ORC console-as-screen treatment: `/home/dev/projects/forgpt/codes/2026/files/s2orc/UX.md:58`

### Compound Engineering reference

- Unified-plan redesign: `/home/dev/Documents/VAULT/references/compound-engineering-plugin/docs/plans/2026-06-18-001-refactor-unified-plan-doc-artifact-plan.md`
- Token-reduction plan: `/home/dev/Documents/VAULT/references/compound-engineering-plugin/docs/plans/2026-02-08-refactor-reduce-plugin-context-token-usage-plan.md`
- Bounded work-unit guidance: `/home/dev/Documents/VAULT/references/compound-engineering-plugin/skills/ce-work/SKILL.md`

Relevant unified-plan locations:

- Line 11, artifact split causing drift and inefficient traceability
- Line 59, one canonical artifact
- Line 63, top-loaded reader contract
- Line 225, avoid reading the whole plan
- `ce-work/SKILL.md:170`, bounded unit packet

## Final assessment

Brana's engineering instincts are stronger than its current information architecture. The workflow correctly values scope discipline, production truth, external-system fidelity, and independent review. Those features likely explain why its gates found real problems in the sampled projects.

The token cost comes from treating each concern as another permanent document, phase, copy of instructions, gate, or evidence obligation. The resulting process is structured, but not simple. It creates more opportunities for synchronization and stale predictions than a professional multi-agent workflow needs.

The highest-leverage change is not another Lite exception. It is a redesign around one canonical plan, conditional risk modules, bounded task packets, external execution evidence, and review performed against concrete implementation. That would preserve Brana's product-quality advantage while making token use, handoffs, and maintenance materially smaller.
