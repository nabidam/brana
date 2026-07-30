# Notes — Cycle 001-core PLAN

## 1. Goal & kernel journey

A local-first notes app: capture a thought in under two seconds and never
lose it.

Kernel journey:

- KJ1 — open the app; the note list (possibly empty) is visible
- KJ2 — create a note "buy milk"; it appears at the top of the list
- KJ3 — close the app entirely and reopen it
- KJ4 — "buy milk" is still listed
- KJ5 — delete the note; it leaves the list and stays gone after reopen

## 2. Scope

In: create, list, delete, persistence across restarts.
Out: editing, search, sync, tags.
Backlog: edit-in-place, full-text search, markdown rendering.

## 3. Requirements

- R1 — a created note persists across app restart (acceptance: run KJ2–KJ4)
- R2 — deletion is durable (acceptance: run KJ5)
- R3 — an empty store shows an empty state, not an error (acceptance: first
  launch on a fresh profile shows "No notes yet")
- R4 (NFR) — cold start under 1s, measured by `scripts/measure-start.sh`

## 4. Active risk modules

None. (No money, no external system, no migration against existing data, UI
is minimal, no operator surface, single-process app. No auth module: notes
are local-only single-user content on the user's own disk, which the
trigger explicitly scopes out — no multi-user access, no sync, nothing
served beyond localhost.)

## 5. Stack & dependencies

Python 3.12 + FastAPI serving a single static page; SQLite via the stdlib.
No strategic dependencies. Routine: `fastapi`, `uvicorn` (resolved at
implementation, reported in unit reports).

## 6. Units

### U1 — walking skeleton (kernel journey end-to-end)

Outcome: KJ1–KJ5 pass against the real app — one page, one table, ugly.
Deps: none. Files (hint): `app/main.py`, `app/store.py`, `static/index.html`.
Acceptance: R1, R2 exercised in the running app.
Produces: `POST /notes`, `GET /notes`, `DELETE /notes/{id}` (JSON:
`{id: int, text: str, created_at: str}`).

### U2 — empty state, ordering, and startup budget

Outcome: fresh profile shows "No notes yet"; list is newest-first; the R4
measurement exists and passes.
Deps: U1. Files (hint): `static/index.html`, `app/store.py`,
`scripts/measure-start.sh`.
Acceptance: R3; KJ2's "appears at the top" assertion; R4 — the script
reports cold start under 1s (re-measured on the release build at the
walkthrough).

## 7. Verification contract

Verify: `scripts/verify.sh` = ruff + pytest + kernel e2e.
Kernel e2e (written once when U1 lands): `tests/test_kernel_journey.py`
drives KJ1–KJ5 against the running app.
Definition of done: verify green + acceptance behavior exercised + ledger
line committed with the U-ID in the commit subject.

## 8. Walkthrough script

1. `scripts/run.sh` — app opens to the note list (KJ1)
2. Walk KJ2–KJ5 in order
3. Edge behaviors: restart mid-session (R1); first launch on a fresh
   profile (R3)
4. Measure R4 via `scripts/measure-start.sh`; record the number
