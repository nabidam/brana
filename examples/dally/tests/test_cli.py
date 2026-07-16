"""Task 3 tests for the CLI commands.

Drives the real Typer app in-process via CliRunner (ARCHITECTURE.md §Test
harness). Click 8.4 separates streams, so confirmations/tables are asserted on
``result.stdout`` and validation errors on ``result.stderr``. Dates are relative
to ``date.today()`` so the suite never couples to a wall-clock literal. The
autouse ``dally_data_dir`` fixture gives each test a throwaway DB.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from typer.testing import CliRunner

from dally import cli, storage
from dally.cli import app

runner = CliRunner()


def _iso(days_ago: int) -> str:
    return (date.today() - timedelta(days=days_ago)).isoformat()


def test_add_prints_confirmation_with_today_mood_and_note() -> None:
    result = runner.invoke(app, ["mood", "add", "4", "--note", "good run"])
    assert result.exit_code == 0
    assert date.today().isoformat() in result.stdout
    assert "4" in result.stdout
    assert "good run" in result.stdout


def test_add_backdated_confirms_the_past_date() -> None:
    past = _iso(2)
    result = runner.invoke(app, ["mood", "add", "2", "--date", past])
    assert result.exit_code == 0
    assert past in result.stdout


@pytest.mark.parametrize("bad_mood", ["0", "6", "abc"])
def test_invalid_mood_exits_2_with_one_line_naming_range(bad_mood: str) -> None:
    result = runner.invoke(app, ["mood", "add", bad_mood])
    assert result.exit_code == 2
    stderr = result.stderr.strip()
    assert "\n" not in stderr  # single line
    assert "1" in stderr and "5" in stderr  # names the valid range


def test_invalid_adds_write_nothing() -> None:
    for bad in ["0", "6", "abc"]:
        runner.invoke(app, ["mood", "add", bad])
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "No moods logged yet" in result.stdout


def test_list_shows_both_entries_newest_first_note_intact() -> None:
    runner.invoke(app, ["mood", "add", "4", "--note", "good run", "--date", _iso(1)])
    runner.invoke(app, ["mood", "add", "2", "--note", "café 🎉"])  # today
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert result.stdout.index(date.today().isoformat()) < result.stdout.index(_iso(1))
    assert "café 🎉" in result.stdout
    assert "good run" in result.stdout


def test_list_empty_state_suggests_add_exit_0() -> None:
    result = runner.invoke(app, ["mood", "list"])
    assert result.exit_code == 0
    assert "No moods logged yet" in result.stdout
    assert "dally mood add 4" in result.stdout


def test_malformed_and_future_dates_exit_2_write_nothing() -> None:
    malformed = runner.invoke(app, ["mood", "add", "3", "--date", "2026-13-45"])
    assert malformed.exit_code == 2
    assert "YYYY-MM-DD" in malformed.stderr
    assert "\n" not in malformed.stderr.strip()

    future = runner.invoke(app, ["mood", "add", "3", "--date", _iso(-1)])
    assert future.exit_code == 2
    assert "future" in future.stderr.lower()

    listed = runner.invoke(app, ["mood", "list"])
    assert listed.exit_code == 0
    assert "No moods logged yet" in listed.stdout


def test_contract_commands_drive_exit_codes_and_shape() -> None:
    ok = runner.invoke(app, ["mood", "add", "5", "--note", "x", "--date", date.today().isoformat()])
    assert ok.exit_code == 0
    assert date.today().isoformat() in ok.stdout

    listed = runner.invoke(app, ["mood", "list"])
    assert listed.exit_code == 0

    bad = runner.invoke(app, ["mood", "add", "9"])
    assert bad.exit_code == 2
    assert bad.stderr.strip()


def test_main_converts_unexpected_error_to_exit_1_no_traceback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["dally", "mood", "list"])

    def boom() -> list[storage.Entry]:
        raise RuntimeError("db exploded")

    monkeypatch.setattr(storage, "list_entries", boom)

    with pytest.raises(SystemExit) as excinfo:
        cli.main()
    assert excinfo.value.code == 1
    err = capsys.readouterr().err
    assert "unexpected error" in err
    assert "Traceback" not in err
