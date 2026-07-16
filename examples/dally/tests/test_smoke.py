"""Task 0 smoke tests.

Covers the scaffold's acceptance criteria: the package imports, ``dally --help``
exits 0 and lists both sub-apps, and the data-dir fixture isolates platformdirs
from the real user directory.
"""

from __future__ import annotations

from pathlib import Path

import platformdirs
import pytest
from typer.testing import CliRunner

from dally.cli import app

runner = CliRunner()


def test_help_exits_zero_and_lists_subapps() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "mood" in result.stdout
    assert "report" in result.stdout


def test_data_dir_fixture_isolates_from_real_dir(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # The autouse fixture has already pointed platformdirs at a temp dir, so any
    # write dally makes lands under the test's tmp_path.
    isolated = Path(platformdirs.user_data_dir("dally"))
    assert tmp_path in isolated.parents

    # Compute the real dir with the override removed: it must differ from the
    # isolated one, and the isolated path must not live under it — proving no
    # test can write to the real user data directory.
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    real = Path(platformdirs.user_data_dir("dally"))
    assert isolated != real
    assert not isolated.is_relative_to(real)
