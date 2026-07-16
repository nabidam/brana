"""Task 1 tests for the persistence layer.

Real temp-dir SQLite only (no mocks), per CONVENTIONS.md §Test strategy. The
autouse ``dally_data_dir`` fixture points platformdirs at a temp dir, so every
call here writes to a throwaway DB.
"""

from __future__ import annotations

import dataclasses
from datetime import date
from pathlib import Path

import pytest

from dally import storage


def test_add_then_list_roundtrip() -> None:
    saved = storage.add_entry(date(2026, 7, 15), 4, "great day 🎉 café")
    listed = storage.list_entries()

    assert len(listed) == 1
    got = listed[0]
    assert got.id == saved.id
    assert got.date == date(2026, 7, 15)
    assert got.mood == 4
    assert got.note == "great day 🎉 café"  # unicode/emoji round-trips


def test_fresh_connect_creates_then_recreates_after_delete(dally_data_dir: Path) -> None:
    storage.add_entry(date(2026, 7, 15), 3, None)
    assert storage.list_entries()  # first connect built dir + DB + schema

    db_file = dally_data_dir / "dally" / "dally.db"
    assert db_file.exists()

    db_file.unlink()  # delete the DB between calls
    assert storage.list_entries() == []  # recreated empty, no crash

    storage.add_entry(date(2026, 7, 16), 2, None)
    assert len(storage.list_entries()) == 1


def test_ordering_inclusive_range_and_same_day_duplicates() -> None:
    d1, d2, d3 = date(2026, 7, 10), date(2026, 7, 12), date(2026, 7, 15)
    storage.add_entry(d1, 1, "old")
    storage.add_entry(d2, 3, "mid-a")
    storage.add_entry(d2, 5, "mid-b")  # same-day duplicate, inserted later
    storage.add_entry(d3, 2, "new")

    listed = storage.list_entries()
    assert [e.date for e in listed] == [d3, d2, d2, d1]  # newest date first

    same_day = [e for e in listed if e.date == d2]
    assert len(same_day) == 2  # duplicates persist as separate rows
    assert same_day[0].note == "mid-b"  # later insert sorts newest-first

    ranged = storage.entries_between(d1, d2)
    assert {e.date for e in ranged} == {d1, d2}  # inclusive of both bounds
    assert d3 not in {e.date for e in ranged}

    exact = storage.entries_between(d2, d2)
    assert len(exact) == 2 and all(e.date == d2 for e in exact)


@pytest.mark.parametrize("bad_mood", [0, 6, -1, 100])
def test_add_entry_rejects_out_of_range_mood(bad_mood: int) -> None:
    with pytest.raises(ValueError):
        storage.add_entry(date(2026, 7, 15), bad_mood, "nope")
    assert storage.list_entries() == []  # nothing written


def test_contract_signatures_and_entry_shape() -> None:
    entry = storage.add_entry(date(2026, 7, 15), 4, "note")
    assert isinstance(entry, storage.Entry)
    assert (entry.date, entry.mood, entry.note) == (date(2026, 7, 15), 4, "note")
    assert isinstance(entry.id, int)
    assert isinstance(entry.created_at, str)

    assert isinstance(storage.list_entries(limit=30), list)
    assert isinstance(storage.entries_between(date(2026, 7, 1), date(2026, 7, 31)), list)

    with pytest.raises(dataclasses.FrozenInstanceError):
        entry.mood = 5  # type: ignore[misc]
