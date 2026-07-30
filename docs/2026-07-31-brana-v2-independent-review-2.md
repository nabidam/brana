# Brana v2 Independent Review — Second Pass

**Date:** 2026-07-31

**Reviewed range:** `d9dfa1f..17134de`

**Fix commits:** `ad44c7a`, `17134de`

**Prior review:** `docs/2026-07-30-brana-v2-independent-review.md`

## Verdict

The repair pass materially improves the v2 release. The two original
high-severity defects are no longer present in their original forms:

- a clean three-skill copy contains a byte-identical canon and gate executable;
- ledger rows no longer try to contain the SHA of their own commit.

The distribution check passes, the bundled files match their sources, the
retired task-gate implementation is gone, the contrast check now runs against
`DESIGN.md`, the corrected risk triggers are in the canon, plugin metadata is
current, and the removal-policy measurements are recordable.

The result is not fully closed. The skill trigger descriptions still use v1's
phase numbering and route v2 phase requests to the wrong skills. The new
ledger identity is ambiguous after the second cycle, the build router retains
the broad dependency hard stop that the canon removed, and the new v2 example
does not pass the workflow's semantic self-review despite passing the narrow
gate script.

Status of the first review's eight findings:

| Finding | Second-pass status |
|---|---|
| 1. Skill-only install omitted canon and gate | Fixed for the documented install-all-three layout |
| 2. Same-commit SHA ledger was impossible | Original defect fixed; replacement identity has a multi-cycle collision |
| 3. Sync script recreated deleted bundles | Fixed |
| 4. UI contrast command omitted `DESIGN.md` | Fixed and independently reproduced |
| 5. Risk-module triggers misclassified work | Fixed in the canon |
| 6. Dependency tiers contradicted the hard stop | Partially fixed; canon corrected, build router still broad |
| 7. Retired v1 machinery remained operational | Partially fixed; tool/example labeling/metadata fixed, skill triggers still use v1 phases |
| 8. Removal policy was not measurable | Fixed |

## Findings

### 1. Skill descriptions route v2 phase numbers to the wrong skills

**Severity: high**

The v2 canon defines:

1. Discover
2. Plan
3. Execute
4. Review
5. Release
6. Change

The skill descriptions still describe the retired seven-phase workflow:

- `skills/brana-plan/SKILL.md:3` triggers on “any Brana phase 1–4.”
- `skills/brana-build/SKILL.md:3` triggers on phases 5 or 6.
- `skills/brana-ship/SKILL.md:3` says it covers phases 6b–7.

These are operational trigger fields, not historical prose. Under v2:

- “phase 3” or “phase 4” should route to `brana-build`, but advertises
  `brana-plan`;
- “phase 5” or “phase 6” should route to `brana-ship`, but advertises
  `brana-build`;
- phases 6b and 7 no longer exist.

This leaves the most consequential v1 residue—the automatic router—unchanged
even though the plugin metadata and examples were corrected.

**Fix:** rewrite the descriptions around v2 step names and numbers:
`brana-plan` = Discover/Plan (1–2), `brana-build` = Execute/Review (3–4),
`brana-ship` = Release/Change (5–6). If legacy aliases are retained, label
them explicitly as v1 aliases so they do not redefine v2 numbering.

### 2. U-ID-only commit lookup becomes ambiguous after one cycle

**Severity: medium**

The new ledger protocol uses a repeated local unit ID in the commit subject:

- `WORKFLOW.md:226-233`
- `skills/brana-build/SKILL.md:25-30`

Every cycle starts again with U1, U2, and so on. After two cycles,
`git log --grep "\[U1\]"` returns at least two commits and is no longer an
authority for which commit completed the current cycle's U1. A branch point
can narrow the query during an active branch, but the protocol does not record
or require one, and post-merge reconstruction remains ambiguous.

