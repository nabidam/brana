# Independent Review of the Brana v2 Workflow and Skills

**Date:** 2026-07-30  
**Reviewed revision:** `d9dfa1f` (`v2.0-token-efficiency`)  
**Comparison baseline:** `088f0e4` (`main`, Brana v1.12)  
**Prior findings checked:**

- `docs/2026-07-30-brana-workflow-audit.md`
- `ANALYSIS-brana-vs-superpowers.md`

## Executive verdict

The v2 redesign fixes the main architectural cause of Brana's token burn. The
workflow now has one canonical per-cycle plan, conditional risk sections,
three thin router skills, a persistent controller, bounded worker context,
risk-scoped review, one kernel e2e, and one mandatory product walkthrough.
Those changes directly address the document fan-out, instruction duplication,
session fragmentation, gate accumulation, line-count sizing, blanket
dependency approval, and stale living-document findings.

The measured instruction reduction is also real:

| Metric | v1.12 | v2 | Change |
|---|---:|---:|---:|
| `WORKFLOW.md` | 14,154 words | 2,598 words | −82% |
| Skills combined | 16,214 words | 918 words | −94% |
| Workflow + skills | 30,368 words | 3,516 words | −88% |
| Skill-to-workflow 8-word shingle overlap | 45% | 2.86% | target met |

However, the revision is not ready to ship through all advertised installation
paths. The router skills depend on files that skill-only installation does not
install, the ledger protocol requires a commit to contain its own SHA, and an
old synchronization script can recreate the five deleted v1 skill bundles.
The UI contrast gate is also invoked in a way that never reads `DESIGN.md`.

The existing `docs/2026-07-30-v2-review.md` therefore overstates the result when
it concludes that all findings are addressed. The redesign direction is
correct; the distribution and execution contract still need a focused cleanup.

## Findings

### 1. Skill-only installations omit the canon and gate executable

**Severity: high**

Every router skill requires the shared canon:

- `skills/brana-plan/SKILL.md:8-10`
- `skills/brana-build/SKILL.md:8-9`
- `skills/brana-ship/SKILL.md:8`

Planning and shipping also invoke `tools/brana-gate`:

- `skills/brana-plan/SKILL.md:28`
- `skills/brana-ship/SKILL.md:40-42`

But the documented direct installation copies only `skills/brana-*`
(`README.md:65-70`), excluding both root `WORKFLOW.md` and `tools/brana-gate`.
The cross-harness instructions repeat that users can copy only those skill
folders (`README.md:74-80`). The universal skill installer is likewise
presented as a skill installation, while no skill contains the shared canon or
tool as an asset.

As a result, a clean skill-only install gives the agent routers whose governing
instructions and required commands are absent. This is a functional regression
introduced by solving instruction duplication through an external shared file.

**Fix:** define and test one distribution layout in which all three skills can
resolve a packaged canonical workflow and gate executable from their installed
locations. Then make every installation method install that layout. Do not
solve this by restoring a full copy of the canon in every router.

### 2. A unit commit cannot contain its own final SHA

**Severity: high**

The ledger line must contain `id, status, SHA, date`, while the ledger must ride
in the same unit commit:

- `WORKFLOW.md:217-221`
- `skills/brana-build/SKILL.md:23-26`

A Git commit's SHA is computed from its tree and metadata. Writing that SHA
into a file in the same commit changes the tree and therefore changes the SHA.
The stated protocol is self-referential and cannot be completed truthfully.
Following it requires an amend loop, an incorrect SHA, or a separate
bookkeeping commit—the exact history friction the redesign says it removes.

This means the prior evidence/status-bookkeeping findings are only partially
resolved. Moving status out of `PLAN.md` is correct, but the replacement
protocol is not executable.

**Fix:** remove SHA from the committed ledger line and require the U-ID in the
commit subject so `git log` is authoritative, or keep the SHA ledger outside
the commit graph, such as Git notes or an uncommitted local controller ledger.

### 3. The retained sync script reverses the single-copy redesign

**Severity: medium**

`tools/sync-gate.sh:2-10` still instructs maintainers to copy
`tools/brana-gate` into the five deleted v1 skill directories. Running it will
recreate:

- `brana-3-plan`
- `brana-4-tasks`
- `brana-5-implement`
- `brana-6-review`
- `brana-7-change`

It therefore undoes the measured “six gate copies to one” improvement and
revives retired skill names. This conflicts directly with
`skills/README.md:18-20` and the v2 changelog.

**Fix:** delete this script or replace it with a check that fails if more than
one gate implementation exists.

### 4. The documented UI gate never scans `DESIGN.md`

**Severity: medium**

The workflow promises deterministic contrast computation when `DESIGN.md`
exists, but its exact command is:

```text
tools/brana-gate docs PLAN.md
```

