"""Shared test constants and markers."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
CHECKPOINTS = DATA / "checkpoints"
NOTEBOOKS = REPO_ROOT / "notebooks"
SOLUTIONS = REPO_ROOT / "solutions"

NBMAKE_TIMEOUT = 300  # seconds; defensive headroom for cold CI runners

DAY_NOTEBOOK_PAIRS = [
    ("day1_00_welcome_setup.ipynb",   None),
    ("day1_explore_marta.ipynb",      "day1_output_stops.csv"),
    ("day2_cleaning_ridership.ipynb", "day2_output_cleaned_ridership.csv"),
    ("day3_eda_and_mapping.ipynb",    "day3_output_eda_summary.csv"),
    ("day4_demand_estimation.ipynb",  "day4_output_demand_estimates.csv"),
    ("day5_briefing_template.ipynb",  None),
]


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: notebook-execution tests; runs under minutes, not seconds",
    )
