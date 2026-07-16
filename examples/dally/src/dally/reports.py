"""Report math — period resolution (ISO week / month / year) and averages.

Pure functions: ``build_report`` takes ``today`` explicitly and never touches the
clock, prints, or exits (ARCHITECTURE.md §Decision log — averages live here, not
in SQL). It reads rows through ``storage.entries_between`` and aggregates in
memory. Raises ``ValueError`` on an unknown period; never prints.

Averages follow the SPEC rule *mean of daily averages, not of raw entries*: a
day with several entries counts once, as that day's mean. The period average is
the mean of those daily averages, rounded to one decimal; empty days (and, in
the year report, empty months) contribute nothing and render as ``None``.
"""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from statistics import fmean
from typing import Literal

from dally import storage

Period = Literal["week", "month", "year"]


@dataclass(frozen=True)
class Bucket:
    # ``label`` is a stable machine string (ISO date ``YYYY-MM-DD`` for day
    # buckets, ``YYYY-MM`` for month buckets) — presentation formatting is the
    # render layer's job (task 7). Internal label-format choice, simplest that
    # round-trips a date.
    label: str
    average: float | None


@dataclass(frozen=True)
class Report:
    period: str
    start: date
    end: date
    average: float | None
    buckets: list[Bucket]


def _week_bounds(today: date) -> tuple[date, date]:
    # ISO week, Monday start (SPEC §Assumptions). weekday(): Mon=0..Sun=6.
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=6)


def _month_bounds(today: date) -> tuple[date, date]:
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.replace(day=1), today.replace(day=last_day)


def _year_bounds(today: date) -> tuple[date, date]:
    return date(today.year, 1, 1), date(today.year, 12, 31)


def _days(start: date, end: date) -> list[date]:
    span = (end - start).days
    return [start + timedelta(days=n) for n in range(span + 1)]


def _months(start: date, end: date) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def _round1(value: float) -> float:
    return round(value, 1)


def build_report(period: Period, today: date) -> Report:
    """Resolve ``period`` around ``today`` and aggregate stored moods.

    week/month → per-day buckets; year → per-month buckets. Bucket and period
    averages are means of *daily* averages, rounded to one decimal; days/months
    with no entries yield ``None`` and are excluded from the period average.
    """
    if period == "week":
        start, end = _week_bounds(today)
        granularity = "day"
    elif period == "month":
        start, end = _month_bounds(today)
        granularity = "day"
    elif period == "year":
        start, end = _year_bounds(today)
        granularity = "month"
    else:
        raise ValueError(f"unknown period {period!r}; expected week, month, or year")

    entries = storage.entries_between(start, end)

    # Exact daily averages — the aggregation unit for every downstream mean.
    moods_by_day: dict[date, list[int]] = {}
    for entry in entries:
        moods_by_day.setdefault(entry.date, []).append(entry.mood)
    daily_avg: dict[date, float] = {day: fmean(moods) for day, moods in moods_by_day.items()}

    period_average = _round1(fmean(daily_avg.values())) if daily_avg else None

    buckets: list[Bucket] = []
    if granularity == "day":
        for day in _days(start, end):
            avg = daily_avg.get(day)
            buckets.append(Bucket(day.isoformat(), _round1(avg) if avg is not None else None))
    else:
        for year, month in _months(start, end):
            month_avgs = [
                avg for day, avg in daily_avg.items() if (day.year, day.month) == (year, month)
            ]
            avg = _round1(fmean(month_avgs)) if month_avgs else None
            buckets.append(Bucket(f"{year:04d}-{month:02d}", avg))

    return Report(period=period, start=start, end=end, average=period_average, buckets=buckets)
