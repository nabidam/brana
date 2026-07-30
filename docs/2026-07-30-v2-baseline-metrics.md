# v2 Baseline Metrics (pre-fix snapshot, v1.12)

Captured 2026-07-30 on `main` (088f0e4) before the v2.0 rewrite. These are the
numbers the post-fix review must be compared against. All counts via `wc`;
overlap via 8-word shingle intersection (same method as the workflow audit).

## Instruction surface

| Source | Lines | Words |
|---|---:|---:|
| WORKFLOW.md | 908 | 14,154 |
| 7 phase skills combined | 923 | 16,214 |
| skills/USAGE.md | 196 | 3,646 |
| COMPARISON.md | 56 | 929 |
| **Total instruction surface** | **2,083** | **34,943** |

Duplication: **45%** of the skills' distinct 8-word sequences also appear in
WORKFLOW.md (6,293 of 14,082 shingles) — two operational authorities for one
process.

`brana_gate.py` (723 lines) is bundled **5 times** (skills 3, 4, 5, 6, 7) plus
`tools/brana-gate` — 6 copies of the same file in the repo.

## Mandated process structure (full profile)

| Dimension | v1.12 value |
|---|---|
| Planning artifacts per cycle | 9 (SPEC, UX, PRD, ARCHITECTURE, PLAN, DESIGN, CONVENTIONS, FILE_STRUCTURE, TASKS) |
| Phases / skills | 7 |
| Gate types | architecture review, consistency gate, task gate, per-task verify+evidence, 6a per 2–3 tasks, mid demo gates (1 per 8–10 feature tasks), crystallization step per gate, release gate |
| Sessions mandated | fresh per phase, per 2–3-task batch, cleared at each gate |
| Per-task bookkeeping | evidence file + SHA done-mark + coverage citations, all in TASKS.md |
| Profile routing | binary full/lite + retro-lite valve |

## Observed project cost (from the two audits)

| Project | Workflow | Initial planning words | Current planning words | Doc-traffic proxy |
|---|---|---:|---:|---:|
| fai-toolkit | superpowers | 6,963 | — | ~8,000 |
| astryxs | brana lite v1.12 | 8,702 | 8,908 | ~26,000 |
| begirex | brana (early) | 20,463 | 31,464 | ~94,000 |
| s2orc | brana (early) | 24,990 | 25,633 | ~118,000 |
| chillify | brana full | 26,802 | 38,628 | ~123,000 |

## Findings the v2 rewrite must address

From `ANALYSIS-brana-vs-superpowers.md` + `docs/2026-07-30-brana-workflow-audit.md`
+ the gate-cost discussion:

- F1 — artifact fan-out: 9 authoritative docs re-expressing the same facts
- F2 — WORKFLOW/skills duplicate authority (45% overlap)
- F3 — safety ratchet: rules only added across 12 versions, never removed
- F4 — front-loaded assurance: implementation detail predicted before evidence
- F5 — gate + crystallization stack is the largest execution-phase token sink
- F6 — evidence bookkeeping pollutes planning docs and git history
- F7 — living docs accumulate history (chillify ARCHITECTURE.md 38% archive)
- F8 — binary full/lite bundles unrelated controls
- F9 — line-count task sizing is a weak proxy
- F10 — interface contracts restated across ARCHITECTURE/PLAN/TASKS
- F11 — mandated session flushes defeat prompt caching
- F12 — dependency approval loop heavier than routine picks need
- F13 — COMPARISON.md carries stale/unmeasured cost claims
- F14 — no measurement policy; rules added without cost/benefit evidence

## Post-fix acceptance targets

- One canonical per-cycle artifact; conditional extras only via risk modules
- Instruction surface (workflow + skills) under ~40% of baseline words
- Skill↔workflow shingle overlap under ~10%
- One copy of the gate script in the repo
- No mandated session flush; persistent controller + bounded subagent packets
- Gates: walking skeleton + one kernel e2e + final walkthrough; mid gates pull-based
- Evidence outside planning docs
- Every rule carries activation condition; removal policy stated
- COMPARISON.md cost claims corrected or marked unmeasured
