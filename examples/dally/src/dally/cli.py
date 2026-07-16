"""Dally CLI — the Typer app wiring the ``mood`` and ``report`` sub-apps.

Task 0 scaffold: the sub-apps are registered so ``dally --help`` lists them.
Command bodies arrive in later tasks (``mood add`` / ``mood list``: task 3;
``report``: task 7). No business logic lives here — validation and wiring only,
per ARCHITECTURE.md §Module layout (``cli → (storage, reports, render)``).
"""

from __future__ import annotations

import typer

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


if __name__ == "__main__":  # pragma: no cover
    app()
