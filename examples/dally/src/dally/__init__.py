"""Dally — a terminal mood tracker.

Package layout (ARCHITECTURE.md §Module layout):
    cli.py       Typer apps, arg parsing, exit codes — no business logic
    storage.py   sqlite3 connection, schema init, add/list/query functions
    reports.py   period resolution, daily + period averages
    render.py    Rich tables, confirmations, empty states, mood color scale
"""

__version__ = "0.1.0"
