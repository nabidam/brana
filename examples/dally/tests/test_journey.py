"""Crystallized journey e2e tests.

Each test replays a walked demo-gate journey step-for-step through the real CLI
(Typer CliRunner, per CONVENTIONS.md §Test strategy), asserting exit codes and
stable substrings — never Rich framebuffers. Joining this suite locks the
kernel behavior against regressions. In-process invocations against a shared
temp data dir stand in for the walkthrough's cross-shell restart; the true
new-terminal restart stays a walkthrough concern.
"""

from __future__ import annotations

import os
from datetime import date, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from dally.cli import app

runner = CliRunner()


def _db_path() -> Path:
    return Path(os.environ["XDG_DATA_HOME"]) / "dally" / "dally.db"


def test_gate1_walking_skeleton(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    today = date.today().isoformat()

    # Step 1 — help exits 0 and lists both sub-apps.
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "mood" in result.stdout and "report" in result.stdout

    # Step 2 — add today's mood with a note (S1 confirmation).
    result = runner.invoke(app, ["mood", "add", "4", "--note", "good run"])
    assert result.exit_code == 0
    assert today in result.stdout
    assert "4" in result.stdout
    assert "good run" in result.stdout

    # Step 3 — backdated add (S1 confirmation with the past date).
    result = runner.invoke(app, ["mood", "add", "2", "--date", "2026-07-14"])
    assert result.exit_code == 0
    assert "2026-07-14" in result.stdout

    # Step 4 — invalid moods each exit 2 with a one-line range message.
    for bad in ["0", "6", "abc"]:
        result = runner.invoke(app, ["mood", "add", bad])
        assert result.exit_code == 2
        stderr = result.stderr.strip()
        assert "\n" not in stderr
        assert "1" in stderr and "5" in stderr

    # Step 5 — list shows both entries newest first, note intact; invalids wrote nothing.
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert result.stdout.index(today) < result.stdout.index("2026-07-14")
    assert "good run" in result.stdout

    # Step 6 — persistence: a fresh invocation against the same data dir still shows both.
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert today in result.stdout and "2026-07-14" in result.stdout

    # Unglamorous — delete the DB in the seeded dir; list recreates it empty, no crash.
    db_file = _db_path()
    assert db_file.exists()
    db_file.unlink()
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "No moods logged yet" in result.stdout

    # Step 7 — a second fresh data dir shows the friendly empty state, exit 0.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "second_home"))
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "No moods logged yet" in result.stdout
    assert "dally mood add 4" in result.stdout


def test_gate2_kernel_journey(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Gate 2 (release) kernel journey — add, backfill, list, persist, report.

    Dates are computed relative to ``date.today()`` so the report-week step stays
    inside the current ISO week on any run day. ``backdate`` is this week's Monday
    (always ≤ today, always in-window); on a Monday it collides with today, which
    the period-average assertion tolerates (mean of daily averages is 3.0 either
    way). The wheel/venv release build stays a walkthrough concern; this e2e
    crystallizes the journey's behavior through the real CLI in-process.
    """
    today = date.today()
    today_iso = today.isoformat()
    backdate = today - timedelta(days=today.weekday())  # this week's Monday, in-window
    backdate_iso = backdate.isoformat()

    # Step 1 — add today's mood with a note (S1 confirmation).
    result = runner.invoke(app, ["mood", "add", "4", "--note", "good run"])
    assert result.exit_code == 0
    assert today_iso in result.stdout
    assert "4" in result.stdout
    assert "good run" in result.stdout

    # Step 2 — backfill a missed in-week day (S1 backdated confirmation).
    result = runner.invoke(app, ["mood", "add", "2", "--date", backdate_iso])
    assert result.exit_code == 0
    assert backdate_iso in result.stdout

    # Step 3 — list shows both entries; newest first when the days are distinct.
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert today_iso in result.stdout and backdate_iso in result.stdout
    if today != backdate:
        assert result.stdout.index(today_iso) < result.stdout.index(backdate_iso)

    # Step 4 — persistence: a fresh invocation against the same data dir still shows both.
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert today_iso in result.stdout and backdate_iso in result.stdout

    # Step 5 — report week: average + per-day breakdown; unlogged days excluded.
    # Daily averages today→4.0, backdate→2.0 (or [4,2]→3.0 on a Monday); period
    # average is 3.0 either way, proving unlogged days are excluded from the mean.
    result = runner.invoke(app, ["report", "week"])
    assert result.exit_code == 0
    assert "3.0" in result.stdout
    assert today_iso in result.stdout

    # Step 6 — a unicode/emoji note survives the round trip; year report renders months.
    result = runner.invoke(app, ["mood", "add", "3", "--note", "café 🎉"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "café 🎉" in result.stdout
    result = runner.invoke(app, ["report", "year"])
    assert result.exit_code == 0
    assert "Month" in result.stdout
    assert f"{today.year}-{today.month:02d}" in result.stdout

    # Step 7 — a second fresh data dir: report month prints the friendly no-data message.
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "second_home"))
    result = runner.invoke(app, ["report", "month"])
    assert result.exit_code == 0
    assert "No data for this month" in result.stdout

    # Unglamorous — invalid and future dates exit 2 with one stderr line; nothing written.
    for bad_date in ["2026-13-45", (today + timedelta(days=5)).isoformat()]:
        result = runner.invoke(app, ["mood", "add", "3", "--date", bad_date])
        assert result.exit_code == 2
        stderr = result.stderr.strip()
        assert stderr and "\n" not in stderr
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "No moods logged yet" in result.stdout  # the rejected adds wrote nothing
