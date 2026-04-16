"""End-to-end pipeline test: run solution notebooks in day order and
confirm each day regenerates its checkpoint.

Contract: after the pipeline runs, every
`data/checkpoints/day{N}_output_*.csv` should exist with the same
columns and non-trivial row count. If Day 3 doesn't produce
`day3_output_eda_summary.csv`, Day 4 can't run — this test catches
that regression.

Marked slow. Snapshots every checkpoint file (including untracked
ones) to a pytest tmp directory on setup, and restores from that
snapshot on teardown. We deliberately do NOT rely on `git checkout`
for restore — it misses untracked files and could raise inside
teardown on a dirty worktree, masking the real test failure.

Safety: never mutates `data/processed/` or `data/raw/`.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys

import pandas as pd
import pytest

from conftest import CHECKPOINTS, NBMAKE_TIMEOUT, REPO_ROOT, SOLUTIONS, DAY_NOTEBOOK_PAIRS

OUTPUT_CHECKPOINTS = [out for _, out in DAY_NOTEBOOK_PAIRS if out]

nbmake_missing = pytest.mark.skipif(
    importlib.util.find_spec("nbmake") is None,
    reason=(
        f"nbmake not importable from {sys.executable}. "
        "Run under the project env: "
        "`conda run -n arctic-scisynth-2026-rwd python -m pytest tests/ -m slow` "
        "(plain `conda activate` may be shadowed by a pyenv shim)."
    ),
)


@pytest.fixture(scope="module")
def _isolated_checkpoints(tmp_path_factory):
    backup = tmp_path_factory.mktemp("checkpoint_backup")
    original_names = []
    for f in CHECKPOINTS.iterdir():
        if f.is_file():
            shutil.copy2(f, backup / f.name)
            original_names.append(f.name)
    try:
        yield backup
    finally:
        # Delete anything the test produced that wasn't in the snapshot,
        # then restore every snapshot file byte-for-byte.
        backup_names = {p.name for p in backup.iterdir()}
        for f in CHECKPOINTS.iterdir():
            if f.is_file() and f.name not in backup_names:
                f.unlink()
        for f in backup.iterdir():
            shutil.copy2(f, CHECKPOINTS / f.name)


@pytest.mark.slow
@nbmake_missing
def test_pipeline_regenerates_all_checkpoints(_isolated_checkpoints):
    backup = _isolated_checkpoints

    for name in OUTPUT_CHECKPOINTS:
        target = CHECKPOINTS / name
        if target.exists():
            target.unlink()

    for name, expected_output in DAY_NOTEBOOK_PAIRS:
        if expected_output is None:
            continue
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--nbmake",
             f"--nbmake-timeout={NBMAKE_TIMEOUT}", SOLUTIONS / name],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0, (
            f"Pipeline failed at {name}.\n"
            f"stdout:\n{result.stdout[-1500:]}\n"
            f"stderr:\n{result.stderr[-500:]}"
        )

        produced = CHECKPOINTS / expected_output
        assert produced.exists(), (
            f"{name} ran but did not produce {expected_output}."
        )

        committed = pd.read_csv(backup / expected_output)
        fresh = pd.read_csv(produced)
        assert list(fresh.columns) == list(committed.columns), (
            f"{expected_output}: column order/set drifted.\n"
            f"  committed: {list(committed.columns)}\n"
            f"  fresh:     {list(fresh.columns)}"
        )
        assert len(fresh) == len(committed), (
            f"{expected_output}: row count drifted "
            f"({len(committed)} → {len(fresh)})."
        )
