"""Task 0 tests for heatmap window/grid math — ``reports.build_heatmap``.

Pure-function tests pass fixed ``today`` dates (never patch the clock,
CONVENTIONS.md §Test strategy). One integration test seeds a real temp-dir DB
via ``storage.add_entry`` and asserts each entry lands in the correct
(week-column, day-of-week-row) cell.
"""

from __future__ import annotations

from datetime import date, timedelta

from dally import reports, storage
from dally.reports import HeatCell, Heatmap


# Sunday-indexed day-of-week: Sun=0 .. Sat=6 (date.weekday() is Mon=0 .. Sun=6).
def _dow(d: date) -> int:
    return (d.weekday() + 1) % 7


def _cell_for(heatmap: Heatmap, d: date) -> HeatCell:
    """Locate the grid cell whose ``day`` equals ``d`` (must be a windowed day)."""
    for week in heatmap.weeks:
        for cell in week:
            if cell.day == d:
                return cell
    raise AssertionError(f"{d} not found as a windowed cell")


# --- default window: trailing 52 weeks [unit] --------------------------------


def test_default_window_is_trailing_52_weeks() -> None:
    today = date(2026, 7, 15)  # Wednesday
    heatmap = reports.build_heatmap(today)
    assert heatmap.label == "past 52 weeks"
    assert len(heatmap.weeks) == 53  # 53 week columns
    # First column starts on the Sunday on/before (today - 52 weeks).
    sunday_of_today = today - timedelta(days=_dow(today))  # 2026-07-12
    assert heatmap.start == sunday_of_today - timedelta(weeks=52)  # 2025-07-13
    assert heatmap.start.weekday() == 6  # a Sunday
    # Every inner week list has length 7, indexed Sunday..Saturday.
    assert all(len(week) == 7 for week in heatmap.weeks)
    # The last column contains today.
    assert any(cell.day == today for cell in heatmap.weeks[-1])
    # today sits in its Sunday-indexed row.
    assert heatmap.weeks[-1][_dow(today)].day == today


def test_days_after_today_in_current_week_are_padding() -> None:
    today = date(2026, 7, 15)  # Wednesday → Thu..Sat of this week are future
    heatmap = reports.build_heatmap(today)
    last_col = heatmap.weeks[-1]
    for row in range(_dow(today) + 1, 7):  # rows after today
        assert last_col[row] == HeatCell(day=None, average=None)


# --- calendar-year window [unit] ---------------------------------------------


def test_year_window_spans_jan1_to_dec31_with_padding() -> None:
    heatmap = reports.build_heatmap(date(2026, 7, 17), year=2025)
    assert heatmap.label == "2025"
    assert heatmap.start == date(2025, 1, 1)
    assert heatmap.end == date(2025, 12, 31)
    # First column is the week containing Jan 1; days before Jan 1 are padding.
    first_col = heatmap.weeks[0]
    assert any(cell.day == date(2025, 1, 1) for cell in first_col)
    pre = [cell for cell in first_col if cell.day is None]
    assert pre and all(cell.average is None for cell in pre)
    # Last column is the week containing Dec 31; days after are padding.
    last_col = heatmap.weeks[-1]
    assert any(cell.day == date(2025, 12, 31) for cell in last_col)
    post = [cell for cell in last_col if cell.day is None]
    assert post and all(cell.average is None for cell in post)


# --- cell coloring source: daily average [unit] ------------------------------


def test_single_multi_and_empty_days() -> None:
    today = date(2026, 7, 15)
    storage.add_entry(date(2026, 7, 13), 4, None)  # single entry
    storage.add_entry(date(2026, 7, 14), 5, None)  # multi → mean 3.0
    storage.add_entry(date(2026, 7, 14), 1, None)
    heatmap = reports.build_heatmap(today)
    assert _cell_for(heatmap, date(2026, 7, 13)).average == 4.0
    assert _cell_for(heatmap, date(2026, 7, 14)).average == 3.0
    # A windowed day with no entry is a real cell with average None (not padding).
    empty = _cell_for(heatmap, date(2026, 7, 15))
    assert empty.day == date(2026, 7, 15) and empty.average is None
    assert heatmap.total_logged == 2  # two distinct logged days


def test_zero_entries_reports_total_logged_zero() -> None:
    heatmap = reports.build_heatmap(date(2026, 7, 15))
    assert heatmap.total_logged == 0
    assert all(cell.average is None for week in heatmap.weeks for cell in week)


# --- integration: real temp DB, correct grid placement -----------------------


def test_entries_land_in_correct_grid_cells() -> None:
    today = date(2026, 7, 15)
    d1, d2 = date(2026, 6, 1), date(2026, 7, 14)  # different weeks
    storage.add_entry(d1, 2, "past")
    storage.add_entry(d2, 5, "recent")
    # An entry outside the window must not appear.
    storage.add_entry(date(2024, 1, 1), 3, "way before window")
    heatmap = reports.build_heatmap(today)
    c1, c2 = _cell_for(heatmap, d1), _cell_for(heatmap, d2)
    assert c1.average == 2.0 and c2.average == 5.0
    # Each entry sits in the row matching its Sunday-indexed weekday.
    assert heatmap.weeks[(d1 - heatmap.start).days // 7][_dow(d1)] == c1
    assert heatmap.total_logged == 2  # the pre-2024 entry is out of window


# --- daily_averages shared helper [unit] -------------------------------------


def test_daily_averages_helper() -> None:
    storage.add_entry(date(2026, 7, 13), 4, None)
    storage.add_entry(date(2026, 7, 13), 2, None)  # mean 3.0
    storage.add_entry(date(2026, 7, 14), 5, None)
    entries = storage.entries_between(date(2026, 7, 13), date(2026, 7, 14))
    avgs = reports.daily_averages(entries)
    assert avgs == {date(2026, 7, 13): 3.0, date(2026, 7, 14): 5.0}


# --- contract: exact signature + shapes [contract] ---------------------------


def test_build_heatmap_contract_shape() -> None:
    for heatmap in (
        reports.build_heatmap(date(2026, 7, 17)),
        reports.build_heatmap(date(2026, 7, 17), year=2025),
    ):
        assert isinstance(heatmap, Heatmap)
        assert isinstance(heatmap.start, date)
        assert isinstance(heatmap.end, date)
        assert isinstance(heatmap.label, str)
        assert isinstance(heatmap.total_logged, int)
        assert isinstance(heatmap.weeks, list)
        for week in heatmap.weeks:
            assert isinstance(week, list) and len(week) == 7
            for cell in week:
                assert isinstance(cell, HeatCell)
                assert cell.day is None or isinstance(cell.day, date)
                assert cell.average is None or isinstance(cell.average, float)
