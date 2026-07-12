# Contributing to Brana

Issues and PRs welcome. Ground rules:

## The deletion test

Every line in WORKFLOW.md and the skills must change agent behavior — **if deleting it would not change the output, delete it.** Adjectives earn their place only when operationalized by a concrete rule. PRs that add prose without behavioral effect will be asked to trim.

## Scope

Brana is a workflow, not a toolkit. Changes should serve the core bet — contract docs plus human eyes on the running app. Harness-specific machinery (hooks, scripts, dependencies) is out of scope: the copy-paste canon must keep working with zero tooling.

## PRs

- One problem per PR. Describe the problem you hit, not just the change.
- If you changed skill wording, say which agent/harness you tested it on and what behavior changed.
- Keep WORKFLOW.md (canon) and `skills/` in sync — a rule that changes in one must change in both.

## Issues

Real experiences beat theory. "Phase 5 did X when I expected Y, transcript attached" is the most useful issue shape.