This appears in `WORKFLOW.md:171-172` and
`skills/brana-plan/SKILL.md:27-28`. The gate only checks files explicitly
passed to it, and contrast parsing runs only when the current filename contains
`DESIGN` (`tools/brana-gate:560-603`, `tools/brana-gate:690-694`).

Consequently, the prescribed command never executes the promised contrast
check. The UI-heavy module also does not require the table shape the parser
expects, so even a manually supplied `DESIGN.md` can produce a silent
no-op.

**Fix:** when UI-heavy is active, require a parser-compatible contrast table
and invoke `tools/brana-gate docs PLAN.md DESIGN.md`.

### 5. Two risk-module triggers misclassify common work

**Severity: medium**

The external-system module activates only for a third-party service “that will
be faked in tests” (`WORKFLOW.md:103`). That makes the safety control depend on
a testing choice. A live or sandbox-only integration can avoid the module and
therefore avoid its wire contract, failure semantics, and immediate review.
The prior audit recommended activating those controls because an external
dependency exists; verified-fake obligations should be the conditional part.

In the other direction, the auth/user-data module includes all “external
input” (`WORKFLOW.md:106`). Almost every CLI, API, and interactive app accepts
external input, so this wording can turn a conditional security module into
default ceremony for ordinary projects.

**Fix:** trigger the external-system module on a runtime third-party boundary,
then condition only the fake-specific checks on use of a fake. Narrow the auth
module to authentication, authorization, personal/sensitive data, or an
identified hostile-input boundary; keep ordinary validation in the base
verification contract.

### 6. Routine dependency handling contradicts the execution hard stop

**Severity: medium**

The dependency section says routine, policy-compliant packages are selected by
the implementer during implementation (`WORKFLOW.md:287-289`). The execution
hard stop instead says any needed capability outside the plan's dependency
list must be proposed to the user (`WORKFLOW.md:202-207`).

The router and usage guide use the intended narrower rule—routine dependencies
are selected by the implementer, while the hard stop applies to strategic
dependencies (`skills/brana-build/SKILL.md:20-22`,
`skills/USAGE.md:29-32`). The canon therefore disagrees with its routers on an
operational decision, partially restoring the approval loop that the redesign
intended to remove.

**Fix:** make the canon's hard stop explicitly “a needed strategic dependency
outside the approved plan.” Routine additions should be reported and verified
through the lockfile and audit as §Dependencies already specifies.

### 7. Retired v1 machinery remains the repository's executable example and tool interface

**Severity: medium**

The v2 review acknowledges that the 723-line `tasks` subcommand is orphaned
(`docs/2026-07-30-v2-review.md:65-68`), but it remains the first and largest
part of `tools/brana-gate`'s help and implementation
(`tools/brana-gate:6-96`, `tools/brana-gate:120-557`). It documents retired
SPEC/TASKS files, full/lite profiles, scheduled gates, crystallization,
evidence paths, and phase numbers.

The only bundled example is also v1:

- `examples/dally/PROMPTS.md` invokes `brana-1-spec` through
  `brana-7-change`.
- `examples/dally/specs/*` contain SPEC/TASKS artifacts and no v2 `PLAN.md`.

Plugin metadata still advertises a seven-phase SPEC/UX/PRD/architecture/tasks
workflow:

- `.claude-plugin/plugin.json:3`
- `.claude-plugin/marketplace.json:11`

This makes the release internally inconsistent and leaves no runnable example
that proves the new plan, ledger, risk routing, or release path.

**Fix:** remove the orphaned task gate, migrate or archive Dally explicitly as
a v1 example, add one small v2 fixture cycle, and update both plugin
descriptions.

### 8. The removal policy cannot be evaluated from the required measurements

**Severity: low**

The maintenance rule says a rule that has not fired in three consecutive
cycles is a removal candidate (`WORKFLOW.md:15-18`). The measurement footer
records planning words, units, fix units, agent invocations, and optional
tokens (`WORKFLOW.md:308-315`), but it does not record which modules or rules
activated or fired.

The policy is directionally right but not auditable from the data the workflow
requires. This leaves the safety-ratchet finding partially addressed by intent
rather than mechanism.

**Fix:** add only the minimum data needed: active modules and exceptional rules
that actually fired. Avoid a per-rule checklist on every cycle; absence can be
derived for named conditional controls.

## Prior-audit resolution matrix

The following matrix uses the fifteen numbered findings in
`docs/2026-07-30-brana-workflow-audit.md`.

