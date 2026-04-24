# Tests

Fast pytest suite that keeps the committed student artifacts
self-consistent. Runs on every push.

## What's covered

| File | What it verifies |
|---|---|
| `test_data_integrity.py` | Pre-committed data files exist; `worldcup_reference.csv` has 8 matches in the June 15–July 15 window; `rail_stops.csv` has 38 rows; `day4_output_demand_estimates.csv` is 9 scenarios with 6 surplus / 3 deficit. |
| `test_env_parity.py` | Every package in `setup/colab_bootstrap.py`'s `COLAB_EXTRA_PIP` list is also in `setup/environment.yml`, so the Colab bootstrap doesn't drift from the conda env. |

## Run

```bash
pytest tests/
```

The suite is pure pandas / PyYAML and finishes in well under a
second. If you're running in a locked-down shell that blocks
arbitrary sockets, that's fine — no Jupyter kernel is started.
