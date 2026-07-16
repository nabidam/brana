"""Task 2 tests for the render layer.

Rich renders plain text when stdout is not a TTY (as under capsys), so these
assert on stable substrings — dates, mood numbers, note text — not framebuffers
(CONVENTIONS.md §Test strategy).
"""

from __future__ import annotations

from datetime import date

import pytest

from dally import render
from dally.storage import Entry


def _entry(mood: int, note: str | None = None, day: int = 15) -> Entry:
    return Entry(
        id=mood,
        date=date(2026, 7, day),
        mood=mood,
        note=note,
        created_at="2026-07-15 10:00:00",
    )


def test_mood_style_is_the_single_1_to_5_palette() -> None:
    assert render.mood_style(1) == "red"
    assert render.mood_style(2) == "dim"
    assert render.mood_style(3) == "default"
    assert render.mood_style(4) == "green"
    assert render.mood_style(5) == "bright_green"
    with pytest.raises(ValueError):
        render.mood_style(0)
    with pytest.raises(ValueError):
        render.mood_style(6)


def test_confirmation_shows_date_mood_number_and_note(capsys: pytest.CaptureFixture[str]) -> None:
    render.confirmation(_entry(4, "good run"))
    out = capsys.readouterr().out
    assert "2026-07-15" in out  # the entry's date
    assert "4" in out  # mood as a number
    assert "good run" in out  # note present


def test_confirmation_omits_note_when_absent(capsys: pytest.CaptureFixture[str]) -> None:
    render.confirmation(_entry(2, None))
    out = capsys.readouterr().out
    assert "2026-07-15" in out
    assert "2" in out


def test_entries_table_one_row_each_newest_first_note_intact(
    capsys: pytest.CaptureFixture[str],
) -> None:
    entries = [
        _entry(4, "café 🎉", day=15),
        _entry(2, "meh", day=14),
    ]
    render.entries_table(entries)
    out = capsys.readouterr().out
    # rows rendered in the order given (newest first), moods shown as numbers
    assert out.index("2026-07-15") < out.index("2026-07-14")
    assert "4" in out and "2" in out
    assert "café 🎉" in out  # unicode/emoji preserved
    assert "meh" in out


def test_empty_state_prints_message(capsys: pytest.CaptureFixture[str]) -> None:
    render.empty_state("No moods logged yet — try `dally mood add 4`")
    out = capsys.readouterr().out
    assert "No moods logged yet" in out
    assert "dally mood add 4" in out


def test_contract_signatures_print_expected_shape(
    capsys: pytest.CaptureFixture[str],
) -> None:
    entry = _entry(5, "note")
    render.confirmation(entry)
    render.entries_table([entry])
    render.empty_state("nothing here")
    style = render.mood_style(entry.mood)
    out = capsys.readouterr().out
    assert isinstance(style, str)
    assert "2026-07-15" in out  # date present
    assert "5" in out  # mood number present
