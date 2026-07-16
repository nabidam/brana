"""Dally CLI — the Typer app wiring the ``mood`` and ``report`` sub-apps.

``cli`` owns argument parsing, validation, and exit codes only — no business
logic (ARCHITECTURE.md §Module layout, ``cli → (storage, reports, render)``).
Validation errors print one plain line to stderr and exit 2 (S4). ``main`` is a
top-level safety net turning any unexpected exception into a one-line stderr
message and exit 1 — never a traceback (ARCHITECTURE.md §Error handling).
"""

from __future__ import annotations

import sys
from datetime import date
from typing import NoReturn

import typer

from dally import render, storage

app = typer.Typer(
    name="dally",
    help="Track your daily mood from the terminal.",
    no_args_is_help=True,
    add_completion=False,
)

mood_app = typer.Typer(help="Log and list mood entries.", no_args_is_help=True)
report_app = typer.Typer(help="View mood averages over time.", no_args_is_help=True)

app.add_typer(mood_app, name="mood")
app.add_typer(report_app, name="report")


@mood_app.callback()
def mood() -> None:
    """Log and list mood entries."""


@report_app.callback()
def report() -> None:
    """View mood averages over time."""


def _fail(message: str) -> NoReturn:
    """Emit one plain stderr line and exit 2 (validation error, S4)."""
    typer.echo(message, err=True)
    raise typer.Exit(2)


def _parse_mood(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError:
        _fail("mood must be a whole number between 1 and 5")
    if not 1 <= value <= 5:
        _fail("mood must be between 1 and 5")
    return value


def _parse_date(raw: str | None) -> date:
    if raw is None:
        return date.today()
    try:
        parsed = date.fromisoformat(raw)
    except ValueError:
        _fail("date must be in YYYY-MM-DD format")
    if parsed > date.today():
        _fail("date must not be in the future")
    return parsed


@mood_app.command("add")
def add(
    mood: str = typer.Argument(..., metavar="1-5", help="Mood on a 1-5 scale."),
    note: str | None = typer.Option(None, "--note", help="Optional note for the entry."),
    date_str: str | None = typer.Option(
        None, "--date", metavar="YYYY-MM-DD", help="Entry date (default: today)."
    ),
) -> None:
    """Log a mood entry and print a confirmation (S1)."""
    mood_value = _parse_mood(mood)
    entry_date = _parse_date(date_str)
    entry = storage.add_entry(entry_date, mood_value, note)
    render.confirmation(entry)


@mood_app.command("list")
def list_moods() -> None:
    """List recent mood entries, newest first (S2)."""
    entries = storage.list_entries()
    if not entries:
        render.empty_state("No moods logged yet — try `dally mood add 4`")
        return
    render.entries_table(entries)


def main() -> None:
    """Console-script entry point with a top-level exception safety net."""
    try:
        app()
    except Exception:
        print("dally: unexpected error", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
