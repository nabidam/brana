# Brana Skills

One skill per phase of `WORKFLOW.md` (Brana v1.1). Run each phase in a **fresh session**; Phase 5 runs one session per 2–3-task batch, cleared at each demo gate.

| Skill | Phase | Reads | Writes |
|---|---|---|---|
| `brana-1-spec` | 1 | your idea | `specs/NNN-name/SPEC.md` (kernel/v1/backlog + kernel journey) |
| `brana-2-prd-arch` | 2 | SPEC.md | `UX.md`, `specs/NNN-name/PRD.md`, `ARCHITECTURE.md` |
| `brana-3-plan` | 3 | PRD.md, ARCHITECTURE.md, UX.md | `specs/NNN-name/PLAN.md`, `CONVENTIONS.md`, `DESIGN.md`, `FILE_STRUCTURE.md` + consistency gate |
| `brana-4-tasks` | 4 | PLAN.md, ARCHITECTURE.md, UX.md, PRD.md (error/edge-case list) | `specs/NNN-name/TASKS.md` (incl. demo-gate tasks) |
| `brana-5-implement` | 5 | task N + context pack | code + tests + commit, demonstrated |
| `brana-6-review` | 6a/6b | git diff + contracts / running app | `specs/NNN-name/reviews/REVIEW_N.md` / gate walkthrough (+ optional screenshots) |
| `brana-7-change` | 7 | change request + living docs | routed cycle (A/B/C/R) + doc sync |

Every skill has two modes (brana-5 adds `delegate`):

- **run** (default): execute the phase here in Claude Code — the workflow's Agent Adaptation Layer applies (reading roams, writing doesn't; gates are soft stops; scope cuts are hard stops).
- **prompt** (pass `prompt` as argument): output paste-ready prompt block(s) — with actual file contents embedded — for an external chat UI, then stop. Copy-paste is the workflow's canon medium; this preserves its cross-vendor and model-tier economics.

Living docs at repo root: `ARCHITECTURE.md`, `UX.md`, `CONVENTIONS.md`, `DESIGN.md` — patched, never regenerated, no "deviations" ledgers. Per-cycle docs (`SPEC.md`, `PRD.md`, `PLAN.md`, `TASKS.md`, `FILE_STRUCTURE.md`) are archived under `specs/NNN-name/` (v1 = `specs/001-core/`, gate screenshots in `specs/NNN-name/screenshots/`) and carry a `status:` frontmatter stamp (`draft` → `gate-passed`; TASKS.md `ready`) — a consuming phase refuses a doc whose gate hasn't cleared. `FILE_STRUCTURE.md` is a per-cycle prediction only, never a living doc and never stamped.
