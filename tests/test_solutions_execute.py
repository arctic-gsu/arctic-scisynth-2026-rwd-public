"""Execute every solution notebook end-to-end via nbmake.

Marked slow — takes a few minutes. Skip with `pytest -m "not slow"`.

Single-pytest invocation: we collect all six solutions into one
`pytest --nbmake` run rather than spawning a subprocess per notebook.
Identical coverage; one pytest boot instead of seven.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys

import pytest

from conftest import NBMAKE_TIMEOUT, REPO_ROOT, SOLUTIONS, DAY_NOTEBOOK_PAIRS

SOLUTION_PATHS = [SOLUTIONS / name for name, _ in DAY_NOTEBOOK_PAIRS]

# nbmake must be importable from whichever interpreter pytest is running
# under — not just any `pytest` on PATH. Skip the slow test with a clear
# message if it isn't (common cause: forgot to `conda activate`).
nbmake_missing = pytest.mark.skipif(
    importlib.util.find_spec("nbmake") is None,
    reason=(
        f"nbmake not importable from {sys.executable}. "
        "Run under the project env: "
        "`conda run -n arctic-scisynth-2026-rwd python -m pytest tests/ -m slow` "
        "(plain `conda activate` may be shadowed by a pyenv shim)."
    ),
)


@pytest.mark.slow
@nbmake_missing
def test_every_solution_executes():
    for path in SOLUTION_PATHS:
        assert path.exists(), f"{path} is missing."
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--nbmake",
         f"--nbmake-timeout={NBMAKE_TIMEOUT}", *SOLUTION_PATHS],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, (
        f"One or more solution notebooks failed to execute.\n"
        f"stdout:\n{result.stdout[-3000:]}\n"
        f"stderr:\n{result.stderr[-1000:]}"
    )
