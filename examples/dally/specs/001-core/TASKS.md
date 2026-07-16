---
status: ready
---

# Dally — TASKS (cycle 001-core, Route S)

Derived from SPEC.md (kernel + acceptance criteria + edge cases), ARCHITECTURE.md (contract
surface, module layout, test harness), UX.md (screens S1–S5, kernel flow). No PLAN.md — Route S
lite: gates authored here with full anatomy.

Task completions are done-marked against `specs/001-core/evidence/task-N.txt` (see Verification
Machinery in WORKFLOW.md).

Context packs are predictions made before code exists — hints, not contracts; the implementation
session verifies against real files. Interfaces blocks are firmer: they quote the contract, and
contract changes route through ARCHITECTURE.md, never through a task improvising.

Walking skeleton: tasks 0–3 (scaffold → storage → render → CLI add/list), proven at gate 1.
Feature tasks (reports) start only after task 5 (gate 1 crystallization) is done.

---

## Task 0 — Scaffold: package, entry point, test harness

```toml
id = 0
type = "scaffold"
deps = []
skeleton = true
files = [
  "pyproject.toml",
  "src/dally/__init__.py",
  "src/dally/cli.py",
  "src/dally/storage.py",
  "src/dally/reports.py",
  "src/dally/render.py",
  "tests/conftest.py",
  "tests/test_smoke.py",
]
produces = [
  "console script `dally` — Typer app with `mood` and `report` sub-apps",
]

[[criteria]]
text = "`dally --help` exits 0 and lists the `mood` and `report` sub-apps"
layer = "e2e"
gate = 1

[[criteria]]
text = "CliRunner invokes `dally --help` exactly as documented; asserts exit code 0 and that usage names `mood` and `report`"
layer = "contract"

[[criteria]]
text = "the `tmp_path` data-dir fixture in tests/conftest.py points platformdirs at a temp dir; a test asserts no file is created under the real user data dir"
layer = "integration"
```

**Objective:** src-layout package per ARCHITECTURE.md file tree; Typer app skeleton (sub-apps
registered, no command bodies beyond `--help`); ruff + mypy(strict on `src/`) config; pytest +
CliRunner harness with the data-dir override fixture. No feature logic.

- **Inputs:** ARCHITECTURE.md (Stack commitment, Module layout, Test harness), CONVENTIONS.md.
- **Outputs:** installable package; documented run command (`pip install -e .` → `dally --help`),
  recorded in CONVENTIONS.md.
- **Difficulty:** easy.
- **Interfaces — CONSUMES:** none. **PRODUCES:** see toml.
- **Context pack (hints):** ARCHITECTURE.md §Stack commitment, §Module layout, §Test harness;
  CONVENTIONS.md §Folder rules, §Lint-over-prose. No UI rendering yet — no UX.md screens.
- **Done:** `70116c3` — evidence `specs/001-core/evidence/task-0.txt`. Verify green
  (ruff · format · mypy strict src · pip-audit dally-closure · detect-secrets · pytest 2 passed);
  `dally --help` boots via the console script and lists the `mood` and `report` sub-apps.

## Task 1 — storage.py: schema init + entry CRUD

```toml
id = 1
type = "feature"
deps = [0]
skeleton = true
files = ["src/dally/storage.py", "tests/test_storage.py"]
produces = [
  "Entry(id: int, date: date, mood: int, note: str | None, created_at: str) — frozen dataclass",
  "storage.add_entry(date: date, mood: int, note: str | None) -> Entry",
  "storage.list_entries(limit: int = 30) -> list[Entry]",
  "storage.entries_between(start: date, end: date) -> list[Entry]",
]

[[criteria]]
text = "add_entry then list_entries against a real temp-dir SQLite DB returns the saved row with date, mood, note intact (unicode/emoji note round-trips)"
layer = "integration"

[[criteria]]
text = "first connect on a fresh temp dir creates directory, DB file, and schema without error; deleting the DB file between calls recreates it empty, no crash"
layer = "integration"

[[criteria]]
text = "list_entries orders newest date first, then newest created_at; entries_between is inclusive of both bounds; same-day duplicate adds persist as separate rows"
layer = "integration"

[[criteria]]
text = "add_entry with mood 0 or 6 raises ValueError and writes nothing"
layer = "integration"

[[criteria]]
text = "a test calls each produced signature exactly as quoted and asserts the Entry shape (id, date, mood, note, created_at)"
layer = "contract"
```

