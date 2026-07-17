---
status: ready
---

# Dally — TASKS (cycle 002-heatmap, Route B / lite delta)

Derived from `specs/002-heatmap/SPEC.md` (acceptance criteria + out-of-scope) and root
ARCHITECTURE.md (contract surface, module layout, test harness) + UX.md (adds screen S6). No
PLAN.md — lite delta: gates authored here with full anatomy. Impact analysis stamped the mini-spec
`gate-passed` (fits architecture; additive only, no schema/API/boundary change).

Task completions are done-marked against `specs/002-heatmap/evidence/task-N.txt` (see Verification
Machinery in WORKFLOW.md). Verify = `tools/verify.sh` (ruff · format · mypy strict · pip-audit ·
detect-secrets · pytest), fail-closed.

Context packs are predictions made before code exists — hints, not contracts; the implementation
session verifies against real files. Interfaces blocks are firmer: they quote the contract, and
contract changes route through ARCHITECTURE.md, never through a task improvising.

No walking skeleton — dally is a live v1 app; the heatmap surface is proven at the demo gate
(task 3) through the real `dally` console script, then re-proven through the built wheel at the
release gate (task 5).

---

## Task 0 — reports.py: `build_heatmap` window + grid math

```toml
id = 0
type = "feature"
deps = []
files = ["src/dally/reports.py", "tests/test_heatmap.py"]
consumes = [
  "storage.entries_between(start: date, end: date) -> list[Entry]",
  "storage.Entry(id: int, date: date, mood: int, note: str | None, created_at: str) — frozen dataclass",
]
produces = [
  "HeatCell(day: date | None, average: float | None) — frozen dataclass; day None = padding cell outside the window, average None = a windowed day with no entry",
  "Heatmap(start: date, end: date, label: str, weeks: list[list[HeatCell]], total_logged: int) — frozen dataclass; each inner list has length 7, index 0 = Sunday .. 6 = Saturday",
  "reports.build_heatmap(today: date, year: int | None = None) -> Heatmap",
  "reports.daily_averages(entries: list[Entry]) -> dict[date, float] — shared helper (extracted, also used by build_report)",
]

[[criteria]]
text = "default (year=None) window is the trailing 52 weeks ending `today`: 53 week columns, first column starts on the Sunday on/before (today - 52 weeks), the last column contains `today`; every inner week list has length 7 indexed Sunday..Saturday"
layer = "unit"

[[criteria]]
text = "year=YYYY window is that calendar year: first column = week containing Jan 1, last column = week containing Dec 31; days before Jan 1 / after Dec 31 render as padding HeatCell(day=None, average=None); label == str(YYYY), default label == \"past 52 weeks\""
layer = "unit"

[[criteria]]
text = "a windowed day with one entry gets that mood as average; a day with multiple entries gets its daily mean; a windowed day with no entry gets HeatCell(average=None); total_logged counts distinct windowed days with >=1 entry"
layer = "unit"

[[criteria]]
text = "against a real temp DB seeded via storage.add_entry, build_heatmap places each entry in the correct (week-column, day-of-week-row) cell for a fixed `today`"
layer = "integration"

[[criteria]]
text = "a test calls build_heatmap(today) and build_heatmap(today, year=2025) exactly as quoted and asserts the Heatmap/HeatCell shapes (weeks is list[list[HeatCell]] of width 7, fields present, total_logged is int)"
layer = "contract"
```

**Objective:** add pure window/grid resolution to `reports.py`. Extract the daily-average
aggregation already inside `build_report` into `daily_averages(entries)` and reuse it in both.
`build_heatmap` never touches the clock (takes `today`), never prints, never validates `year`
(the CLI owns validation) — it reads rows via `storage.entries_between` and lays them onto the
7×N grid. Rounding for the cell color is the render layer's job — `average` stays the exact mean.

- **Inputs:** ARCHITECTURE.md §Contract surface, §Data model, §Decision log (averages live in
  reports.py, not SQL); SPEC.md ACs 1–3.
- **Outputs:** `build_heatmap`, `Heatmap`/`HeatCell`, `daily_averages`; unit + integration tests.
- **Difficulty:** medium (calendar/week-alignment math is the trap — test with fixed dates).
- **Interfaces — CONSUMES / PRODUCES:** see toml.
- **Context pack (hints):** `src/dally/reports.py`, `src/dally/storage.py` (Entry, entries_between),
  `tests/conftest.py` (temp-DB fixture), `tests/test_reports.py` (fixed-`today` test style).
  ARCHITECTURE.md §Contract surface, §Data model. Backend-only — no UX screens, no DESIGN.md.
