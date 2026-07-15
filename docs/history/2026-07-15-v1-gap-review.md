# v1.0.0 gap review — 2026-07-15

Senior-engineer concept-level review of WORKFLOW.md and all 7 Brana skills, run against the published v1.0.0 release. Governing question: what makes apps built by this workflow hard to maintain or test? The review found 15 gaps (G1–G15). G1–G14 were found by the reviewer reading the workflow and skill files; G15 was found by the user in live use of the workflow, after the concept review had already concluded.

This document is the findings record. The remediation plan that answers each gap is `docs/superpowers/plans/2026-07-15-brana-gap-remediation.md`; this doc exists so the plan, the fix tasks, and the eventual CHANGELOG entry all have one place to point back to for "why."

## Gap → fix map

| # | Finding | Fix direction |
|---|---|---|
| G1 | Demo gates never become automated tests; Route A has zero product verification | Journey crystallization: after a gate's walkthrough passes, a crystallization task encodes that journey as an automated e2e test on the harness named in CONVENTIONS.md; journey suite joins the verify script; Route A runs verify (incl. journey suite) before merge |
| G2 | Acceptance criteria (journey-level) vs unit tests — nothing bridges | CONVENTIONS.md gains a required Test strategy section; Phase 4 tags every acceptance criterion with its verifying layer (`[unit]`, `[integration]`, `[contract]`, `[e2e@gate-N]`), making an e2e-tagged criterion machine-checkable against gate journeys |
| G3 | No seam/contract tests | Every task with a PRODUCES block ships a contract test asserting the exact produced shape/signature |
| G4 | Test quality never reviewed | 6a gains a finding category (7) test adequacy; reviewer input adds the tasks' acceptance criteria as the contract, not implementer claims |
| G5 | Verification evidence is self-reported prose | Evidence = command + captured output tail saved to `specs/NNN-name/evidence/task-N.txt`; TASKS.md done-mark references the file |
| G6 | No CI, no clean-checkout verification | Task 0 creates a single verify script (build+lint+typecheck+suite; journey suite once it exists), recorded in CONVENTIONS.md; agent mode wires CI to run verify if a remote exists; gate preflight runs verify |
| G7 | Error paths/NFRs untested until v1 exit; WCAG unverifiable | Each demo-gate journey appends one unglamorous step rotated from the PRD error/edge list; UI stacks add an automated a11y check to verify; DESIGN.md token table lists computed contrast ratios per fg/bg pair, checked ≥ AA at the consistency gate |
| G8 | Mechanical conventions enforced by prose review | Task 0 sets up linter/formatter/typecheck; CONVENTIONS.md rule: machine-checkable convention ⇒ lint rule; prose is reserved for what lint can't see; lint-green is a precondition to 6a |
| G9 | No learning loop into CONVENTIONS.md | Compound rule: same 6a finding class twice in a cycle → the fix task also adds a CONVENTIONS.md line or lint rule |
| G10 | No refactor/upgrade route | New Route R in Phase 7: refactor / dependency upgrade / debt, with journey suite + verify green before and after, behavior freeze, 6a on diff, doc sync |
| G11 | DESIGN.md tokens + FILE_STRUCTURE.md duplicate code truth | Code token file becomes the single source once Task 0 emits it, DESIGN.md keeps semantic roles and points to the file; FILE_STRUCTURE.md demoted to a per-cycle archived artifact in `specs/NNN-name/`, living navigational truth becomes the repo tree + code map |
| G12 | Patched living docs lose "why" | ARCHITECTURE.md gains an append-only Decision log section (`YYYY-MM-DD — decision — why`); Route C patches and doc sync append, patches never delete the why |
| G13 | Mid-cycle contract patch leaves stale CONSUMES/PRODUCES quotes in pending tasks | Escalation rule: after any contract patch, a cheap pass diffs old/new contract and updates the interface blocks of every not-done task quoting a changed section, before the next implementation session |
| G14 | Smaller: migrations, REVIEW_N.md location, parallel delegation | Migration tasks get up+down+up on fixture data with a data-preservation assertion, rollback = down migration never git revert; reviews live at `specs/NNN-name/reviews/REVIEW_N.md` with each finding becoming a TASKS.md fix task; delegate mode allows parallel only when file sets are disjoint and no dependency edge |
| G15 | Implementer works directly on main (user-found) | New Git Rule: Phase 5 step 0 checks the current branch; on main/master, create the cycle branch (named after the spec dir) before any code; direct-to-main only on explicit human instruction; Route A moves to a short-lived branch merged after verify green |

## Findings

### Big holes (testing)

**G1. Demo gates never crystallize into automated tests. Biggest hole.**

The kernel journey is walked by a human at every gate, forever. Nothing in any phase says "encode the walked journey as an e2e/integration test after it passes." Regression protection for the app's most important behavior is human labor, linear in gate count, forever. Post-v1 Route A commits to main with "full existing suite passes" — but the suite is only implementer-written unit tests; it never encoded the journeys. A Route A bugfix can silently break the kernel journey and nothing catches it until someone happens to walk it again. Phase 7 makes this worse: 6b runs only for Routes B/C — Route A has zero product verification.

**G2. Acceptance criteria and tests live at different altitudes; nothing bridges them.**

Criteria are journey-level observable behaviors ("restart app; items listed"). Phase 5 mandates "unit tests covering the acceptance criteria" — unit tests structurally cannot cover restart/persistence/navigation behaviors. So "test that actually drives the behavior" is aspirational; in practice the agent writes unit tests, marks acceptance verified via self-run, and the phrase papers over the gap. The workflow even names this failure ("code passes the tests it wrote for itself") but its only countermeasure is the manual gate from G1.

