---
status: gate-passed
profile: lite
---

# Dally — SPEC 002: Mood heatmap

## What

A new top-level command `dally heatmap` that renders a GitHub-style calendar
heatmap of daily mood to the terminal (Rich). 7 rows (days of week) ×
~53 week columns; each cell colored by that day's mood using the existing 1–5
mood color scale.

- `dally heatmap` — trailing 52 weeks ending today (default).
- `dally heatmap --year YYYY` — that calendar year, Jan 1 → Dec 31.

## Why

Reports (S3) give period averages and tables; the heatmap gives an at-a-glance
year of logging density and mood pattern — the single view that answers "how
has the year felt?" and surfaces gaps in logging. Backlog-adjacent to the
report family but a distinct surface.

## Acceptance criteria (falsifiable)

1. `dally heatmap` prints a grid of 7 day-of-week rows and ~53 week columns,
   most recent week rightmost, covering the trailing 52 weeks ending today.
2. Each day cell is colored on the same 1–5 scale as S1/S2/S3
   (1 red → 2 dim → 3 neutral → 4 green → 5 bright green). A day with **no**
   entry renders as an empty/blank cell distinct from all mood colors.
3. A day with **multiple** entries colors by its **daily average rounded to the
   nearest integer 1–5** (same bucketing as reports; ties round half up, so
   avg 2.5 → 3).
4. `dally heatmap --year 2025` renders Jan 1 – Dec 31 2025 with month labels;
   a future year or malformed `--year` → S4 error (one line, stderr, exit 2).
5. Zero entries in the window → friendly empty state (exit 0), not a blank crash.
6. A legend maps the 5 colors + empty to their meaning; mood is never conveyed
   by color alone (legend names the numbers). Respects `NO_COLOR`.
7. Reads only via `storage.entries_between`; no schema, no writes, exit 0 on
   success.

## Out of scope

- No new storage columns or migrations.
- No streak/stat overlays (backlog #2), no export, no interactivity/scrolling.
- No configurable color themes — reuse the existing scale verbatim.
- Non-year custom ranges (`--from/--to`) stay backlog #6.