- **Done:** `f0729ad` — evidence `specs/002-heatmap/evidence/task-0.txt`. Verify green (57 passed;
  9 new heatmap tests). `build_heatmap` default = 53-column trailing-52-week grid, `--year` =
  calendar-year grid with padding; `daily_averages` extracted and reused by `build_report`.

## Task 1 — render.py: `heatmap_grid` + legend (S6)

```toml
id = 1
type = "feature"
deps = [0]
files = ["src/dally/render.py", "tests/test_render.py"]
consumes = [
  "Heatmap(start: date, end: date, label: str, weeks: list[list[HeatCell]], total_logged: int)",
  "HeatCell(day: date | None, average: float | None)",
  "render.mood_style(mood: int) -> str — existing shared palette",
  "render._nearest_mood(average: float) -> int — existing 1-5 clamp",
]
produces = [
  "render.heatmap_grid(heatmap: Heatmap) -> None — prints 7 day-of-week rows x week columns to stdout, month labels above, a legend below",
]

[[criteria]]
text = "prints exactly 7 day-of-week rows; each column is a week; a cell for a windowed day with an entry is glyph-colored via mood_style(_nearest_mood(average)) on the same 1-5 scale as S1/S2/S3; a windowed no-entry day and a padding cell (day=None) render blank/distinct from every mood color"
layer = "unit"

[[criteria]]
text = "a legend row maps each of the 5 mood colors plus the empty cell to its meaning, naming the numbers 1-5 (mood never conveyed by color alone); month abbreviations label the columns; respects NO_COLOR (asserted by rendering with NO_COLOR set and checking no ANSI escapes)"
layer = "unit"

[[criteria]]
text = "a test constructs a Heatmap with known cells and asserts heatmap_grid runs and emits the expected day-count / legend substrings (assert stable substrings, not Rich framebuffers)"
layer = "contract"
```

**Objective:** render the grid as a Rich renderable to stdout. Pure formatting — no clock, no I/O
beyond printing, imports no `cli`. Reuse the single mood palette already defined here; do not
define new mood colors. Blank cell for `average is None` and for padding (`day is None`).

- **Inputs:** SPEC.md ACs 1–2, 6; UX.md S6 (density/color notes); ARCHITECTURE.md §Module layout.
- **Outputs:** `heatmap_grid`; render tests.
- **Difficulty:** medium (terminal grid layout + column month labels).
- **Interfaces — CONSUMES / PRODUCES:** see toml.
- **Context pack (hints):** `src/dally/render.py` (mood_style, _nearest_mood, empty_state,
  console), `src/dally/reports.py` (Heatmap/HeatCell from task 0), `tests/test_render.py`.
  ARCHITECTURE.md §Module layout (render is pure formatting). **UX screen: S6.** DESIGN.md tokens:
  reuse the existing mood scale verbatim; airy `gh`-style density.
- **Done:** `2f7100a` — evidence `specs/002-heatmap/evidence/task-1.txt`. Verify green (62 passed).
  `heatmap_grid` prints 7 Sun..Sat rows, colored `■` cells via the shared 1–5 palette, `·` for empty
  windowed days, blank padding; month header (collision-safe) + numbered legend + empty key;
  NO_COLOR clean. Visual spot-check: trailing-52wk grid renders all 12 month labels.

## Task 2 — cli.py: `dally heatmap` command + `--year` validation

```toml
id = 2
type = "feature"
deps = [0, 1]
files = ["src/dally/cli.py", "tests/test_cli.py"]
consumes = [
  "reports.build_heatmap(today: date, year: int | None = None) -> Heatmap",
  "render.heatmap_grid(heatmap: Heatmap) -> None",
  "render.empty_state(message: str) -> None",
]
produces = [
  "console command `dally heatmap [--year YYYY]` — top-level (not under mood/report); exit 0 on success and on empty state, exit 2 on a future/malformed year",
]

[[criteria]]
text = "`dally heatmap` builds build_heatmap(date.today()) and prints the grid; `dally heatmap --year 2025` builds build_heatmap(date.today(), year=2025); heatmap is registered top-level (appears in `dally --help`, not under `mood`/`report`)"
layer = "integration"

[[criteria]]
text = "a future `--year` (> today's year) or a malformed one (non-integer) exits 2 with one plain stderr line naming the constraint/format (S4); nothing is rendered to stdout"
layer = "integration"

[[criteria]]
text = "when the window has zero logged days, prints the friendly empty state (exit 0), not a blank grid or a crash"
layer = "integration"

[[criteria]]
text = "a CliRunner test invokes `dally heatmap` and `dally heatmap --year 2025` exactly as documented and asserts exit 0 and that the grid/legend substrings appear; invokes `--year 2099` and `--year abc` and asserts exit 2 + one stderr line"
layer = "contract"

[[criteria]]
text = "the trailing-52-weeks default grid is visible end-to-end when run through the real `dally` console script"
layer = "e2e"
gate = 1
```