**Objective:** `storage.connect()` ensuring dir + schema (`CREATE ... IF NOT EXISTS`, DDL from
ARCHITECTURE.md §Data model verbatim); the three query functions; `Entry` frozen dataclass.
Raises, never prints or exits.

- **Inputs:** ARCHITECTURE.md §Data model, §Contract surface, §Error handling.
- **Outputs:** working persistence layer at platformdirs path (fixture-overridable).
- **Difficulty:** easy.
- **Interfaces — CONSUMES:** none. **PRODUCES:** see toml.
- **Context pack (hints):** src/dally/storage.py, tests/conftest.py (fixture from task 0);
  ARCHITECTURE.md §Data model, §Contract surface, §Error handling; CONVENTIONS.md §Test strategy
  (no SQLite mocks — real temp DB). Backend-only: no UX.md/DESIGN.md.
- **Done:** `f350419` — evidence `specs/001-core/evidence/task-1.txt`. Verify green (10 passed);
  real temp-dir SQLite exercises round-trip unicode, recreate-after-delete, ordering, inclusive
  range, same-day duplicates, mood-range ValueError (writes nothing), Entry frozen shape.

## Task 2 — render.py: mood scale, confirmation, entries table, empty state

```toml
id = 2
type = "feature"
deps = [1]
skeleton = true
files = ["src/dally/render.py", "tests/test_render.py"]
consumes = [
  "Entry(id: int, date: date, mood: int, note: str | None, created_at: str) — frozen dataclass",
]
produces = [
  "render.mood_style(mood: int) -> str — 1→5 scale: red → dim → neutral → green → bright green",
  "render.confirmation(entry: Entry) -> None",
  "render.entries_table(entries: list[Entry]) -> None",
  "render.empty_state(message: str) -> None",
]

[[criteria]]
text = "confirmation output contains the entry's date, the mood as a number, and the note when present"
layer = "unit"

[[criteria]]
text = "entries_table renders one row per entry, newest first as given, mood shown as its number, note column intact (unicode/emoji preserved)"
layer = "unit"

[[criteria]]
text = "mood_style is the single palette: values 1–5 map to red/dim/neutral/green/bright green; no other module defines mood colors"
layer = "unit"

[[criteria]]
text = "a test calls each produced signature exactly as quoted with sample Entry data and asserts printed output shape (capsys: date + mood number present)"
layer = "contract"
```

**Objective:** pure formatting per ARCHITECTURE.md — takes plain data/Entry, prints Rich
renderables to stdout. Single mood palette. No manual ANSI (Rich handles `NO_COLOR`). Never
color-only: mood always printed as its number.

- **Inputs:** UX.md screens S1, S2; SPEC.md §Design direction; CONVENTIONS.md §Output style.
- **Outputs:** all S1/S2 rendering.
- **Difficulty:** easy.
- **Interfaces:** see toml (CONSUMES quotes task 1 PRODUCES).
- **Context pack (hints):** src/dally/render.py, src/dally/storage.py (Entry import only);
  ARCHITECTURE.md §Module layout (render is pure formatting, imports no cli); UX.md **S1, S2**,
  §Density & color notes; CONVENTIONS.md §Output style. No DESIGN.md in lite profile — UX.md
  color/density notes are the design contract.
- **Done:** `78cd9e7` — evidence `specs/001-core/evidence/task-2.txt`. Verify green (16 passed);
  single mood palette, S1 confirmation + S2 airy gh-style table + empty state; never color-only,
  emoji/unicode intact, NO_COLOR-safe. Live tty render sanity-checked (no per-task screenshot —
  visual quality is the demo-gate 1 call).

## Task 3 — cli.py: `mood add` + `mood list` with validation