| Prior finding | Status | Review |
|---|---|---|
| 1. Artifact fan-out | Addressed | One canonical `PLAN.md`; conditional living docs have distinct access patterns. |
| 2. Workflow/skill authority duplication | Partial | Text duplication fell to 2.86%, but installed routers cannot reliably reach the authority. |
| 3. Safety ratchet | Partial | A removal policy exists, but its firing condition is not measured. |
| 4. Excess pre-implementation certainty | Addressed | File paths are hints, file-tree prediction is removed, and structure is deferred. |
| 5. Quality spending front-loaded | Addressed | Review now concentrates on diffs and running behavior; architecture review is risk-triggered. |
| 6. Evidence bookkeeping pollutes history | Partial | Evidence left the plan and separate commits disappeared, but the same-commit SHA ledger is impossible. |
| 7. Living documents become archives | Addressed | Current architecture and historical ADRs are separated explicitly. |
| 8. Full/lite is too blunt | Partial | Risk modules are the right model, but two triggers need correction. |
| 9. Line-count task sizing | Addressed | Units are bounded by outcome and interfaces. |
| 10. Interface blocks over-replicated | Addressed | Contracts live at producing units or risk boundaries and consumers reference them. |
| 11. Fresh sessions amplify context | Addressed in design | Persistent controller and path-based worker packets replace phase flushes. Distribution must still be fixed. |
| 12. Gate stack is cumulative | Addressed | One kernel e2e, one final walkthrough, and pull-based interim demos replace scheduled gates. |
| 13. Dependency approval is excessive | Partial | The tiers are separated, but the execution hard stop still asks about every out-of-plan dependency. |
| 14. Status/evidence consumes the task document | Partial | The plan stays clean, but ledger identity needs a workable protocol. |
| 15. Comparison claims are stale/unsupported | Addressed | Unsupported cost claims were retracted; project-level v2 savings remain correctly unclaimed. |

## Check against `ANALYSIS-brana-vs-superpowers.md`

The second analysis made one recommendation that the v2 self-review does not
account for: put complete code in the plan so the strong planner writes it
once. V2 explicitly chooses the opposite:

- low-level structure is decided during implementation
  (`WORKFLOW.md:41-43`);
- `brana-plan` says “Never write code here”
  (`skills/brana-plan/SKILL.md:35`).

This recommendation is therefore **not adopted**, not “addressed.” That is not
automatically a defect: the longer workflow audit warned that code-heavy plans
can be overprescriptive and recommended deferring low-level decisions. V2
reasonably sides with that audit and offsets re-derivation through smaller
plans, freely roaming read access, and bounded units.

The tradeoff should be explicit and measured. A representative v2 cycle should
compare prose-only units with one or two code-bearing high-risk unit briefs
before Brana adopts either position categorically.

The rest of the second analysis's direction is substantially implemented:

| Recommendation | Status |
|---|---|
| One decision-dense canonical artifact | Implemented, without a hard plan-size cap |
| Plan contains complete code | Not adopted; deliberate unresolved tradeoff |
| Persistent parent plus path-only workers | Implemented |
| Keep product demo gates, remove scheduled bureaucracy | Implemented |
| Replace consistency/task gates with inline self-review | Implemented |
| Stop restating workflow rules in skills | Implemented structurally; packaging is broken |
| Make lightweight ceremony the default | Replaced with the more precise risk-module model |

## Controls retained

The redesign retains the earlier audits' important keep-list:

- kernel journey and scope challenge;
- explicit user decision on visible scope cuts;
- falsifiable acceptance examples and measured NFRs;
- production-entry-point preflight;
- wire contracts and verified fakes when the module activates;
- migration rehearsal;
- independent review with reproduction before fixes;
- a kernel e2e in the normal verify path;
- a human walkthrough of the release build;
- current-truth architecture with ADR history;
- routine versus strategic dependency handling.

The controls are now far cheaper in instruction surface. Finding 5 should be
fixed before claiming that external-system coverage is preserved for every
relevant integration, and finding 4 before claiming deterministic UI contrast
coverage.

## Verification performed

- Recomputed line and word counts with `wc`.
- Recomputed normalized 8-word shingle overlap: 27 shared skill shingles out
  of 944, or 2.86%.
- Read the full v2 workflow, all three skills, usage and comparison docs,
  manifests, gate implementation, sync script, and bundled example.
- Confirmed `tools/brana-gate` compiles under Python 3.11.
- Inspected all non-history references to retired skills, artifacts, profiles,
  phases, and gate commands.

No v2 end-to-end workflow run was possible from this repository because it
contains no v2 example plan or fixture. Instruction-surface savings are
measured; project-level token savings and behavioral quality remain unproven,
as the existing v2 review correctly notes.

## Recommended release order

1. Fix the install/package contract and the self-referential ledger.
2. Remove the reverse-sync script and retired task-gate surface.
3. Correct UI gate invocation and risk triggers.
4. Migrate one example to v2 and exercise plan → build → ship from a clean
   installation.
5. Collect the first cycle metrics before making any project-level cost claim.

After those changes, the redesign would satisfy the substance of the main
audit while documenting—rather than silently omitting—the one material
recommendation from the Superpowers comparison that it chose not to adopt.
