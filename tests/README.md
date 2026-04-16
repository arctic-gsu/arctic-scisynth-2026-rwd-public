# Tests

Pytest suite that keeps the curriculum's committed artifacts
executable and self-consistent. Four test files, two categories
(fast / slow).

## What each file covers

| File | Category | What it verifies |
|---|---|---|
| `test_data_integrity.py` | fast | Pre-committed data files exist; `worldcup_reference.csv` has 8 matches in the June 15–July 15 window; `rail_stops.csv` has 38 rows; `day4_output_demand_estimates.csv` is 9 scenarios with 6 surplus / 3 deficit. |
| `test_student_notebooks.py` | fast | Student ↔ solution parity (same code-cell count, student has `???`, solution has no `???`, student notebooks have no committed outputs). |
| `test_solutions_execute.py` | slow | Every solution notebook runs end-to-end via nbmake. |
| `test_pipeline_e2e.py` | slow | Back up all checkpoints, delete them, re-run solutions in day order, confirm each day regenerates its checkpoint with the same schema. `git checkout` restores on teardown. |

## Run

**Use the project env's Python** — the slow suite needs `nbmake`,
which is only installed in the project env, not your system Python.
If you use pyenv, its `pytest` shim may shadow the conda env even
after `conda activate`. The simplest robust invocation:

```bash
conda run -n arctic-scisynth-2026-rwd python -m pytest tests/ -m slow
```

Without the right Python, slow tests **skip** with a clear message
(rather than fail obscurely on an `unrecognized arguments: --nbmake`
error from the outer shell's pytest).

```bash
# Fast tests (~5 seconds); works in any env with pandas + pytest
pytest tests/ -m "not slow"

# Slow tests (~3-5 minutes); requires the conda env for nbmake
pytest tests/ -m slow

# Everything
pytest tests/

# Just the solution-execution sweep directly (also needs nbmake)
pytest --nbmake solutions/
```

## When to run which

- **On every commit / push:** fast suite.
- **Before a PR to main:** full suite.
- **After touching a notebook:** at minimum `pytest tests/test_student_notebooks.py -k "<dayN>"` and the corresponding `test_solutions_execute.py -k "<dayN>"`.
- **After touching `setup/` or `data/processed/`:** full suite + re-run the pipeline (`test_pipeline_e2e.py`).
- **After the late-May preflight data re-validation:** full suite.

## Design notes

### Why no hand-filled student pipeline directory?

SPEC Phase 5 task 4 called for a `tests/student_pipeline_filled/`
directory of hand-maintained "what a student would produce" notebooks,
run via nbmake. We chose structural parity (`test_student_notebooks`)
instead. The student notebook differs from the solution only in `???`
placeholders; filling in any `???` with the solution-cell code
recovers the solution. The solution notebooks are already covered by
`test_solutions_execute.py`. A separate hand-filled directory would be
a maintenance debt with no additional coverage.

If at any point the student notebook drifts *structurally* from the
solution (different cell count, different non-answer content),
`test_student_notebooks.py::test_student_and_solution_code_cell_counts_align`
catches it.

### Why the e2e test backs up and restores

`test_pipeline_e2e.py` deletes every `day*_output_*.csv` in
`data/checkpoints/` before re-running the notebooks. If the test
fails mid-pipeline, the committed checkpoints would be lost or
corrupted. The fixture backs them up to a pytest tmp directory and
restores from `git checkout` on teardown — so a failed test leaves
the working tree exactly as it started.

### Why `test_solutions_execute.py` shells out

We could, in principle, call the nbclient API directly from Python.
Shelling out to `pytest --nbmake` keeps the invocation identical to
what the GitHub Actions job uses, so a failing CI run reproduces
exactly with `pytest --nbmake solutions/dayN_*.ipynb` locally.

## Sandbox note

Local `pytest --nbmake` spawns a Jupyter kernel subprocess, which
needs a local socket bind. If that's blocked by a sandbox profile,
run the slow suite in a non-sandboxed shell. The fast suite
(`-m "not slow"`) is pure pandas/JSON and has no such dependency.
