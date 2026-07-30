---
name: brana-build
description: "Use when the user says implement, build, do the next unit or task, continue the plan, or asks for code review of workflow-built code, or mentions Brana phase 5 or 6. Requires a specs/NNN-name/PLAN.md."
---

# Brana — Execute & Review

Canon: `WORKFLOW.md` — Flow §§3–4, §Units, §Dependencies, §Model & Session
Economics. This skill sequences; rules live there.

## Steps

1. **State**: read `.brana/ledger.md` + git log for done units (after
   compaction, only these — never remembered conversation). On main/master:
   create the cycle branch before any code.
2. **Dispatch** the next unready unit to a subagent — packet is paths, not
   prose: the unit's PLAN.md heading, referenced interfaces, CONVENTIONS.md,
   active-module section paths. Parallel dispatch only for disjoint files
   with no dependency edge. Subagent writes only its unit's files.
3. **Hard stops** (unit or controller): user-visible ambiguity, scope cut,
   out-of-plan dependency → stop and ask; never guess past. Routine deps:
   implementer picks and reports (§Dependencies).
4. **Verify** per unit: the verify command green, acceptance behavior
   exercised, commit, one ledger line (id, status, SHA, date — rides in the
   same commit). Never mark done on green unit-tests alone; never write
   status into PLAN.md.
5. **After U1 lands**: write the kernel e2e once, add to verify. No other
   e2e unless a module demands it or a walkthrough finding requires it.
6. **Review** (Flow §4): risk-module diffs → immediate independent reviewer
   subagent (diff + contracts only, never implementer rationale); everything
   else → one batched branch review before release. Findings need repros
   before becoming fix units; failed repros go to the user. Second
   occurrence of a specific rule → add lint/CONVENTIONS line.
7. **Plan changed mid-cycle?** Patch PLAN.md, re-run self-review on the
   patched section, update stale interfaces of not-done units.
8. **Pull gate**: user says "show me" → launch + print journey script, zero
   ceremony. Long cycle → post a screenshot when a vertical slice lands.

Two failed subagent attempts on a unit → take it over directly in the
controller. All units done + reviews clean → hand off to `brana-ship`.
