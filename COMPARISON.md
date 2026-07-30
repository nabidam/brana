# How Brana Compares

Brana v2.0 (`WORKFLOW.md` + `skills/brana-plan|build|ship`) side by side with two excellent public workflows we studied closely and borrowed from: [**Superpowers**](https://github.com/obra/superpowers) (Jesse Vincent / prime-radiant) and [**Compound Engineering**](https://github.com/EveryInc/compound-engineering) (Every). Updated 2026-07-30 for v2.0.

> **Cost-claim policy:** earlier versions of this document claimed Brana was
> "cheapest to run" and "cheapest per feature". Audited project data showed the
> opposite for v1 (see `docs/2026-07-30-brana-workflow-audit.md`). Per the v2
> measurement rule, this document makes no unmeasured cost claims.

## At a glance

| Dimension | Brana v2 | Superpowers | Compound Engineering |
|---|---|---|---|
| Core bet | One canonical plan + human walkthrough of the running app | Behavioral discipline skills | Compounding knowledge loops |
| Flow | 6 steps (discover→plan→execute→review→release→change) | 5-ish, chained by terminal states | 6 (brainstorm→…→compound) |
| Artifacts | 1 canonical PLAN.md per cycle + conditional living docs | Design doc + plan | 1 mutating unified plan |
| Ceremony scaling | Risk modules (money, external, migration, UI, auth, operator, deployment) | Uniform | Tier-sized |
| Product review | **Final human walkthrough + pull gates** | None | None |
| Scope discipline | **Kernel journey + scope challenge + hard-stop cuts** | YAGNI + decomposition | Tier-sized ceremony |
| Delegation | Path-based subagent packets, persistent controller | Core mechanism (SDD) | Core mechanism (persona panel) |
| Code review | Risk-scoped: immediate on risky diffs, batched otherwise | 2-stage per task | 6–13 personas, diff-selected |
| Learning persistence | ADRs + lint-rule compounding on repeat findings | None | **docs/solutions/ + validation** |
| Size | ~380-line canon + 3 thin router skills | ~15 skills, mostly short | 29 skills, 300–800 lines each |

## Three different bets

Superpowers bets on **agent discipline** — quality fails because agents rationalize, so bulletproof the rules. Compound Engineering bets on **accumulated knowledge** — quality fails because lessons evaporate, so persist and validate them. Brana bets on **one plan plus human eyes on the running app** — quality fails because green tests can lie about products, so gate on demonstrated behavior.

That last bet remains Brana's distinctive contribution: both reference workflows stop at code review. Nothing in either launches the app, walks a user journey, or judges a screen.

## What v2 adopted from them

| Adaptation | Source |
|---|---|
| Single canonical plan, enriched in place, stable IDs | Compound Engineering (unified-plan redesign) |
| Bounded worker packets; workers never read the whole plan | Superpowers (SDD) |
| Interfaces stated once at boundary units | Superpowers |
| Progress outside the plan (ledger) | Compound Engineering |
| Plan self-review checklist replacing gate passes | Superpowers (writing-plans self-review) |
| Repro-before-fix review findings | both |

## Where they remain stronger

1. **Superpowers' anti-rationalization machinery** (Iron Laws, red-flag tables) is deeper than Brana's hard-stop rules.
2. **Compound Engineering's solutions store** genuinely compounds across projects; Brana's ADRs + lint-compounding are a lighter equivalent.
3. Both are more battle-tested across harnesses.