The example ledger introduces a related ambiguity:
`examples/notes-v2/.brana/ledger.md:4` contains an `in-progress` U2 row, while
the canon says the ledger line rides in the unit's completion commit. An
in-progress row either remains uncommitted, rides in another unit's commit, or
needs a separate bookkeeping commit; the workflow does not choose.

The self-referential SHA defect is fixed, but state reconstruction is not yet
well-defined across cycles and intermediate states.

**Fix:** make the commit marker cycle-qualified, for example
`[001-core/U3]`, and require that same cycle ID in the ledger header. Define
the committed ledger as terminal unit records only; if an in-progress row is
useful, state explicitly that it is working-tree controller state and is
replaced by the terminal row in the unit commit.

### 3. The build router still stops on every out-of-plan dependency

**Severity: medium**

The canon now correctly limits the hard stop to a strategic-tier dependency:

- `WORKFLOW.md:209-216`

The build router still says:

> `out-of-plan dependency → stop and ask`

at `skills/brana-build/SKILL.md:22-24`, followed by “Routine deps:
implementer picks and reports.” Those two statements conflict inside the same
step. An agent can reasonably obey the first sentence and restore the blanket
approval loop the fix was meant to remove.

The addendum's claim that the canon/router contradiction is fixed
(`docs/2026-07-30-v2-review.md:101`) is therefore premature.

**Fix:** change the router phrase to “out-of-plan strategic-tier dependency.”

### 4. The v2 example violates the canon's coverage and risk-selection rules

**Severity: medium**

The example is presented as a “minimal but complete” shape reference
(`examples/README.md:3-7`), but its plan has two semantic violations that the
model self-review is required to catch.

First, the canon requires every requirement to map to a unit
(`WORKFLOW.md:170-171`). The example's R4 cold-start NFR is measured in the
walkthrough (`examples/notes-v2/specs/001-core/PLAN.md:28,72`) but neither U1
nor U2 owns R4 or its measurement mechanism
(`examples/notes-v2/specs/001-core/PLAN.md:44-56`).

Second, the auth/user-data module triggers on stored personal/sensitive data
(`WORKFLOW.md:110`). The example says no module is active because there is no
personal data “beyond local notes”
(`examples/notes-v2/specs/001-core/PLAN.md:30-34`). That wording acknowledges
that the app stores user-authored notes while treating them as exempt from the
trigger. Either the module should be active or the canon should explicitly
scope local-only content out of the trigger.

`brana-gate docs` passes because it checks placeholders and contrast, not
semantic requirement coverage or risk routing. The passing script result
therefore does not validate the example's claimed completeness.

**Fix:** assign R4 and its measurement script to a unit. Then either activate
the user-data module with a compact local-data threat section, or clarify the
trigger in the canon and explain why local-only notes do not activate it.

### 5. The distribution drift check is not part of a required verification path

**Severity: low**

`tools/check-dist.sh` correctly detects source/bundle drift and extra copies,
and it passes on the reviewed tree. It is mentioned descriptively in README
and `skills/README.md`, but it is not required by `CONTRIBUTING.md`, a release
script, or CI. No `.github` workflow exists.

The bundle is now a load-bearing installation artifact. A guard that is never
required can silently stop guarding on the next edit.

**Fix:** add `tools/check-dist.sh` to the contributor/release verification
contract or CI. The script itself does not need more complexity.

### 6. The post-fix metrics and limitations describe the pre-repair tree

**Severity: low**

`docs/2026-07-30-v2-review.md` received an addendum but its headline metrics
and limitations were not recalculated or marked as a historical snapshot:

- lines 15–19 report 315 workflow lines, 119 skill lines, and one gate copy;
- the current tree has 330 workflow lines, 131 skill lines, and one source
  plus one bundled gate copy;
- lines 65–68 still say the task implementation remains orphaned;
- lines 74–76 still say installed-skill synchronization is pending.

The addendum later says these issues were fixed, so the same document now
contains incompatible current-state claims. The corrected source instruction
surface remains strong—3,859 words versus 30,368, a reduction of about
87%—but the record should distinguish the original `d9dfa1f` snapshot from the
post-repair numbers.

