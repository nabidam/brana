---
status: gate-passed
profile: lite
---

# Dally — SPEC

## Core promise

Log today's mood from the terminal in seconds and see an honest trend over weeks, months, and years.

## Kernel

1. **Add a mood** — `dally mood add <1-5>` with optional `--note TEXT` and `--date YYYY-MM-DD` (backdating). Mood is an integer 1–5 (1 = down, 5 = top). Invalid values rejected with a clear error.
2. **Persistent storage** — entries stored in SQLite at the XDG data dir (`~/.local/share/dally/dally.db` via platformdirs). DB and schema auto-created on first run.
3. **List entries** — `dally mood list` shows recent entries (date, mood, note) as a Rich table, newest first.
4. **Reports** — `dally report week|month|year` shows the average mood for the period plus a per-day (week), per-day (month), or per-month (year) breakdown, rendered as a Rich table. Days with multiple entries count as their average; days with no entries shown as empty, excluded from the average.

### Kernel journey

Run `dally mood add 4 --note "good run"` → confirmation shows saved entry → `dally mood add 2 --date 2026-07-14` backfills a missed day → `dally mood list` shows both entries in a Rich table → close the terminal, open a new one → `dally mood list` still shows both → `dally report week` shows this week's average and a per-day breakdown including both days.

## v1

Exactly the kernel. No additional features.

## Backlog (ranked)

1. Terminal bar chart in reports (Rich bars per day/week/month)
2. Best/worst days + logging streak in reports
3. Mood distribution (count of 1s–5s per period)
4. `dally mood delete <id>`
5. `dally mood edit <id>`
6. Custom date ranges for reports (`--from/--to`)
7. Export (CSV/JSON)
8. Configurable DB path (`DALLY_DB` env var)
9. Daily reminder / shell-prompt nudge

## Acceptance criteria

- `dally mood add 3` exits 0, prints confirmation with date, mood, note (if any).
- `dally mood add 0`, `add 6`, `add abc` exit non-zero with a message naming the valid range; nothing is written.
- `--date` accepts `YYYY-MM-DD`; future dates rejected; malformed dates exit non-zero.
- Multiple `add`s on one date all persist as separate rows; reports use the per-day average.
- `dally mood list` with no entries prints a friendly empty state, exits 0.
- `dally report week` covers the current ISO week (Mon–Sun); `month` the current calendar month; `year` the current calendar year.
- Period average is the mean of daily averages (not of raw entries), rounded to 1 decimal.
- All dates use local system time.
- Fresh machine: first command creates `~/.local/share/dally/dally.db` and schema without error.
- All human-facing output rendered via Rich (tables, colored confirmations); errors go to stderr.

## Assumptions

- Week = ISO week, Monday start. Timezone = local system time, naive dates (no TZ column).
- Single user, single machine; no sync, no auth.
- Entry timestamp stored as date + created-at; reports operate on the date.

## Edge cases

- Same-day duplicate adds → allowed, averaged in reports.
- Report over period with zero entries → friendly "no data" message, exit 0.
- DB file deleted between runs → recreated empty, no crash.
- Note containing quotes/unicode/emoji → stored and displayed intact.

## Non-functional requirements + tech constraints

- Any command completes in < 1s for ≤ 10k entries.
- No network access, ever.
- Works on Linux/macOS; Python ≥ 3.11.

## Suggested tech stack

Python 3.11+, **Typer** (CLI), **Rich** (output), stdlib `sqlite3`, **platformdirs** (XDG path). Packaged with pyproject.toml, installable via `pipx install dally`. Tests: pytest.

## Design direction

Personality: calm, encouraging, minimal. References: `gh` CLI (clean tables, quiet color), `httpie` (friendly confirmations). Terminal density: airy — one table per screen, generous padding. Mood values color-coded on a consistent 1→5 scale (red → dim → neutral → green → bright green), reused identically in list and reports. Accessibility: never color-only — mood always shown as number too; respects `NO_COLOR`.

## Accepted risks

- 2026-07-16 — Phase 2 architecture review skipped (Route S lite, advisory) — small 4-module CLI, no external systems or concurrency.

## Out of scope

- GUI/TUI dashboards, mobile, web
- Multi-user, sync, cloud backup
- Mood tags/categories, journaling beyond one note
- Notifications/reminders (backlog #9 at most)
- Analytics beyond listed reports (correlations, ML, predictions)