**Objective:** wire the command. `cli` owns validation only (ARCHITECTURE.md §Module layout) —
parse/validate `--year` (reject future year and non-integer via `_fail`, exit 2, S4), call
`reports.build_heatmap`, branch to `render.empty_state` when `total_logged == 0` (same pattern as
`_show_report`), else `render.heatmap_grid`. No business logic in `cli`.

- **Inputs:** SPEC.md ACs 4–5, 7; UX.md S6 + error states; ARCHITECTURE.md §Contract surface
  (CLI validation → exit codes), §Error handling.
- **Outputs:** `heatmap` command; CLI tests.
- **Difficulty:** easy.
- **Interfaces — CONSUMES / PRODUCES:** see toml.
- **Context pack (hints):** `src/dally/cli.py` (app, `_fail`, `_parse_date`, `_show_report`
  empty-state pattern), `src/dally/reports.py`, `src/dally/render.py`, `tests/test_cli.py`.
  ARCHITECTURE.md §Contract surface, §Error handling. **UX screens: S6, S4.**
- **Done:** `a662129` — evidence `specs/002-heatmap/evidence/task-2.txt`. Verify green (69 passed).
  Driven through the real `dally` console script: `dally heatmap` renders the trailing-52wk grid,
  `--year 2099` exits 2 (one stderr line), fresh data dir prints the friendly empty state exit 0.
  `heatmap` registered top-level (in `dally --help`).

## Task 3 — DEMO GATE 1: heatmap surface (default / --year / empty / bad input)

```toml
id = 3
type = "gate"
deps = [0, 1, 2]

[gate]
n = 1
release = false
launch = "pip install -e . && export XDG_DATA_HOME=$(mktemp -d) && dally --help"
seed = "dally mood add 4 --date <a date in the last 4 weeks>; dally mood add 2 --date <another recent date>; dally mood add 5 --date <a third> (spread across ≥2 weeks so multiple columns light up)"
unglamorous = "`dally heatmap --year 2099` (future) and `dally heatmap --year abc` (malformed) each exit 2 with one stderr line naming the constraint/format; nothing rendered to stdout"

[[gate.journey]]
step = "`dally heatmap` on the seeded data shows a 7-row grid of the trailing 52 weeks; the seeded days are colored on the 1-5 mood scale (number-legend visible), other windowed days blank"
task = 2

[[gate.journey]]
step = "the trailing-52-weeks default grid is visible end-to-end when run through the real `dally` console script"
task = 2

[[gate.journey]]
step = "`dally heatmap --year 2025` renders the full calendar year Jan-Dec with month labels; days outside the year are blank padding"
task = 2

[[gate.journey]]
step = "point XDG_DATA_HOME at a second fresh temp dir, `dally heatmap` prints the friendly empty state, exit 0 (no blank grid, no crash)"
task = 2

[[gate.journey]]
step = "the legend maps all 5 mood colors + empty cell to their meaning and names the numbers; with NO_COLOR=1 the grid still reads (numbers/labels, no reliance on color)"
task = 1
```

**Preflight (fail-closed):** journey MUST run with `XDG_DATA_HOME` exported to a fresh temp dir —
verify `echo $XDG_DATA_HOME` is a `/tmp/...` path before step 1; **abort if unset or under
`$HOME`** (would touch the real `~/.local/share/dally`). Same-composition rule: this is the
production entry point (`dally` console script) with a disposable data dir — no gate-only harness.
Seed command above provides the data the grid needs.

**Completion artifact:** human walkthrough result (observations per step; screenshots optional —
a heatmap is worth capturing). A skipped walkthrough marks this task `GATE SKIPPED` (never deleted)
and task 4's test `UNWITNESSED`; the journey must be walked at latest at the release gate.