**Fix:** label the original table and limitations explicitly as the
`d9dfa1f` snapshot, then add a compact post-repair table. Count “source +
bundle” separately from “canon loaded per agent session” so repository copies
and runtime context are not conflated.

## Independently confirmed repairs

### Distribution

- `tools/check-dist.sh` passes.
- Root and bundled `WORKFLOW.md` files are byte-identical.
- Root and bundled gate scripts are byte-identical and executable.
- A clean temporary copy containing only `brana-plan`, `brana-build`, and
  `brana-ship` resolved both sibling paths and ran the bundled gate
  successfully against the v2 plan.
- `tools/sync-gate.sh` is deleted.

The qualification matters: `brana-build` and `brana-ship` are not individually
self-contained; the documented three-skill set is.

### Ledger repair

The impossible same-commit SHA field is gone from the canon, build skill, and
example ledger. Commit subjects now carry unit IDs and the ledger rows contain
only ID, status, and date. Finding 2 above concerns uniqueness and intermediate
state, not the original self-reference.

### Gate behavior

- Both gate copies compile under Python 3.11.
- `brana-gate docs` passes on the root and bundled canons.
- `brana-gate docs` passes on the v2 example plan.
- A synthetic `DESIGN.md` with `#777777` on `#FFFFFF` was independently
  rejected at 4.48:1, confirming the corrected contrast invocation and parser
  shape.
- A synthetic plan containing a placeholder token was rejected.
- Calling the retired `tasks` subcommand returns exit code 2 with a v2
  migration message; the 500-plus-line v1 implementation is gone.

### Workflow corrections

- External-system activation now follows a runtime third-party boundary;
  fake-specific obligations are conditional.
- Auth/user-data activation no longer includes every ordinary input.
- The canon's dependency hard stop is strategic-only.
- The measurement footer now records active modules and exceptional rules
  that fired.
- A soft ~2,500-word plan budget addresses the unbounded-single-document risk.
- Plugin and marketplace descriptions now describe v2.
- Dally is clearly labeled as an archived v1 example.
- The code-in-plan recommendation is recorded as intentionally unadopted and
  pending measurement, rather than incorrectly marked resolved.

## Updated assessment against the original audits

The redesign still satisfies the central direction of both earlier audits:

- one canonical plan instead of nine transformed artifacts;
- conditional risk controls instead of full/lite bundles;
- persistent controller and bounded worker packets;
- implementation-time structure instead of speculative file trees;
- review against concrete diffs;
- one kernel e2e and one mandatory release walkthrough;
- routine dependency autonomy;
- current architecture separated from ADR history;
- measured cost claims and a removal policy.

Current source instruction size is:

| Surface | Lines | Words |
|---|---:|---:|
| `WORKFLOW.md` | 330 | 2,838 |
| Three router skills | 131 | 1,021 |
| Combined source instructions | 461 | 3,859 |

That is an approximately 87% word reduction from the 30,368-word v1.12
workflow-plus-skills baseline. Router-to-canon 8-word shingle overlap is now
2.26%, below the 10% target. The bundled canon is a byte-identical
distribution artifact and is not read in addition to the root canon during a
normal session, but it should be counted when reporting physical repository or
package size.

Project-level token savings and quality remain unproven. The new notes fixture
tests artifact and gate shape, not plan → implementation → review → release
from a clean install. That limitation is correctly retained in the addendum.

## Release recommendation

The packaging blocker from the first review is cleared. Before tagging or
merging v2, fix findings 1–4:

1. correct the skill trigger descriptions;
2. cycle-qualify ledger/commit IDs and define in-progress state;
3. narrow the build router's dependency stop;
4. make the v2 reference plan semantically conform to the canon.

Findings 5–6 are documentation and maintenance hardening. They need not reopen
the architecture, but resolving them now will keep the next release from
reintroducing the same source/bundle drift and current-truth ambiguity that v2
was designed to remove.