```toml
id = 3
type = "feature"
deps = [1, 2]
skeleton = true
files = ["src/dally/cli.py", "tests/test_cli.py"]
consumes = [
  "storage.add_entry(date: date, mood: int, note: str | None) -> Entry",
  "storage.list_entries(limit: int = 30) -> list[Entry]",
  "render.confirmation(entry: Entry) -> None",
  "render.entries_table(entries: list[Entry]) -> None",
  "render.empty_state(message: str) -> None",
]
produces = [
  "CLI: `dally mood add <1-5> [--note TEXT] [--date YYYY-MM-DD]` — exit 0 + S1 confirmation; exit 2 + one-line stderr on invalid mood/date",
  "CLI: `dally mood list` — S2 table newest first; friendly empty state, exit 0",
]

[[criteria]]
text = "`dally mood add 4 --note \"good run\"` prints confirmation: today's date, mood 4 (green), the note"
layer = "e2e"
gate = 1

[[criteria]]
text = "`dally mood add 2 --date 2026-07-14` confirms with the backdated date and mood 2 (dim)"
layer = "e2e"
gate = 1

[[criteria]]
text = "`dally mood add 0`, `add 6`, `add abc` each exit 2 with one stderr line naming the valid range 1-5; `dally mood list` confirms nothing extra was written"
layer = "e2e"
gate = 1

[[criteria]]
text = "`dally mood list` shows both entries newest date first, mood color-coded with the number always visible, note intact"
layer = "e2e"
gate = 1

[[criteria]]
text = "`dally mood list` prints the friendly empty state suggesting `dally mood add 4`, exit 0"
layer = "e2e"
gate = 1

[[criteria]]
text = "malformed `--date` (not YYYY-MM-DD) and future dates exit 2 with a one-line stderr message naming the expected format/constraint; nothing written"
layer = "unit"

[[criteria]]
text = "a test drives both produced commands exactly as quoted via CliRunner and asserts exit codes 0/2 and stdout/stderr shape"
layer = "contract"
```

**Objective:** Typer `mood` sub-app commands. All validation in cli.py (mood int 1–5, date
`YYYY-MM-DD` not in the future) → exit 2, plain one-line stderr. Top-level unexpected-exception
handler → exit 1, one line, no traceback. No business logic in cli.py.

- **Inputs:** SPEC.md §Acceptance criteria; UX.md S1, S2, S4, S5 + empty/error states;
  ARCHITECTURE.md §Contract surface (CLI validation row), §Error handling.
- **Outputs:** working `dally mood add` / `dally mood list` end to end.
- **Difficulty:** medium.
- **Interfaces:** see toml.
- **Context pack (hints):** src/dally/cli.py, src/dally/storage.py + src/dally/render.py
  (signatures per interfaces block — do not read bodies); ARCHITECTURE.md §Contract surface,
  §Error handling; UX.md **S1, S2, S4, S5**; CONVENTIONS.md §Error handling.
- **Done:** `7bb36a5` — evidence `specs/001-core/evidence/task-3.txt`. Verify green (27 passed);
  driven through the **real `dally` console script** (fresh XDG_DATA_HOME): add/backdate/list,
  invalid mood 0/6/abc + bad/future date → exit 2 one-line stderr (nothing written), empty state
  exit 0. Extra file touched: `pyproject.toml` script → `cli:main` (top-level exit-1 handler).

## Task 4 — DEMO GATE 1: walking skeleton (add / list / persist)

```toml
id = 4
type = "gate"
deps = [0, 1, 2, 3]

[gate]
n = 1
release = false
launch = "pip install -e . && export XDG_DATA_HOME=$(mktemp -d) && dally --help"
unglamorous = "delete dally.db inside $XDG_DATA_HOME/dally, run `dally mood list` — DB recreated empty, friendly empty state, no crash"

[[gate.journey]]
step = "`dally --help` exits 0 and lists the `mood` and `report` sub-apps"
task = 0

[[gate.journey]]
step = "`dally mood add 4 --note \"good run\"` prints confirmation: today's date, mood 4 (green), the note"
task = 3

