# Brana vs Superpowers — Token Burn & Quality Analysis

**Date:** 2026-07-30
**Scope:** Documents only — no code read. Compared Brana workflow (WORKFLOW.md v1.12 + brana-1…7 skills) against the two reference workflows (`references/superpowers`, `references/compound-engineering-plugin`) and their real outputs:

- **Superpowers project:** `fai-toolkit` (API management platform — gateway, billing, admin; a genuinely large scope)
- **Brana projects:** `astryxs-rtl-dashboard`, `chillify`, `begirex`, `s2orc`

**Observed:** Brana projects burned far more tokens; code quality was sometimes *better* on the superpowers project. This document explains why, from the document trail alone.

---

## TL;DR

Brana burns tokens **by design, not by accident**. Three root causes:

1. **9 process artifacts vs superpowers' 2**, all re-read across ~30–40 fresh cold sessions.
2. **The plan contains zero code** — every implementer re-derives everything from prose contracts, while superpowers' plan embeds the actual code, written once by the strong model.
3. **12 versions of ratchet growth** — every post-mortem added gates and rules; none ever removed any.

The quality gap follows the same causes: superpowers puts the whole design in one small document that every session reads fully; Brana scatters the truth across 9 documents that implementers only ever see in fragments.

---

## The Numbers

| | Superpowers (fai-toolkit) | Brana (chillify, worst case) |
|---|---|---|
| Process docs | **2 files**: spec 151 lines + plan 1,059 lines | **9 doc types**: root living docs 1,922 lines + cycle docs 2,539 lines ≈ 4,500 lines |
| Plan content | **Actual code**, TDD steps, exact commands | Contracts, criteria, prose — no code |
| Per-task context | Subagent gets its own task section only | Task + CONVENTIONS + ARCHITECTURE §§ + DESIGN + UX screen + files (ARCHITECTURE.md alone: 1,211 lines chillify, 1,018 s2orc) |
| Sessions | 1 lineage + ~21 subagents, prompt cache **hot** | Fresh session per phase + per 2–3-task batch + per review + per gate + confirmation + doc sync — cache **cold** every time |
| Extra passes | 1 plan self-review (inline checklist) | Consistency gate (pastes **all 8 docs**), task gate, architecture review, 6a review per 2–3 tasks, finding-confirmation pass, doc sync per merge, gate preflights, evidence file per task |
| Process instructions loaded | 1 small skill at a time (70–420 lines) | WORKFLOW.md 909 lines + skill 80–194 lines; skills **duplicate** WORKFLOW content |
| Scale delivered | 21 tasks, full platform (gateway, rate limits, wallet, Zarinpal, admin) | chillify 001-core: ~30 tasks incl. 8+ fix/spawn micro-tasks (4a, 4b, 9a, 14a/b, 18a/b, 20-preflight, 20-seed-guard, 20-spotdl-proxy, 20-proxy-wiring) |

Doc volume per project (root + cycle process docs, lines):

| Project | Workflow | Process-doc lines |
|---|---|---|
| fai-toolkit | superpowers | ~1,210 |
| astryxs-rtl-dashboard | brana (litest) | ~1,290 |
| begirex | brana | ~2,550 |
| chillify | brana | ~4,500 |
| s2orc | brana | ~3,800 |

And these lines are not read once — Brana's session model re-reads them cold dozens of times.

---

## Root Causes, Ranked

### 1. Code lives in the wrong phase

Superpowers' `writing-plans` rule: *"Complete code in every step."* The planner — the strong model, with full context, in one session — writes ~80% of the code **once**; implementers near-transcribe it. The fai-toolkit plan (52 KB) contains complete `config.py`, `main.py`, migrations, test bodies, exact shell commands with expected output.

Brana forbids this: PLAN.md and TASKS.md carry prose contracts and acceptance criteria only, so every Sonnet batch session re-invents the code from scratch against 4+ contract documents. The same code is paid for twice — once as prose specification, again as generation. **This alone explains most of the burn gap.**

### 2. Session fragmentation kills the prompt cache

Brana mandates a fresh session per phase, per 2–3-task batch, per review, cleared at every gate. Every cold start re-reads thousand-line living docs at full input price.

