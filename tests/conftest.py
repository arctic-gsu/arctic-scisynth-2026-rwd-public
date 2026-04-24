"""Shared test constants and markers."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
CHECKPOINTS = DATA / "checkpoints"


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: notebook-execution tests; runs under minutes, not seconds",
    )
