"""Verify the RWD track environment is healthy.

Checks:
1. Python version (>= 3.11, matches Colab default).
2. Core packages import successfully.
3. Committed data files exist in data/processed/ and data/checkpoints/.

Prints ✅ lines for each successful check and ❌ with an actionable
message for each failure. Exits with status 0 if all checks pass and
non-zero otherwise.

Run either:
    python setup/check_setup.py
    conda run -n arctic-scisynth-2026-rwd python setup/check_setup.py
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PYTHON = (3, 11)

# Keep in sync with setup/environment.yml.
REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "folium",
    "geopy",
    "openpyxl",
    "requests",
    "nbformat",
]

PROCESSED_FILES = [
    "data/processed/rail_stops.csv",
    "data/processed/station_frequencies.csv",
    "data/processed/ntd_marta_clean.csv",
    "data/processed/ntd_marta_for_cleaning_session.csv",
    "data/processed/worldcup_reference.csv",
]

CHECKPOINT_FILES = [
    "data/checkpoints/day1_output_stops.csv",
    "data/checkpoints/day2_output_cleaned_ridership.csv",
    "data/checkpoints/day2_output_station_freq_clean.csv",
    "data/checkpoints/day3_output_eda_summary.csv",
    "data/checkpoints/day4_output_demand_estimates.csv",
    "data/checkpoints/marta_map.html",
]


def check_python() -> bool:
    v = sys.version_info
    if (v.major, v.minor) < REQUIRED_PYTHON:
        print(
            f"❌ Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]}+ required; "
            f"you have {v.major}.{v.minor}.{v.micro}.\n"
            f"   Fix: conda activate arctic-scisynth-2026-rwd"
        )
        return False
    print(f"✅ Python {v.major}.{v.minor}.{v.micro}")
    return True


def check_packages() -> bool:
    ok = True
    for name in REQUIRED_PACKAGES:
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, "__version__", "?")
            print(f"✅ {name:12s} {version}")
        except ImportError as exc:
            ok = False
            print(
                f"❌ {name:12s} failed to import: {exc}\n"
                f"   Fix: conda env update -f setup/environment.yml --prune"
            )
    return ok


def check_data_files(paths: list[str], label: str) -> bool:
    ok = True
    for rel in paths:
        path = REPO_ROOT / rel
        if not path.exists():
            ok = False
            print(
                f"❌ Missing {label} file: {rel}\n"
                f"   Fix: restore from a clean git clone (files are committed)."
            )
        else:
            size_kb = path.stat().st_size / 1024
            print(f"✅ {rel} ({size_kb:.1f} KB)")
    return ok


def main() -> int:
    print("=" * 60)
    print("ARCTIC SciSynth 2026 — RWD Track — Environment Check")
    print("=" * 60)

    checks = [
        ("Python version", check_python()),
        ("Required packages", check_packages()),
        ("Processed data files", check_data_files(PROCESSED_FILES, "processed")),
        ("Checkpoint data files", check_data_files(CHECKPOINT_FILES, "checkpoint")),
    ]

    print("-" * 60)
    all_ok = all(result for _, result in checks)
    if all_ok:
        print("✅ All checks passed. You're ready for the camp.")
        return 0

    print("❌ Some checks failed — see messages above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