Superpowers keeps one parent session (cached) plus throwaway subagents that read only their own task. Brana's Agent Adaptation Layer copied superpowers' mechanism ("pass paths, not prose") but kept the session-flush rule that defeats it.

### 3. Doc count multiplies cross-checking; cross-checking multiplies docs

9 artifacts → contradictions become possible → consistency gate pasting all 8 docs → task gate → stale-plan re-gates → doc sync per merge → `brana-gate claims` checks. Each gate exists to police drift *between documents Brana itself created*. Superpowers has no consistency gate because 2 documents can't drift much. **Ceremony is quadratic in artifact count.**

### 4. Ratchet growth — rules only added, never removed

CHANGELOG + version history: v1.1 closed 15 gaps; v1.2 added wire contracts and verified fakes; v1.3 the task gate; v1.4–1.6 added 8 mechanisms; v1.8 done-mark integrity; v1.9–1.12 added *countermeasures to earlier versions' own weight* (lite profile, token diet, interior-task slimming, retro-lite valve). The workflow now spends whole releases mitigating itself.

WORKFLOW.md's own maintenance rule — "every line must change agent behavior, else delete it" — has never triggered a deletion release. Superpowers stays at 14 orthogonal skills; Brana is one 909-line monolith plus 7 skills that restate it — violating its own "one source of truth per fact" rule for the process itself.

### 5. Overhead tasks are real tasks

Gates, crystallization steps, evidence files, preflights, spawn cycles, finding-confirmation loops — each is a session with full context load. Chillify: gate 20 spawned 4 micro-tasks (preflight, seed-guard, spotdl-proxy, proxy-wiring); the review loop produced 4a/4b/9a/14a/14b/18a/18b. fai-toolkit shipped 21 tasks *total*, including scaffold and the end-to-end smoke.

### 6. Isolation-by-contract hurts quality

Brana implementers must "learn neighboring types from the interfaces block, never by reading neighbor code" — a rule designed for copy-paste token budgets, but kept in agent mode where reading is cheap. Result: seam bugs that the demo gates then catch expensively (WORKFLOW.md itself admits: "bugs live in the seams between well-tested tasks"). The superpowers implementer sees concrete code in the plan plus the real repo. Better coherence, fewer fix loops.

---

## Why Superpowers Quality Is Sometimes Higher

- **Decision density beats volume.** The fai-toolkit spec is 151 lines but denser in decisions than chillify's 4,500: exact key format, exact rate-limit resolution order, exact payment-idempotency mechanism. It is small enough that every session actually reads all of it. Brana's intent spreads across SPEC + PRD + UX + ARCHITECTURE; any one reader holds a fragment.
- **Self-review replaces gate bureaucracy.** Superpowers' plan self-review is one inline checklist (spec coverage, placeholder scan, cross-task type consistency). It catches the same failure class Brana's consistency gate catches, at near-zero cost, with no extra session.
- **Verification is built in, not bolted on.** TDD steps inside the plan make verification part of execution, instead of an after-the-fact evidence-file bureaucracy.

---

## What Brana Got Right (Keep)

Demo gates and "done = demonstrated", the kernel journey, the scope challenge, the dependency plan (buy-first), scope-cut hard stops, reviewer independence. These are genuine improvements over superpowers, which has weak product-level verification.

The problem is not the ideas — it's that each idea was implemented as **a document + a gate + a stamp + a script check + a skill paragraph**.

---

## Direction (for a future revision — nothing changed yet)

Collapse toward superpowers' economy while keeping Brana's product verification:

1. **One spec** — decisions-dense, ≤200 lines (the fai-toolkit spec is the model).
2. **One plan with code in it** — the strong model writes code once, at planning time.
3. **One parent session + path-only subagents** — preserve the prompt cache; stop mandating session flushes.
4. **Demo gates stay** as the only human stop — they are Brana's real contribution.
5. **Delete the consistency gate and the task gate** — a plan self-review checklist replaces both.
6. **Stop restating WORKFLOW.md in the skills** — one source of truth for the process.
7. **Lite is not a valve; lite is the default** — the full profile must earn its existence per project, not the other way around.
