# Brana v2 Independent Review — Final Pass

**Date:** 2026-07-31

**Reviewed range:** `17134de..e45dd70`

**Fix commit:** `e45dd70`

**Prior review:** `docs/2026-07-31-brana-v2-independent-review-2.md`

## Verdict: PASSED

No high- or medium-severity findings remain in the reviewed changes. All six
findings from the second independent review are resolved, the two bundled
distribution artifacts match their sources, the documented clean-install
layout works, and the repository's required checks pass.

This pass means the v2 workflow and skill distribution are internally
consistent and ready to merge or tag. It does not convert the still-unmeasured
project-level token and quality claims into evidence; those correctly remain
open until a real v2 cycle records its metrics.

## Second-review closure

| Second-review finding | Final status | Confirmation |
|---|---|---|
| 1. V1 phase numbers routed v2 requests incorrectly | Fixed | Skill descriptions now lead with v2 steps 1–2, 3–4, and 5–6. Legacy phase names are explicitly labeled v1 aliases rather than v2 numbering. |
| 2. Bare U-IDs collided across cycles; in-progress ledger state was undefined | Fixed | Commit markers are cycle-qualified (`[001-core/U3]`); ledger headers identify the cycle; committed rows are terminal-only; in-progress state is explicitly uncommitted. |
| 3. Build router retained the blanket dependency stop | Fixed | `skills/brana-build/SKILL.md` now stops only for an out-of-plan strategic-tier dependency and explicitly permits routine picks. |
| 4. The v2 fixture violated requirement coverage and risk routing | Fixed | R4 and its measurement belong to U2; the auth/user-data trigger and fixture consistently exclude local-only single-user content. |
| 5. Distribution integrity check was not required anywhere | Fixed | `CONTRIBUTING.md` defines the required commands and `.github/workflows/check.yml` runs them on pushes and pull requests. |
| 6. Post-fix review mixed historical and current measurements | Fixed | The original table and limitations are labeled as the `d9dfa1f` snapshot; Addendum 2 records current source metrics and distinguishes source, bundle, and session context. |

## Independent verification

### Source and distribution integrity

- `bash tools/check-dist.sh` passes.
- Root `WORKFLOW.md` and
  `skills/brana-plan/reference/WORKFLOW.md` are byte-identical.
- Root `tools/brana-gate` and
  `skills/brana-plan/scripts/brana_gate.py` are byte-identical and executable.
- No extra canon or gate copy is reported.
- A clean temporary install containing only the documented three-skill set
  resolved the sibling canon and gate paths successfully.
- The bundled gate ran successfully against the v2 example plan from that
  clean install.

### Required checks

The commands now required by `CONTRIBUTING.md` and CI all pass locally:

```text
bash tools/check-dist.sh
python3 -m py_compile tools/brana-gate skills/brana-plan/scripts/brana_gate.py
python3 tools/brana-gate docs WORKFLOW.md skills/*/SKILL.md examples/notes-v2/specs/001-core/PLAN.md
```

The GitHub Actions workflow uses the same checks with Python 3.12. Its event
and job structure is valid for pushes and pull requests.

### Gate behavior

- The current canon, all three router skills, and the v2 fixture pass the docs
  gate.
- The retired `tasks` subcommand exits with code 2 and a clear v2 migration
  message; no v1 task-gate implementation remains.
- The previously repaired contrast behavior remains intact from the second
  review's independent reproduction.

### Metrics

The current measurements in `docs/2026-07-30-v2-review.md` match the tree:

| Surface | Lines | Words |
|---|---:|---:|
| `WORKFLOW.md` | 335 | 2,902 |
| Three router skills | 134 | 1,078 |
| Combined source instructions | 469 | 3,980 |

That is approximately 87% fewer words than the 30,368-word v1.12
workflow-plus-skills baseline. Recomputed router-to-canon 8-word shingle
overlap is 2.22%, still well below the 10% target.

## Review of the repaired contracts

### Skill routing

The current descriptions have one unambiguous primary route:

- `brana-plan` — v2 Discover and Plan;
- `brana-build` — v2 Execute and Review;
- `brana-ship` — v2 Release and Change.

Backward-compatible v1 aliases are explicitly qualified as legacy names. This
satisfies the second review's requirement without redefining v2 numbering.

### Ledger

The ledger no longer contains self-referential SHAs or globally ambiguous bare
unit markers. Cycle-qualified subjects make Git history the commit authority,
while terminal-only committed rows keep status updates in the unit commit.
The example ledger follows the same protocol.

### Risk routing and example

The auth/user-data trigger now has a concrete trust-boundary distinction:
local-only single-user content remains base-workflow scope, while multi-user,
synced, network-accessible personal data and hostile boundaries activate the
module. The notes fixture states the same boundary.

Every example requirement now maps to implementation work. U2 owns the
cold-start measurement mechanism and R4 acceptance, while the release
walkthrough re-measures the budget as required.

### Maintenance controls

The source/bundle duplication required for skill-only installation is
deterministically controlled rather than maintained by instruction alone.
Contributor guidance now treats skills as routers, requires source/bundle
checks, and avoids the old “change the rule in both places” duplication rule.

## Non-blocking observations

These do not prevent the pass:

1. The example ledger records `planning words: 430`, while a plain `wc -w` on
   its current `PLAN.md` reports 453. Token/word counting methods can differ,
   but future measured cycles should name the counting command so comparisons
   use one definition.
2. CI exercises the positive docs-gate path but has no committed negative
   contrast fixture. The contrast parser works now and was independently
   reproduced in the previous review; a small regression fixture would be
   useful if that script changes again.
3. A bare, versionless phrase such as “Brana phase 3” remains inherently
   ambiguous between current v2 numbering and a legacy v1 alias. The
   descriptions correctly prioritize and label v2; repositories still using
   v1 should identify themselves through their SPEC/TASKS artifact shape or
   say “v1.”

None of these observations changes behavior in the reviewed release or
reopens the workflow architecture.

## Final assessment

The redesign now satisfies the substance of the two original audits and the
two independent follow-up reviews:

- one canonical plan rather than a graph of transformed artifacts;
- risk-triggered ceremony rather than full/lite bundles;
- persistent controller and bounded worker packets;
- outcome-based units and implementation-time structure;
- risk-scoped review against concrete diffs;
- one kernel e2e and one mandatory release walkthrough;
- executable, cycle-safe progress bookkeeping;
- a self-contained three-skill distribution with automated drift checks;
- current-truth documentation and measured cost governance.

**Final status: PASSED.**