[[gate.journey]]
step = "`dally mood add 2 --date 2026-07-14` confirms with the backdated date and mood 2 (dim)"
task = 3

[[gate.journey]]
step = "`dally mood add 0`, `add 6`, `add abc` each exit 2 with one stderr line naming the valid range 1-5; `dally mood list` confirms nothing extra was written"
task = 3

[[gate.journey]]
step = "`dally mood list` shows both entries newest date first, mood color-coded with the number always visible, note intact"
task = 3

[[gate.journey]]
step = "open a new shell, re-export the SAME XDG_DATA_HOME, `dally mood list` still shows both entries (persistence)"
task = 1

[[gate.journey]]
step = "point XDG_DATA_HOME at a second fresh temp dir, `dally mood list` prints the friendly empty state suggesting `dally mood add 4`, exit 0"
task = 3
```

**Preflight (fail-closed):** journey MUST run with `XDG_DATA_HOME` exported to a fresh temp dir —
verify `echo $XDG_DATA_HOME` is a `/tmp/...` path before step 1; **abort if unset or under
`$HOME`** (would touch the real `~/.local/share/dally`). Same-composition rule: this is the
production entry point (`dally` console script) with a disposable data dir — no gate-only harness.
No seed command — the journey creates its own entries.

**Completion artifact:** human walkthrough result (observations per step; screenshots optional).
A skipped walkthrough marks this task `GATE SKIPPED` (never deleted) and task 5's test
`UNWITNESSED`; the journey must be walked at latest at the v1 exit bar.

- **Difficulty:** human time only.
- **GATE 1 WALKED — PASS** (2026-07-17, human) — evidence `specs/001-core/evidence/task-4.txt`.
  Preflight green (verify 27 passed, real console script boots, XDG isolated to /tmp); all 7
  journey steps + unglamorous DB-delete confirmed by the user. No screenshots (declined). No
  findings → no fix tasks. Task 5 crystallization runs next (test is WITNESSED, not UNWITNESSED).

## Task 5 — Crystallize gate 1 as journey e2e

```toml
id = 5
type = "crystallization"
gate = 1
deps = [4]
files = ["tests/test_journey.py"]

[[criteria]]
text = "an automated e2e on pytest + Typer CliRunner (harness per CONVENTIONS.md Test strategy) replays every gate-1 journey step including the unglamorous DB-delete step, asserting exit codes and stable substrings; joins the journey suite and is green"
layer = "e2e"
gate = 1
```

**Objective:** encode gate 1's scripted journey (all steps + unglamorous step) as
`tests/test_journey.py::test_gate1_walking_skeleton`. No feature task (6, 7) starts before this is
done. If gate 1 was `GATE SKIPPED`, this task still runs now; the test is marked `UNWITNESSED`
until the journey is walked.

- **Difficulty:** easy.
- **Interfaces — CONSUMES:** the CLI surface quoted in task 3 PRODUCES. **PRODUCES:** none.
- **Context pack (hints):** tests/test_journey.py, tests/conftest.py, gate 1 journey above;
  CONVENTIONS.md §Test strategy (assert exit codes + stable substrings, not Rich framebuffers).
- **Done:** `4184901` — evidence `specs/001-core/evidence/task-5.txt`. Verify green (28 passed);
  `test_gate1_walking_skeleton` replays all 7 steps + unglamorous DB-delete via CliRunner.
  WITNESSED (gate 1 walked). Feature work (tasks 6–7) unlocked.

## Task 6 — reports.py: period resolution + averages

```toml
id = 6
type = "feature"
deps = [5]
files = ["src/dally/reports.py", "tests/test_reports.py"]
consumes = [
  "storage.entries_between(start: date, end: date) -> list[Entry]",
]
produces = [
  "Report(period: str, start: date, end: date, average: float | None, buckets: list[Bucket]) — frozen dataclass; Bucket = (label: str, average: float | None)",
  "reports.build_report(period: Literal[\"week\",\"month\",\"year\"], today: date) -> Report",
]