**G3. Seam bugs acknowledged, then left to manual gates.**

WORKFLOW.md admits "bugs live in the seams between well-tested tasks." Interfaces blocks quote CONSUMES/PRODUCES from ARCHITECTURE.md, but no mechanism verifies an implementation actually matches its PRODUCES quote — no contract tests, no integration-test requirement at seams. Two tasks both green-unit-tested can disagree on payload shape; the only catch is a demo gate, and only if the broken seam happens to lie on the walked journey. Non-journey seams (error paths, secondary flows) have no net at all.

**G4. Test quality is never reviewed.**

6a's finding categories: bugs, security, races, contract violations, convention violations, UI contracts. No category for "missing test", "test asserts nothing", "test mocks away the behavior under test." The implementer authors code + its tests in one prompt — classic self-grading — and the one reviewer in the loop is explicitly not asked to look at test adequacy. Diff-only review also can't see coverage gaps (what's absent isn't in the diff).

**G5. Verification evidence is self-reported prose.**

A done-mark is a commit SHA plus one line "what was exercised, what was observed" — written by the same agent that implemented. No artifact (test-run output, script, exit code). The v1 exit bar and demo gates trust TASKS.md marks written by agents, and agents demonstrably write plausible evidence lines for things they half-ran.

**G6. No CI anywhere.**

The whole system runs on one human's machine. "Full suite passes" is a session claim; nothing re-verifies on a clean checkout, so "works in the batch session, broken on fresh clone" ships. Also no build/lint/typecheck gate independent of any agent's honesty.

**G7. NFRs and error paths pile up untested until v1 exit.**

The PRD specs offline/error/edge cases; gates walk the kernel (happy) journey. The first forced check of restart/offline/error paths is the v1 exit bar — the most expensive possible moment to discover persistence is broken. WCAG AA is a "hard rule" whose verification mechanism is a reviewer reading a diff; contrast ratios need computation, not reading.

### Big holes (maintainability)

**G8. Mechanically checkable rules enforced by prose review — expensive and lossy.**

"Tokens only, no raw hex/px", naming conventions, folder rules: all lintable. No phase sets up eslint/prettier/typecheck/stylelint. Opus-tier reviews repeatedly catch what a free linter would catch deterministically.

**G9. No learning loop into CONVENTIONS.md.**

Review findings → fix tasks → done. Nothing routes a recurring 6a finding class back into CONVENTIONS.md or a lint rule; every batch pays for the same lesson. (The compound-engineering reference in `references/` is built around exactly this loop; Brana didn't take it.)

**G10. No refactor route; anti-refactor pressure by design.**

Phase 5: "no refactoring unrelated code", tasks ≤300 lines, write only task-listed files — correct for control, but Phase 7's routes are bugfix/small-feature/big-feature. A pure refactor fits none: no user-visible behavior (not B/C), too broad for one 300-line Route A task. No debt inventory either. Architecture accretes monotonically; the workflow structurally forbids the maintenance work that keeps apps maintainable. Dependency upgrades have the same problem: on paper they change nothing, so self-triage lands them in Route A — no review, no 6b.

**G11. Doc/code duplication built into the design, contradicting rule 5.**

"One source of truth per fact" — but DESIGN.md's token table holds exact values AND the code's token file holds them (except in pre-built-system mode). FILE_STRUCTURE.md is worse: the full tree is prophesied before any code exists, then "corrected by doc sync" forever — a drift-generation machine with near-zero read value once the repo exists. Doc sync catches drift only after merge; between merges the docs lie and any mid-feature impact analysis reads stale truth.

**G12. Patched living docs lose "why".**

ARCHITECTURE.md holds current truth, patched in place, no decision record. Six months of Route C patches later, impact analysis — the phase that most needs rationale — reads a doc that says what the boundaries are but not why. Judgment quality degrades exactly as the app grows. No ADR-equivalent anywhere.

**G13. Mid-cycle contract change doesn't invalidate pending tasks.**

Escalation to Route C patches quoted doc sections — but already-written TASKS.md entries carry frozen CONSUMES/PRODUCES quotes from the old contract. Nothing says re-derive remaining tasks' interface blocks. The isolated implementer is told to trust the block over neighbor code, so it will faithfully implement the stale contract.

### Smaller (G14)

- Schema migrations: Task 0 and Route C mention them; no up/down test, no data-preservation check. "Per-task rollback via git" is false comfort — git revert doesn't un-migrate a database.
- REVIEW_N.md location/lifecycle unspecified — not in the specs-dir convention; accumulates at root forever; findings→fix-task linkage untracked.
- Parallel delegation: two delegated tasks writing sibling files race; the workflow never mentions it.

### G15 (found by the user in live use)

The implementer never checks the current branch. If the branch is main, it implements directly on main. It should create/switch to a feature branch unless the human explicitly says to work on main.

## Shape of the whole

The workflow invests heavily in pre-code contract quality (phases 1–4, consistency gate) and human product judgment (6b), and delegates nearly all machine verification to implementer-written unit tests plus one diff review. Human walkthroughs are the load-bearing quality mechanism, and human labor is the one input that doesn't scale with app size. The missing layer is compiling human checks into machine checks: journeys→automated e2e, contracts→contract tests, conventions→lint rules, evidence→captured artifacts, findings→convention updates. Each is "compile the human check into a machine check once it passes" — the workflow has the compile source (falsifiable criteria, quoted contracts) but never compiles.