- **Difficulty:** human time only.
- **Status:** not yet walked.

## Task 4 — Crystallize gate 1 as heatmap-journey e2e

```toml
id = 4
type = "crystallization"
gate = 1
deps = [3]
files = ["tests/test_journey.py"]

[[criteria]]
text = "an automated e2e on pytest + Typer CliRunner (harness per CONVENTIONS.md Test strategy) replays every gate-1 step — seeded default grid, --year 2025, empty state on a fresh data dir, legend/NO_COLOR — plus the unglamorous future/malformed --year step, asserting exit codes and stable substrings; joins the journey suite and is green"
layer = "e2e"
gate = 1
```

**Objective:** encode gate 1's scripted journey (all steps + unglamorous step) as
`tests/test_journey.py::test_gate1_heatmap`. If gate 1 was `GATE SKIPPED`, this task still runs
now; the test is marked `UNWITNESSED` until the journey is walked.

- **Difficulty:** easy.
- **Interfaces — CONSUMES:** the `dally heatmap` surface quoted in task 2 PRODUCES. **PRODUCES:** none.
- **Context pack (hints):** `tests/test_journey.py`, `tests/conftest.py`, gate 1 journey above;
  CONVENTIONS.md §Test strategy (assert exit codes + stable substrings, not Rich framebuffers).

## Task 5 — RELEASE GATE: heatmap through the built wheel

```toml
id = 5
type = "gate"
deps = [0, 1, 2, 4]

[gate]
n = 2
release = true
launch = "python -m build --wheel && python -m venv $VENV && $VENV/bin/pip install dist/dally-*.whl && export PATH=$VENV/bin:$PATH && export XDG_DATA_HOME=$(mktemp -d) && dally --help"
seed = "dally mood add 4 --date <a recent date>; dally mood add 2 --date <another recent date> (through the installed console script)"
unglamorous = "in a second fresh XDG_DATA_HOME (restart into a clean data dir), `dally heatmap` prints the friendly empty state, exit 0 — no crash on first run of a fresh install"

[[gate.journey]]
step = "`dally --help` on the installed wheel lists a top-level `heatmap` command (new command reachable through the production entry point, not only `pip install -e .`)"
task = 2

[[gate.journey]]
step = "`dally heatmap` on the seeded data renders the trailing-52-weeks grid with the seeded days colored on the mood scale — the production-composition proof for the delta"
task = 2

[[gate.journey]]
step = "`dally heatmap --year 2025` renders the calendar-year grid through the installed artifact"
task = 2
```

**Preflight (fail-closed):** `$VENV` and `XDG_DATA_HOME` MUST be fresh temp dirs — verify both are
`/tmp/...` paths and `XDG_DATA_HOME` is not under `$HOME` before seeding; abort otherwise. The
built wheel installed into a throwaway venv is the production composition (same-composition rule) —
the install itself is the production-composition proof this delta adds no new entry-point wiring
beyond the registered command. Seed through the installed `dally`, not `-e .`.

**Completion artifact:** human walkthrough result. A skipped walkthrough marks this task
`GATE SKIPPED` and task 6's test `UNWITNESSED`; must be walked at latest at merge.

- **Difficulty:** human time only.
- **Status:** not yet walked.

## Task 6 — Crystallize release gate as installed-heatmap e2e

```toml
id = 6
type = "crystallization"
gate = 2
deps = [5]
files = ["tests/test_journey.py"]

[[criteria]]
text = "an automated e2e on pytest + Typer CliRunner replays the release-gate journey against the same in-process console app — heatmap command present, seeded default grid, --year 2025, plus the unglamorous fresh-data-dir empty-state step — asserting exit codes and stable substrings; joins the journey suite and is green"
layer = "e2e"
gate = 2
```

**Objective:** encode gate 2's journey as `tests/test_journey.py::test_gate2_heatmap_release`.
CliRunner exercises the same registered app the wheel exposes; the wheel-install proof itself stays
the human release-gate artifact. If gate 2 was `GATE SKIPPED`, this test is `UNWITNESSED` until
the walkthrough happens.

- **Difficulty:** easy.
- **Interfaces — CONSUMES:** the `dally heatmap` surface (task 2 PRODUCES). **PRODUCES:** none.
- **Context pack (hints):** `tests/test_journey.py`, `tests/conftest.py`, gate 2 journey above;
  CONVENTIONS.md §Test strategy.