[[criteria]]
text = "for fixed `today` dates: week = current ISO week Mon-Sun, month = calendar month, year = calendar year (day buckets for week/month, month buckets for year)"
layer = "unit"

[[criteria]]
text = "a day with multiple entries counts as its average; period average = mean of daily averages (not raw entries), rounded to 1 decimal; month buckets in the year report = mean of that month's daily averages"
layer = "unit"

[[criteria]]
text = "days/months with no entries yield average None and are excluded from the period average; a period with zero entries yields Report.average None"
layer = "unit"

[[criteria]]
text = "against a real temp DB seeded via storage.add_entry, build_report aggregates the stored rows correctly"
layer = "integration"

[[criteria]]
text = "a test calls build_report exactly as quoted for all three period literals and asserts the Report/Bucket shape"
layer = "contract"
```

**Objective:** pure period math per ARCHITECTURE.md — takes `today: date` explicitly (tests pass
fixed dates, never patch the clock). Raises, never prints.

- **Inputs:** SPEC.md §Acceptance criteria (period/average rules), §Assumptions (ISO week, local
  naive dates); ARCHITECTURE.md §Contract surface.
- **Difficulty:** medium.
- **Interfaces:** see toml.
- **Context pack (hints):** src/dally/reports.py, src/dally/storage.py (signature per interfaces
  block); ARCHITECTURE.md §Contract surface, §Decision log (averages in Python, not SQL);
  CONVENTIONS.md §Test strategy. Backend-only: no UX.md/DESIGN.md.
- **Done:** `860cf68` — evidence `specs/001-core/evidence/task-6.txt`. Verify green (40 passed);
  `Report`/`Bucket` frozen dataclasses + `build_report`. ISO-week/calendar-month/calendar-year
  bounds; day buckets (week/month), month buckets (year). Period average = mean of daily averages
  (live drive: seed 5,2 on one day + 2 on next → 2.8, not raw 3.0), rounded 1 decimal; empty
  days/months → None, excluded; zero-entry period → None. Integration test aggregates real temp-DB
  rows. Bucket labels are stable ISO strings (`YYYY-MM-DD` / `YYYY-MM`) — render formats in task 7.

## Task 7 — `dally report` command + report table

```toml
id = 7
type = "feature"
deps = [5, 6]
files = ["src/dally/cli.py", "src/dally/render.py", "tests/test_cli.py", "tests/test_render.py"]
consumes = [
  "reports.build_report(period: Literal[\"week\",\"month\",\"year\"], today: date) -> Report",
  "render.mood_style(mood: int) -> str — 1→5 scale: red → dim → neutral → green → bright green",
]
produces = [
  "CLI: `dally report week|month|year` — S3 header (period + average, 1 decimal) + breakdown table; friendly no-data message, exit 0",
  "render.report_table(report: Report) -> None",
]

[[criteria]]
text = "`dally report week` shows this week's average and a per-day breakdown including both logged days; unlogged days are empty cells excluded from the average"
layer = "e2e"
gate = 2

[[criteria]]
text = "`dally report month` prints a friendly no-data message and exits 0"
layer = "e2e"
gate = 2

[[criteria]]
text = "`dally report year` renders one row per month; months without entries are empty cells"
layer = "integration"

[[criteria]]
text = "report_table uses the same mood_style palette; averages always shown as numbers"
layer = "unit"

