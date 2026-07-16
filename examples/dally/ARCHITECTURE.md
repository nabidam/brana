# Dally — ARCHITECTURE (lite)

Living doc — current truth. Patch on every change; append decisions to the Decision log.

## Stack commitment

- Python 3.11+, packaged via `pyproject.toml` (src layout: `src/dally/`), installable with `pipx install dally`.
- **CLI**: Typer (`dally` entry point; `mood` and `report` sub-apps).
- **Output**: Rich (tables, styled confirmations) to stdout; errors as plain one-liners to stderr; respects `NO_COLOR` (Rich handles natively).
- **Storage**: stdlib `sqlite3`, DB at `platformdirs.user_data_dir("dally")/dally.db`; directory, DB, and schema created on first connection.
- **Test harness**:
  - Unit/integration (storage, report math): **pytest**, against a temp-dir DB (fixture overrides the data dir).
  - e2e/journey: **pytest + Typer's `CliRunner`** — invokes the real CLI in-process against a temp data dir, asserts exit codes and output text. This is the harness the walking skeleton and every gate's crystallization task use.

## Module layout

```
src/dally/
  cli.py       # Typer apps, arg parsing, exit codes — no business logic
  storage.py   # sqlite3 connection, schema init, add/list/query functions
  reports.py   # period resolution (ISO week / month / year), daily + period averages
  render.py    # Rich tables, confirmations, empty states, mood color scale
```

Dependency direction: `cli → (storage, reports, render)`; `reports → storage`; `render` is pure formatting (takes plain data, returns/prints Rich renderables). No module imports `cli`.

## Data model

```sql
CREATE TABLE IF NOT EXISTS entries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT    NOT NULL,             -- ISO YYYY-MM-DD, local time, naive
    mood       INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 5),
    note       TEXT,                          -- nullable, unicode intact
    created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date);
```

- No UNIQUE on `date` — same-day duplicates are allowed by SPEC and averaged in reports.
- `idx_entries_date` serves list ordering and report period range scans (< 1s at 10k entries is comfortably met).

## Contract surface (internal API)

| Function | Shape | Errors |
|----------|-------|--------|
| `storage.add_entry(date: date, mood: int, note: str \| None) -> Entry` | returns saved row (id, date, mood, note, created_at) | raises `ValueError` on mood outside 1–5 (also enforced by CHECK) |
| `storage.list_entries(limit: int = 30) -> list[Entry]` | newest date first, then newest created_at | — |
| `storage.entries_between(start: date, end: date) -> list[Entry]` | inclusive range for reports | — |
| `reports.build_report(period: Literal["week","month","year"], today: date) -> Report` | period bounds, per-bucket averages (day or month), period average = mean of daily averages, 1 decimal | — |
| CLI validation (in `cli.py`) | mood int 1–5; `--date` parsed as `YYYY-MM-DD`, must not be in the future | exit code 2, one-line stderr message naming valid range/format |

`Entry` and `Report` are frozen dataclasses in their owning modules.

Exit codes: 0 success (including empty states), 2 validation error, 1 unexpected failure.

## Kernel-journey traceability

| Journey step (UX.md) | Serving contract |
|----------------------|------------------|
| 1. `mood add 4 --note` → confirmation (S1) | `cli` validation → `storage.add_entry` → `render.confirmation` |
| 2. `mood add 2 --date 2026-07-14` → backdated confirm (S1) | `cli` date validation → `storage.add_entry(date=...)` → `render.confirmation` |
| 3. `mood list` → both entries (S2) | `storage.list_entries` → `render.entries_table` |
| 4. new terminal → `mood list` still shows both | same as step 3 — persistence via SQLite file at XDG path (schema init on connect) |
| 5. `report week` → average + per-day breakdown (S3) | `reports.build_report("week")` → `storage.entries_between` → `render.report_table` |
| Empty/error states (S2/S3/S4) | `render.empty_state`, `cli` error path (stderr, exit 2) |

No external systems → no wire contracts. No auth / no cross-boundary input → no threat model (lite qualification holds).

## Error handling

- Validation errors: caught in `cli.py`, one line to stderr, exit 2, no partial writes (single INSERT per add).
- Missing DB/dir: `storage.connect()` always ensures dir + schema (`CREATE ... IF NOT EXISTS`) — deleted DB is recreated empty, no crash.
- Unexpected exceptions: top-level handler prints one-line error to stderr, exit 1 — never a traceback in normal use.

## Configuration

None in v1. DB path fixed at platformdirs location (configurable `DALLY_DB` is backlog #8). Tests override via the data-dir fixture, not an env var.

## Decision log

<!-- append-only: YYYY-MM-DD — decision — why -->
- 2026-07-16 — stdlib sqlite3 over an ORM — 4-function storage surface; ORM serves no requirement.
- 2026-07-16 — period average computed in Python (reports.py) not SQL — mean-of-daily-averages is clearer and testable as a pure function; 10k rows is trivial in memory.
- 2026-07-16 — Typer CliRunner as the e2e harness — in-process, fast, asserts the real CLI surface (exit codes + output) without subprocess flake.
