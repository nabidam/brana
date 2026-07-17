"""Shared pytest fixtures.

``dally_data_dir`` redirects platformdirs to a temp dir via ``XDG_DATA_HOME`` so
no test ever touches the real user data directory (``~/.local/share/dally``).
This mirrors the demo gates, which export ``XDG_DATA_HOME`` to a disposable dir
(same-composition rule). Linux target per ARCHITECTURE.md §Stack commitment;
platformdirs honours ``XDG_DATA_HOME`` there.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def dally_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point platformdirs at a per-test temp dir; return the data-home root."""
    data_home = tmp_path / "xdg_data_home"
    monkeypatch.setenv("XDG_DATA_HOME", str(data_home))
    return data_home
