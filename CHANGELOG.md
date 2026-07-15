# Changelog

## Unreleased

Demo gates made runnable by construction — fixes gates landing at points where the app can't launch or the journey isn't walkable:

- **Phase 3:** gate placement rule changed from pure cadence to cadence-as-target + runnability-as-constraint; gate intervals must be vertical slices; every DEMO GATE entry carries runnability preconditions (launch command, seed data, serving chunk per journey step; a disposable/fixture path when the journey would otherwise touch production state). Consistency-gate machine pass now also checks PLAN.md: unserved gate journey steps and missing preconditions are blocking findings.
- **Phase 4:** demo-gate tasks carry a preflight block (build/launch command, seed command, dependency task ids); a journey step with no implementing task before its gate is a blocking finding.
- **Phase 5/6b:** agent preflights every gate (build, launch, journey entry reachable) before the soft stop; failure is the new `GATE BLOCKED` state — fix tasks at head of queue, re-preflight, only then invite the walkthrough. Unresolved `GATE BLOCKED` fails the v1 exit bar outright.
- **Task 0:** scaffold's smoke test is now "app boots via documented run command" (recorded in CONVENTIONS.md).

## 1.0.0 — 2026-07-12

First public release as **Brana**. Skills renamed `wf-N-*` → `brana-N-*`. Added README, LICENSE (MIT), CONTRIBUTING, Claude Code plugin manifest, and a public-facing COMPARISON.md.

### Pre-release lineage (internal versions)

- **v2.2** — folded in five tested patterns from [Superpowers](https://github.com/obra/superpowers) and [Compound Engineering](https://github.com/EveryInc/compound-engineering): path-based delegation, task interface blocks (CONSUMES/PRODUCES), live verification evidence + commit-SHA ledger, reviewer independence, and `status:` frontmatter stamps with downstream refusals. Plus Phase 1 brainstorming moves (decomposition, ask-first interviewing, multi-approach proposals, integration check, spec self-review). Made per-task visual verification opt-in.
- **v2.1** — added DESIGN.md as the fourth Phase 3 living doc (design-system contract; fixes incoherent AI-generated UIs); synced skills to canon.
- **v2.0** — consolidated from 5 agent proposals after a v1 post-mortem: 7-phase structure, kernel journey, demo gates, consistency gate, living-doc model, model-tier bindings, copy-paste canon.
