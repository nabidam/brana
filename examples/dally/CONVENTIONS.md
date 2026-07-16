# Dally — CONVENTIONS (lite)

Living doc — current truth for how code is written here.

## Naming

- Modules/functions/variables: `snake_case`; dataclasses: `PascalCase` (`Entry`, `Report`).
- CLI command names and flags exactly as SPEC.md spells them (`dally mood add`, `--note`, `--date`).
- Test files: `tests/test_<module>.py`; journey tests: `tests/test_journey.py`.

## Folder rules

- `src/dally/` only — the four modules ARCHITECTURE.md names (`cli.py`, `storage.py`, `reports.py`, `render.py`). New module = ARCHITECTURE.md patch first.
- Dependency direction per ARCHITECTURE.md: `cli → (storage, reports, render)`; `reports → storage`; `render` pure formatting. No module imports `cli`.
- Tests in `tests/`, no `src` pollution; shared fixtures in `tests/conftest.py`.

## Error handling

- Validation caught in `cli.py`: one line to stderr naming what was wrong and what valid looks like, exit 2, nothing written.
- Unexpected exceptions: top-level handler, one line to stderr, exit 1 — never a traceback in normal use.
- `storage`/`reports` raise (`ValueError`); they never print or exit.

## Test strategy

| Layer | Verifies | Framework |
|-------|----------|-----------|
| `[unit]` | report math (period bounds, daily/period averages), mood/date validation helpers | pytest |
| `[integration]` | storage against a real temp-dir SQLite DB (schema init, add/list/range, persistence, recreate-after-delete) | pytest + `tmp_path` data-dir fixture |
| `[e2e]` | kernel journey + empty/error states via the real CLI: exit codes, stdout/stderr text | pytest + Typer `CliRunner` (harness per ARCHITECTURE.md) |

- No mocks for SQLite — always a real temp DB. `reports.build_report` takes `today: date` explicitly; tests pass fixed dates, never patch the clock.
- e2e asserts on exit code and stable substrings (dates, mood numbers, error phrases), not full Rich framebuffers.
- **Verify script** (single fail-closed gate for every task and demo gate): `bash tools/verify.sh` — runs, in order, `ruff check` · `ruff format --check` · `mypy` (strict on `src/`) · `pip-audit` (dally's own dependency closure, resolved fresh — not the ambient env) · `detect-secrets` (secret scan) · `pytest`. Any non-zero check aborts. Requires network (dependency + advisory-DB lookups).

## Run

- Install + smoke: `pip install -e ".[dev]"` then `dally --help` (exits 0, lists the `mood` and `report` sub-apps). Python 3.11+.
- Release build (release gate): `python -m build --wheel`, install the wheel into a fresh venv, run `dally`.
- **CI:** the app lives at `examples/dally/` inside the `brana` workflow repo, not its own repository. Repo-root CI would fire on every unrelated brana docs push, so CI wiring is deferred to the parent repo's concern; `tools/verify.sh` is the local gate and is what a dally-scoped CI job would call.

## Lint-over-prose (Task 0)

Ruff enforces naming, import order, line length (100), and format; mypy (strict on `src/`) enforces the contract-surface type hints. Prose above covers only what lint can't see (dependency direction, error-message shape).

## Output style (≤5 rules)

1. Mood color scale defined once in `render.py` (1→5: red → dim → neutral → green → bright green) — S1/S2/S3 all use it; never a second palette.
2. Never color-only: mood always printed as its number; Rich's native `NO_COLOR` support must stay unbroken (no manual ANSI codes).
3. One table per invocation, `gh`-style quiet color: default terminal foreground for data, color only on mood values and the confirmation check.
4. Empty states are friendly one-liners suggesting the next command (per UX.md), exit 0.
5. stderr is plain text (no Rich markup) — one actionable line.

## Commit style

Conventional commits (`feat:`, `fix:`, `test:`, `chore:`, `docs:`), imperative, ≤72-char subject. One task per commit; commit message names the task id (`feat: mood add command (task 3)`).