[[criteria]]
text = "a test drives `dally report week|month|year` exactly as quoted via CliRunner and calls render.report_table with a sample Report, asserting exit codes and output shape"
layer = "contract"
```

**Objective:** Typer `report` sub-app wired to `reports.build_report` + new `render.report_table`.
Unknown period → Typer usage error (S5). No-data → friendly message, exit 0 (S3 empty state).

- **Inputs:** UX.md S3 + empty state; SPEC.md report acceptance criteria.
- **Difficulty:** medium.
- **Interfaces:** see toml.
- **Context pack (hints):** src/dally/cli.py, src/dally/render.py, src/dally/reports.py
  (signature per interfaces block); ARCHITECTURE.md §Contract surface; UX.md **S3, S5**,
  §Density & color notes; CONVENTIONS.md §Output style.
- **Done:** `050963e` — evidence `specs/001-core/evidence/task-7.txt`. Verify green (48 passed);
  driven through the **real `dally` console script** (fresh XDG_DATA_HOME): `report week` header
  (period + range + average 3.0) + per-day breakdown, unlogged days blank (not zeroed); `report
  month` no-data → friendly message exit 0; `report year` 12 month rows; unknown period `decade` →
  Typer usage error exit 2 (S5). `render.report_table` shares the single mood_style palette (nearest
  1–5), averages always shown as numbers. `dally report` = three thin commands (week/month/year)
  over a shared `_show_report` helper; cli owns the clock (`today=date.today()`), reports stays pure.

## Task 8 — RELEASE GATE: kernel journey, release build

```toml
id = 8
type = "gate"
deps = [0, 1, 2, 3, 5, 6, 7]

[gate]
n = 2
release = true
launch = "python -m build --wheel && python -m venv $(mktemp -d)/venv && $VENV/bin/pip install dist/dally-*.whl && export PATH=$VENV/bin:$PATH && export XDG_DATA_HOME=$(mktemp -d) && dally --help"
unglamorous = "`dally mood add 3 --date 2026-13-45` and `--date` in the future each exit 2 with one stderr line naming the expected format/constraint; nothing written"

[[gate.journey]]
step = "`dally mood add 4 --note \"good run\"` prints confirmation with today's date, mood 4, note"
task = 3

[[gate.journey]]
step = "`dally mood add 2 --date 2026-07-14` backfills the missed day, confirmation shows the backdated date"
task = 3

[[gate.journey]]
step = "`dally mood list` shows both entries in a Rich table, newest first"
task = 3

[[gate.journey]]
step = "close the terminal, open a new one, re-export the SAME XDG_DATA_HOME and PATH — `dally mood list` still shows both entries"
task = 1

[[gate.journey]]
step = "`dally report week` shows this week's average and a per-day breakdown including both logged days; unlogged days are empty cells excluded from the average"
task = 7

[[gate.journey]]
step = "`dally report year` renders per-month breakdown; a note with unicode/emoji added earlier displays intact in `dally mood list`"
task = 7

[[gate.journey]]
step = "point XDG_DATA_HOME at a second fresh temp dir — `dally report month` prints a friendly no-data message and exits 0"
task = 7
```

**Preflight (fail-closed):** wheel install into a fresh venv (release build — not editable), then
the SPEC kernel journey verbatim through the installed `dally` entry point. `XDG_DATA_HOME` must
be a fresh temp dir — **abort if unset or under `$HOME`**. Same-composition rule: installed
console script = the production composition; no wire contracts in ARCHITECTURE.md → no separate
production-composition proof task required. No seed command — journey creates its own entries.
Unglamorous rotation: gate 1 took restart/DB-delete; this gate takes invalid input.

**Completion artifact:** human walkthrough result. Skip → `GATE SKIPPED` + task 9's test
`UNWITNESSED`; must be walked by the v1 exit bar.

- **Difficulty:** human time only.

## Task 9 — Crystallize release gate as kernel-journey e2e

```toml
id = 9
type = "crystallization"
gate = 2
deps = [8]
files = ["tests/test_journey.py"]

[[criteria]]
text = "an automated e2e on pytest + Typer CliRunner replays every gate-2 journey step including the invalid-date unglamorous step, asserting exit codes and stable substrings; joins the journey suite and is green"
layer = "e2e"
gate = 2
```

**Objective:** encode the kernel journey (gate 2, all steps + unglamorous) as
`tests/test_journey.py::test_gate2_kernel_journey`. The release-build aspect (wheel + fresh venv)
stays a walkthrough concern; the e2e crystallizes the journey's behavior through the real CLI
surface in-process.

- **Difficulty:** easy.
- **Interfaces — CONSUMES:** CLI surfaces quoted in tasks 3 and 7 PRODUCES. **PRODUCES:** none.
- **Context pack (hints):** tests/test_journey.py, gate 2 journey above; CONVENTIONS.md §Test
  strategy.
