# How Brana Compares

Brana (WORKFLOW.md v1.0 + `skills/brana-1…7`) side by side with two excellent public workflows we studied closely and borrowed from: [**Superpowers**](https://github.com/obra/superpowers) (Jesse Vincent / prime-radiant) and [**Compound Engineering**](https://github.com/EveryInc/compound-engineering) (Every). Both are strong projects worth your time — this document explains where each shines and which bet Brana makes differently. Written 2026-07-12.

## At a glance

| Dimension | Brana | Superpowers | Compound Engineering |
|---|---|---|---|
| Core bet | Contract docs + human demo gates | Behavioral discipline skills | Compounding knowledge loops |
| Phases | 7 fixed (spec→…→change loop) | 5-ish, chained by terminal states | 6 (brainstorm→…→compound) |
| Artifacts | 4 per-cycle + 5 living docs | Design doc + plan | 1 mutating unified plan |
| Handoff gate | Consistency gate + `status:` stamps | User approval gates | Readiness frontmatter contract |
| Product review | **6b demo gate (human, running app)** | None | None |
| Scope discipline | **Kernel journey + scope challenge** | YAGNI + decomposition | Tier-sized ceremony |
| Model tiering | Concrete bindings table | Per-dispatch, explicit | Named semantic tiers |
| Delegation | Path-based, opt-in | Core mechanism (SDD flagship) | Core mechanism (persona panel) |
| Code review | 1 reviewer, different model, 6 categories | 2-stage (spec + quality) per task | 6–13 personas, diff-selected |
| Learning persistence | Doc sync (contract truth only) | None | **docs/solutions/ + validation** |
| Portability | **Copy-paste canon, any chat UI** | Multi-harness plugin | Converter + per-harness files |
| Size | ~600 lines total | ~15 skills, mostly short | 29 skills, 300–800 lines each |
| Human role | High: reads docs, walks gates | Medium: approves design/spec | Low–medium: confirms scope, `/lfg` near-autonomous |

## Strengths and trade-offs

| Workflow | Strengths | Trade-offs |
|---|---|---|
| **Brana** | The only one of the three with product-level verification (the 6b demo gate) and a hard v1 exit bar; cheapest to run (fresh sessions, diff-only review, model-tier bindings); works with zero tooling (copy-paste canon); a dedicated UX.md artifact; a hard-stop rule for scope cuts; status stamps, verification evidence, task interface blocks, path-based delegation | No lesson persistence yet (doc sync keeps contracts true, but doesn't capture *why* bugs happened); single reviewer vs. their multi-perspective panels; no TDD enforcement; discipline rules aren't bulletproofed with rationalization tables; younger and less battle-tested than either reference |
| **Superpowers** | Best-in-class skill-writing craft (description-as-trigger, form-matches-failure, eval-tested wording); the strongest anti-rationalization machinery (Iron Laws, red-flag tables); subagent-driven development with a context firewall; rigorous verification-before-completion | Focused on code, not products — no UX/product layer, design-system contract, or post-v1 change loop; TDD everywhere costs tokens on trivial work |
| **Compound Engineering** | The learning loop genuinely compounds (solutions store + grounding validation + discoverability checks); best token-efficiency machinery (evidence dossiers, repo-profile cache, read budgets); review panel that right-sizes to the diff; anti-false-agreement and cross-model adversarial passes | Heavyweight: 800-line skills, per-harness duplication, converter machinery; `/lfg` autonomy trades away human product judgment; one mutating plan doc is weaker than doc-per-concern for big builds; no visual/UX verification |

## Three different bets

Each workflow answers "where does quality come from?" differently. Superpowers bets on **agent discipline** — quality fails because agents rationalize, so bulletproof the rules. Compound Engineering bets on **accumulated knowledge** — quality fails because lessons evaporate, so persist and validate them. Brana bets on **contracts plus human eyes on the running app** — quality fails because green tests can lie about products, so gate on demonstrated behavior.

That last bet is Brana's distinctive contribution: both reference workflows stop at code review. Nothing in either launches the app, walks a user journey, or judges a screen — "every task green, app unusable" can ship through both. Brana's 6b demo gate, kernel journey, and UX.md exist to close exactly that gap.

The honest flip side — Brana's open gaps, in priority order:

1. **No lesson capture** — the root cause of a Phase 6/7 bug dies with the session. A small equivalent of Compound Engineering's solutions store is the highest-value pattern still to adopt.
2. **Single-reviewer 6a** vs. their multi-perspective panels — the diff-selected category list is a partial answer; a second persona (security/adversarial) on risky diffs would close most of the rest.
3. **No rationalization-table armor** on the hard rules (scope cuts, gate skips) — cheap to add, but per Superpowers' own guidance, only worth it where violations actually occur in practice.

Cost profile: Brana is cheapest per feature (fewest agent turns; the human supplies the expensive judgment for free), Superpowers is mid (review round-trips per task), Compound Engineering is highest upfront with claimed compounding payback at scale. For a solo dev shipping apps, Brana's shape fits best; the other two are excellent sources of ingredients — which is exactly how we use them.

## What Brana adopted from them

Credit where due — v1.0 already folds in five tested patterns from these projects:

| Adaptation | Source | Landed in |
|---|---|---|
| Path-based delegation, no re-narration | both | Agent Adaptation Layer, brana-5 delegate |
| Interfaces block (CONSUMES/PRODUCES) | Superpowers | brana-4 task schema |
| Verification evidence + SHA ledger, compaction recovery | Compound Engineering / Superpowers | brana-5 |
| Reviewer independence + subagent report contract | both | brana-5, brana-6 |
| `status:` stamps + refusals; deletion-test rule | Compound Engineering | all phases; WORKFLOW.md intro |
| Brainstorming moves (decomposition, ask-first, approaches, integration check, spec self-review) | both | Phase 1 / brana-1 |
