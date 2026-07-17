# Prompts

## Phase 1

```
/brana-1-spec lets build a cli app that tracks users mood. name is Dally, it has some cli commands, for example `dally mood add 3`. moods are stored as 1-5 that 1 is down and 5 is top mood. data is stored in sqlite. dally also has some stats for report as weekly, monthly, and annual. use cli and rich for beautiful cli outputs. if any clarification needed, ask.
```

Agent asked some questions and decided to keep specs lite. (PRD folds into SPEC acceptance criteria; UX/ARCHITECTURE mini; PLAN.md/FILE_STRUCTURE.md cut).

## Phase 2

```
 /brana-2-prd-arch
```

## Phase 3

```
/brana-3-plan
```

Read markdowns.

## Phase 4

```
/brana-4-tasks
```

Agent writes tasks, then calls a cheaper model (Haiku) to run a semantic verification of tasks over spec and documents.

## Phase 5

```
/brana-5-implement - task 0
```

Repeat this step to task 4, after implementing task 4 agent shows a walkthrough about Demo Gate 1. User walks through the app, and kernel journey, observes and reports findings. Nothing found so we pass demo gate 1.
Again rerun skill 5 for tasks 6, 7, 8. User should walk again at task 8, then agent ends task 9.

## Phase 6

Now core spec is done, we can ask another vendors agent to review the code.

```
/brana-6-review
```

## Phase 7

We want to add new feature, so we send:

```
lets add a new feature: add a heatmap arg to app, so it renders a github like heatmap over a year with colored days (based on the saved mood). if you find any ambiguity, ask to clarify.
```

Agent writes a new spec (002-heatmap), and generates its rules.

## PHASE 8

We repeat previous commands to implement this specs tasks.
And done.
