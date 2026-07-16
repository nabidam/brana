"""Persistence layer — sqlite3 connection, schema init, entry CRUD.

Storage raises on invalid input and never prints or exits (ARCHITECTURE.md
§Error handling). The DB lives at platformdirs' user data dir; the directory,
DB file, and schema are created on first connect (CREATE ... IF NOT EXISTS), so
a deleted DB is transparently recreated empty.
"""

from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import platformdirs

# DDL verbatim from ARCHITECTURE.md §Data model.
_SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    date       TEXT    NOT NULL,             -- ISO YYYY-MM-DD, local time, naive
    mood       INTEGER NOT NULL CHECK (mood BETWEEN 1 AND 5),
    note       TEXT,                          -- nullable, unicode intact
    created_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);
CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date);
"""

_COLUMNS = "id, date, mood, note, created_at"


@dataclass(frozen=True)
class Entry:
    id: int
    date: date
    mood: int
    note: str | None
    created_at: str


def _db_path() -> Path:
    return Path(platformdirs.user_data_dir("dally")) / "dally.db"


def connect() -> sqlite3.Connection:
    """Open the dally DB, ensuring its directory and schema exist first."""
    path = _db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    return conn


def _row_to_entry(row: sqlite3.Row) -> Entry:
    # Stored date is ISO TEXT; hydrate back to a datetime.date. created_at stays
    # the raw local-time string as written by the DB DEFAULT.
    return Entry(
        id=row["id"],
        date=date.fromisoformat(row["date"]),
        mood=row["mood"],
        note=row["note"],
        created_at=row["created_at"],
    )


def add_entry(date: date, mood: int, note: str | None) -> Entry:
    """Insert one mood entry and return the saved row.

    Raises ValueError on a mood outside 1–5 (also enforced by the table CHECK),
    writing nothing.
    """
    if not 1 <= mood <= 5:
        raise ValueError(f"mood must be between 1 and 5, got {mood}")
    with closing(connect()) as conn, conn:
        cursor = conn.execute(
            "INSERT INTO entries (date, mood, note) VALUES (?, ?, ?)",
            (date.isoformat(), mood, note),
        )
        row = conn.execute(
            f"SELECT {_COLUMNS} FROM entries WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return _row_to_entry(row)


def list_entries(limit: int = 30) -> list[Entry]:
    """Return up to ``limit`` entries, newest date first, then newest created_at.

    ``id DESC`` is the final tiebreaker so same-second inserts stay deterministic
    (id is monotonic with insertion order) — an internal ordering choice.
    """
    with closing(connect()) as conn:
        rows = conn.execute(
            f"SELECT {_COLUMNS} FROM entries ORDER BY date DESC, created_at DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [_row_to_entry(row) for row in rows]


def entries_between(start: date, end: date) -> list[Entry]:
    """Return entries with date in [start, end] inclusive, oldest first.

    ISO date TEXT sorts lexically == chronologically, so BETWEEN is an inclusive
    calendar range.
    """
    with closing(connect()) as conn:
        rows = conn.execute(
            f"SELECT {_COLUMNS} FROM entries "
            "WHERE date BETWEEN ? AND ? "
            "ORDER BY date ASC, created_at ASC, id ASC",
            (start.isoformat(), end.isoformat()),
        ).fetchall()
    return [_row_to_entry(row) for row in rows]
