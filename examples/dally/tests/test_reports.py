"""Task 6 tests for report math — period bounds + mean-of-daily-averages.

Pure-function tests pass fixed ``today`` dates (never patch the clock,
CONVENTIONS.md §Test strategy). One integration test seeds a real temp-dir DB
via ``storage.add_entry`` and asserts ``build_report`` aggregates the stored
rows.
"""

from __future__ import annotations

from datetime import date

from dally import reports, storage
from dally.reports import Bucket, Report

# --- period resolution [unit] ------------------------------------------------


def test_week_bounds_iso_monday_to_sunday() -> None:
    # 2026-07-15 is a Wednesday → ISO week Mon 2026-07-13 .. Sun 2026-07-19.
    report = reports.build_report("week", date(2026, 7, 15))
    assert report.start == date(2026, 7, 13)
    assert report.end == date(2026, 7, 19)
    assert [b.label for b in report.buckets] == [
        "2026-07-13",
        "2026-07-14",
        "2026-07-15",
        "2026-07-16",
        "2026-07-17",
        "2026-07-18",
        "2026-07-19",
    ]


def test_week_bounds_when_today_is_monday_and_sunday() -> None:
    monday = reports.build_report("week", date(2026, 7, 13))
    assert (monday.start, monday.end) == (date(2026, 7, 13), date(2026, 7, 19))
    sunday = reports.build_report("week", date(2026, 7, 19))
    assert (sunday.start, sunday.end) == (date(2026, 7, 13), date(2026, 7, 19))


def test_month_bounds_calendar_month_with_day_buckets() -> None:
    report = reports.build_report("month", date(2026, 2, 10))
    assert report.start == date(2026, 2, 1)
    assert report.end == date(2026, 2, 28)  # 2026 is not a leap year
    assert len(report.buckets) == 28
    assert report.buckets[0].label == "2026-02-01"
    assert report.buckets[-1].label == "2026-02-28"


def test_year_bounds_calendar_year_with_month_buckets() -> None:
    report = reports.build_report("year", date(2026, 7, 17))
    assert report.start == date(2026, 1, 1)
    assert report.end == date(2026, 12, 31)
    assert [b.label for b in report.buckets] == [f"2026-{m:02d}" for m in range(1, 13)]


# --- averages: mean of daily averages, rounded 1 decimal [unit] --------------


def test_multi_entry_day_counts_as_its_average() -> None:
    storage.add_entry(date(2026, 7, 15), 5, None)
    storage.add_entry(date(2026, 7, 15), 2, None)  # same day → mean 3.5
    report = reports.build_report("week", date(2026, 7, 15))
    day = next(b for b in report.buckets if b.label == "2026-07-15")
    assert day.average == 3.5


def test_period_average_is_mean_of_daily_averages_not_raw_entries() -> None:
    # Day A: two entries 5,2 → daily avg 3.5. Day B: one entry 2 → daily avg 2.0.
    # Mean of daily averages = (3.5 + 2.0) / 2 = 2.75 → 2.8 (not raw mean 3.0).
    storage.add_entry(date(2026, 7, 13), 5, None)
    storage.add_entry(date(2026, 7, 13), 2, None)
    storage.add_entry(date(2026, 7, 14), 2, None)
    report = reports.build_report("week", date(2026, 7, 15))
    assert report.average == 2.8


def test_year_month_bucket_is_mean_of_that_months_daily_averages() -> None:
    # January: day1 daily-avg 4.0 (two entries 5,3), day2 daily-avg 1.0.
    # Month bucket = mean of daily averages = (4.0 + 1.0) / 2 = 2.5.
    storage.add_entry(date(2026, 1, 5), 5, None)
    storage.add_entry(date(2026, 1, 5), 3, None)
    storage.add_entry(date(2026, 1, 20), 1, None)
    report = reports.build_report("year", date(2026, 7, 17))
    jan = next(b for b in report.buckets if b.label == "2026-01")
    assert jan.average == 2.5


# --- empty units → None, excluded from period average [unit] -----------------


def test_empty_days_are_none_and_excluded_from_period_average() -> None:
    storage.add_entry(date(2026, 7, 15), 4, None)  # only one logged day
    report = reports.build_report("week", date(2026, 7, 15))
    logged = [b for b in report.buckets if b.average is not None]
    empty = [b for b in report.buckets if b.average is None]
    assert len(logged) == 1 and logged[0].label == "2026-07-15"
    assert len(empty) == 6  # the other six days
    assert report.average == 4.0  # mean over the single logged day only


def test_empty_months_are_none_in_year_report() -> None:
    storage.add_entry(date(2026, 3, 10), 3, None)
    report = reports.build_report("year", date(2026, 7, 17))
    mar = next(b for b in report.buckets if b.label == "2026-03")
    assert mar.average == 3.0
    assert all(b.average is None for b in report.buckets if b.label != "2026-03")
    assert report.average == 3.0


def test_zero_entry_period_yields_none_average() -> None:
    report = reports.build_report("month", date(2026, 7, 17))
    assert report.average is None
    assert all(b.average is None for b in report.buckets)


# --- integration: real temp DB seeded via storage.add_entry ------------------


def test_build_report_aggregates_stored_rows() -> None:
    # Entries inside and outside the week window; only in-window rows aggregate.
    storage.add_entry(date(2026, 7, 13), 4, "in")
    storage.add_entry(date(2026, 7, 14), 2, "in")
    storage.add_entry(date(2026, 7, 14), 4, "in")  # day avg 3.0
    storage.add_entry(date(2026, 7, 6), 1, "prev week")  # excluded
    storage.add_entry(date(2026, 7, 20), 5, "next week")  # excluded

    report = reports.build_report("week", date(2026, 7, 15))
    assert report.start == date(2026, 7, 13)
    # daily averages in-window: 2026-07-13 → 4.0, 2026-07-14 → 3.0.
    assert report.average == 3.5
    labelled = {b.label: b.average for b in report.buckets}
    assert labelled["2026-07-13"] == 4.0
    assert labelled["2026-07-14"] == 3.0
    assert labelled["2026-07-15"] is None


# --- contract: exact signature for all three literals [contract] -------------


def test_build_report_contract_shape_all_periods() -> None:
    for period in ("week", "month", "year"):
        report = reports.build_report(period, date(2026, 7, 17))  # type: ignore[arg-type]
        assert isinstance(report, Report)
        assert report.period == period
        assert isinstance(report.start, date)
        assert isinstance(report.end, date)
        assert report.average is None or isinstance(report.average, float)
        assert isinstance(report.buckets, list)
        for bucket in report.buckets:
            assert isinstance(bucket, Bucket)
            assert isinstance(bucket.label, str)
            assert bucket.average is None or isinstance(bucket.average, float)
