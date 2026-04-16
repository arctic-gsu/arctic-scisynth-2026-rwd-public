# Setup

This directory contains everything needed to stand up a fresh working
environment for the RWD track.

## Files

| File | Purpose |
|---|---|
| `environment.yml` | Canonical conda environment definition (Python 3.11, conda-forge). **Edit this file** to add or update dependencies. |
| `environment.lock.yml` | Locked versions generated from `environment.yml`. Regenerate via `conda env export --from-history -n arctic-scisynth-2026-rwd > setup/environment.lock.yml`. |
| `download_data.py` | Fetches raw datasets into `data/raw/`. Idempotent; pass `--force` to re-fetch. |
| `check_setup.py` | Verifies the env is healthy and that `data/processed/` and `data/checkpoints/` are populated. Prints ✅ or specific errors. |
| `colab_bootstrap.py` | Run from the first cell of every notebook. In Colab, clones the repo and `pip install`s deps. No-op locally. |
| `screenshot_html.py` | Playwright helper that snapshots a Folium map HTML file to PNG. Used by Phase 0 / Day 3. |

## First-time local setup

```bash
conda env create -f setup/environment.yml
conda activate arctic-scisynth-2026-rwd
python setup/check_setup.py
```

Expected output ends with a line beginning `✅`.

## First-time Colab setup

Every notebook in `notebooks/` starts with a cell that runs
`setup/colab_bootstrap.py`. In Colab that cell clones the repo into
`/content/arctic-scisynth-2026-rwd`, installs dependencies with pip,
and chdir's into the repo root. Locally, the cell is a no-op (assumes
the conda env is already active).

## Re-fetching datasets

Datasets are committed to `data/raw/` so students do not need network
access for any of them. If you are re-validating before camp or
updating for a new GTFS release:

```bash
python setup/download_data.py --force
```

### Manual step: NTD monthly ridership

`transit.dot.gov` returns **HTTP 403** to automated requests
(CloudFlare WAF). `download_data.py` prints browser instructions for
that file and continues with the other fetchers; you must download the
NTD Excel file by hand.

1. Open <https://www.transit.dot.gov/ntd/data-product/monthly-module-adjusted-data-release>
   in a browser.
2. Download the most recent "Complete Monthly Ridership with
   adjustments and estimates" file (`.xlsx`).
3. Save as `data/raw/ntd_monthly_ridership.xlsx`.
4. Re-run `python setup/download_data.py` to verify it's recognized.

**MARTA's NTD ID is `40022`** (5-digit, not the older "4022" shorthand).

## Known dataset surprises

See `planning/phase0_dryrun/README.md` for the full log. Headline:

- **GTFS `location_type` is all NaN** — use `data/processed/rail_stops.csv`.
- **GWCC/CNN Center has been renamed "SEC District Station"** in the
  current GTFS feed.
- **Stadium capacity for the World Cup is 75,000** (not the 71,000
  MLS/Falcons seated figure).
- **Rail ridership since fall 2023 is undercounted** because of broken
  faregates; NTD data reflects the undercount.

## Re-validation before camp

A late-May GTFS re-validation is planned (target: 2026-05-25) so the
feed reflects MARTA's NextGen Bus Network launch on 2026-04-18. Rail
data is unaffected by NextGen. See `instructor/preflight_checklist.md`.
