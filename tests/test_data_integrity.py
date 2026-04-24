"""Fast tests verifying pre-committed data files exist with expected shape.

These run on every push. If one of these fails, the week's notebooks
cannot possibly work — a student opens Day 1 and immediately hits a
FileNotFoundError or a KeyError on a renamed column.
"""
from __future__ import annotations

import pandas as pd
import pytest

from conftest import CHECKPOINTS, PROCESSED, RAW

REQUIRED_FILES = [
    (RAW, "marta_gtfs.zip",
     "Run `python setup/download_data.py`."),
    (RAW, "acs_b08301_fulton_dekalb.csv",
     "Run `python setup/download_data.py`."),
    (RAW, "acs_b08141_fulton_dekalb.csv",
     "Run `python setup/download_data.py`. "
     "NTD may need the manual-download step (CloudFlare)."),
    (PROCESSED, "rail_stops.csv",
     "Restore from a clean git clone (file is committed)."),
    (PROCESSED, "station_frequencies.csv",
     "Restore from a clean git clone (file is committed)."),
    (PROCESSED, "ntd_marta_clean.csv",
     "Restore from a clean git clone (file is committed)."),
    (PROCESSED, "ntd_marta_for_cleaning_session.csv",
     "Restore from a clean git clone (file is committed)."),
    (PROCESSED, "worldcup_reference.csv",
     "Restore from a clean git clone (file is committed)."),
    (CHECKPOINTS, "day1_output_stops.csv",
     "Restore from a clean git clone (file is committed)."),
    (CHECKPOINTS, "day2_output_cleaned_ridership.csv",
     "Restore from a clean git clone (file is committed)."),
    (CHECKPOINTS, "day2_output_station_freq_clean.csv",
     "Restore from a clean git clone (file is committed)."),
    (CHECKPOINTS, "day3_output_eda_summary.csv",
     "Restore from a clean git clone (file is committed)."),
    (CHECKPOINTS, "day4_output_demand_estimates.csv",
     "Restore from a clean git clone (file is committed)."),
]


@pytest.mark.parametrize(
    "base,name,remediation", REQUIRED_FILES,
    ids=[name for _, name, _ in REQUIRED_FILES],
)
def test_required_file_exists(base, name, remediation):
    path = base / name
    assert path.exists(), f"{path} is missing. Fix: {remediation}"
    assert path.stat().st_size > 0, f"{path} is empty. Fix: {remediation}"


def test_rail_stops_schema():
    df = pd.read_csv(PROCESSED / "rail_stops.csv")
    assert len(df) == 38, f"Expected 38 rail stations; got {len(df)}."
    for col in ("station_name", "lat", "lon"):
        assert col in df.columns, f"rail_stops.csv missing column {col}."
    names = df["station_name"].str.lower()
    assert names.str.contains("sec district").any(), "SEC District missing."


def test_worldcup_reference_schema():
    df = pd.read_csv(PROCESSED / "worldcup_reference.csv")
    for col in ("type", "name", "lat", "lon", "date"):
        assert col in df.columns, f"worldcup_reference.csv missing column {col}."
    stadium_rows = df[df["type"] == "stadium"]
    assert len(stadium_rows) == 1, "Expected exactly one stadium row."
    matches = df[df["type"] == "match"]
    assert len(matches) == 8, f"Expected 8 World Cup matches; got {len(matches)}."
    match_dates = pd.to_datetime(matches["date"])
    assert match_dates.min() >= pd.Timestamp("2026-06-15")
    assert match_dates.max() <= pd.Timestamp("2026-07-15")


def test_station_frequencies_has_stadium_neighbors():
    df = pd.read_csv(PROCESSED / "station_frequencies.csv")
    assert len(df) >= 38, f"Expected ≥38 station rows; got {len(df)}."
    names = df["station_name"].str.lower()
    assert names.str.contains("sec district").any(), "SEC District missing."
    assert names.str.contains("vine city").any(), "Vine City missing."


def test_day4_gap_grid_shape():
    df = pd.read_csv(CHECKPOINTS / "day4_output_demand_estimates.csv")
    assert len(df) == 9, f"Expected 9 scenarios in the gap grid; got {len(df)}."
    assert set(df["mode_share_scenario"].unique()) == {"low", "central", "high"}
    assert set(df["capacity_scenario"].unique()) == {
        "seated_only", "service_standard", "full_crush",
    }
    n_surplus = (df["verdict"] == "SURPLUS").sum()
    n_deficit = (df["verdict"] == "DEFICIT").sum()
    assert n_surplus == 6, f"Expected 6 surplus cells; got {n_surplus}."
    assert n_deficit == 3, f"Expected 3 deficit cells; got {n_deficit}."


def test_ntd_clean_schema():
    df = pd.read_csv(PROCESSED / "ntd_marta_clean.csv")
    assert len(df) > 100, f"Expected >100 monthly rows; got {len(df)}."
    for col in ("date", "mode", "mode_name", "upt"):
        assert col in df.columns, f"ntd_marta_clean missing column {col}."
    assert set(df["mode"].unique()) <= {"HR", "MB", "SR", "DR"}
