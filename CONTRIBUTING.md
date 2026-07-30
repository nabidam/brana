# Contributing to Brana

Issues and PRs welcome. Ground rules:

## The deletion test

Every line in WORKFLOW.md and the skills must change agent behavior — **if deleting it would not change the output, delete it.** Adjectives earn their place only when operationalized by a concrete rule. PRs that add prose without behavioral effect will be asked to trim.

## The addition test

Every new rule must state the failure it prevents, what activates it, and what would justify removing it (WORKFLOW.md maintenance rules). Cost claims require measured cycle data.

## Scope

Brana is a workflow, not a toolkit. Changes should serve the core bet — one canonical plan plus human eyes on the running app. Heavy harness-specific machinery is out of scope; the only sanctioned scripts are `tools/brana-gate` and `tools/check-dist.sh`.

## Required checks before any PR

```bash
bash tools/check-dist.sh                       # bundle byte-identical to source, no extra copies
python3 -m py_compile tools/brana-gate skills/brana-plan/scripts/brana_gate.py
python3 tools/brana-gate docs WORKFLOW.md skills/*/SKILL.md examples/notes-v2/specs/001-core/PLAN.md
```

All three must exit 0. If you edited `WORKFLOW.md` or `tools/brana-gate`, re-copy the bundle (`cp WORKFLOW.md skills/brana-plan/reference/WORKFLOW.md`; `cp tools/brana-gate skills/brana-plan/scripts/brana_gate.py`) before running check-dist. CI runs the same commands plus a negative contrast fixture (`tools/testdata/DESIGN-bad.md` must fail the gate).

## PRs

- One problem per PR. Describe the problem you hit, not just the change.
- If you changed skill wording, say which agent/harness you tested it on and what behavior changed.
- The skills are routers: a rule lives in WORKFLOW.md only — never restate it in a skill.

## Issues

Real experiences beat theory. "brana-build did X when I expected Y, transcript attached" is the most useful issue shape.
