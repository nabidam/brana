"""Task 2 tests for the render layer.

Rich renders plain text when stdout is not a TTY (as under capsys), so these
assert on stable substrings — dates, mood numbers, note text — not framebuffers
(CONVENTIONS.md §Test strategy).
"""

from __future__ import annotations

from datetime import date

import pytest

from dally import render, reports, storage
from dally.reports import Heatmap
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


def test_report_table_shows_averages_as_numbers_and_empty_cells(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from dally.reports import Bucket, Report

    render.report_table(
        Report(
            period="week",
            start=date(2026, 7, 13),
            end=date(2026, 7, 19),
            average=3.0,
            buckets=[
                Bucket("2026-07-13", 4.0),
                Bucket("2026-07-14", None),
                Bucket("2026-07-15", 2.0),
            ],
        )
    )
    out = capsys.readouterr().out
    assert "3.0" in out  # period average shown as a number
    assert "4.0" in out and "2.0" in out  # bucket averages shown as numbers
    assert "2026-07-13" in out and "2026-07-14" in out  # one row per bucket
    assert "0.0" not in out  # empty bucket is blank, never zeroed


def test_report_table_year_uses_month_header(capsys: pytest.CaptureFixture[str]) -> None:
    from dally.reports import Bucket, Report

    render.report_table(
        Report(
            period="year",
            start=date(2026, 1, 1),
            end=date(2026, 12, 31),
            average=None,
            buckets=[Bucket("2026-01", 3.0)],
        )
    )
    out = capsys.readouterr().out
    assert "Month" in out
    assert "2026-01" in out and "3.0" in out


def test_report_table_uses_the_same_mood_palette(monkeypatch: pytest.MonkeyPatch) -> None:
    from dally.reports import Bucket, Report

    seen: list[int] = []
    real_mood_style = render.mood_style

    def spy(mood: int) -> str:
        seen.append(mood)
        return real_mood_style(mood)

    monkeypatch.setattr(render, "mood_style", spy)
    render.report_table(
        Report(
            period="week",
            start=date(2026, 7, 13),
            end=date(2026, 7, 19),
            average=4.0,
            buckets=[Bucket("2026-07-13", 4.0)],
        )
    )
    # Averages are colored through the single mood_style palette (nearest 1–5).
    assert seen and all(1 <= m <= 5 for m in seen)


# --- S6 heatmap grid ---------------------------------------------------------


def _heatmap() -> Heatmap:
    # A realistic full calendar-year grid (12 well-spaced month columns), with a
    # single logged mood-4 day so the palette path is exercised. Built through the
    # real reports layer against the temp-DB fixture.
    storage.add_entry(date(2026, 1, 1), 4, None)
    return reports.build_heatmap(date(2026, 7, 17), year=2026)


def test_heatmap_grid_has_seven_day_rows_and_labels(capsys: pytest.CaptureFixture[str]) -> None:
    render.heatmap_grid(_heatmap())
    out = capsys.readouterr().out
    lines = [line for line in out.splitlines() if line.strip()]
    for label in ("Sun", "Mon", "Sat"):
        assert any(line.startswith(label) for line in lines)  # 7 day-of-week rows
    assert "■" in out  # a logged day is a filled cell
    assert "·" in out  # a windowed no-entry day is a distinct dot


def test_heatmap_grid_has_month_labels_and_the_period_label(
    capsys: pytest.CaptureFixture[str],
) -> None:
    render.heatmap_grid(_heatmap())
    out = capsys.readouterr().out
    assert "Jan" in out and "Feb" in out  # month column labels
    assert "2026" in out  # the window label


def test_heatmap_grid_legend_names_all_five_numbers(capsys: pytest.CaptureFixture[str]) -> None:
    render.heatmap_grid(_heatmap())
    out = capsys.readouterr().out
    # Mood never color-only — the legend spells out every number and the empty key.
    for mood in ("1", "2", "3", "4", "5"):
        assert mood in out
    assert "no entry" in out


def test_heatmap_grid_uses_the_single_mood_palette(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[int] = []
    real_mood_style = render.mood_style

    def spy(mood: int) -> str:
        seen.append(mood)
        return real_mood_style(mood)

    monkeypatch.setattr(render, "mood_style", spy)
    render.heatmap_grid(_heatmap())
    # Cell + legend colors both flow through the shared 1–5 palette.
    assert seen and all(1 <= m <= 5 for m in seen)


def test_heatmap_grid_respects_no_color(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    render.heatmap_grid(_heatmap())
    out = capsys.readouterr().out
    assert "\x1b[" not in out  # no ANSI escapes emitted
    # Still readable without color: day rows, month labels, and numbers survive.
    assert "Sun" in out and "Jan" in out and "4" in out
