# Data dictionary

All files in this tree are committed so the project runs from a clean
clone without network access. `data/raw/` is the input layer;
`data/processed/` is instructor-prepped for student notebooks;
`data/checkpoints/` is the per-day-output safety net that lets any
notebook start independently.

Dataset quirks are noted inline below.

---

## `data/raw/`

Source downloads. Not modified after download. `setup/download_data.py`
is idempotent; pass `--force` to re-fetch.

### `marta_gtfs.zip`

- **Source:** <https://itsmarta.com/google_transit.zip> (listed on
  <https://itsmarta.com/app-developer-resources.aspx>)
- **License:** MARTA open-data policy (GTFS is publicly redistributable)
- **Format:** ZIP archive of CSV-like `.txt` files (GTFS Static)
- **Size:** ~18 MB
- **Update frequency:** ~4× per year with MARTA service changes
- **Key files inside:** `stops.txt`, `stop_times.txt`, `trips.txt`,
  `routes.txt`, `calendar.txt`
- **Quirks:**
  - **No `feed_info.txt`** — use `calendar.txt` for effective dates.
  - **`location_type` is all NaN** in `stops.txt`. Filtering by
    `location_type == 1` returns zero rows; use
    `data/processed/rail_stops.csv` instead.
  - **Station rename:** "GWCC/CNN Center" → "SEC District Station" in
    the current feed (closest station to Mercedes-Benz Stadium).
  - **"MIDTOWN&nbsp;&nbsp;STATION"** appears with a double space.
  - The current feed (as of Phase 0) is **pre-NextGen** and effective
    through 2026-04-17. Rail is unaffected by NextGen; bus routes are
    pre-redesign. Re-validate in late May.

### `ntd_monthly_ridership.xlsx`

- **Source:** <https://www.transit.dot.gov/ntd/data-product/monthly-module-adjusted-data-release>
- **License:** U.S. government public domain
- **Format:** Excel workbook (multiple sheets: UPT, VRM, VRH, VOMS, Read
  Me, Master, UPT Estimates, VRM Estimates, Calendar Year UPT, Calendar
  Year VRM, Mozart Reports)
- **Size:** ~14 MB
- **Coverage:** Monthly data, 2002–present, for all US transit agencies.
- **MARTA's NTD ID:** `40022` (5-digit; older planning prose used the
  incorrect "4022" shorthand).
- **Quirks:**
  - **Manual download required.** `transit.dot.gov` returns HTTP 403 to
    automated requests (CloudFlare WAF). `setup/download_data.py` prints
    browser instructions for this file.
  - **No preamble rows** in the current release — header is row 0. FTA
    reformats between releases; if future downloads have preamble rows,
    adjust `skiprows` with an explicit comment.
  - **Rail ridership since fall 2023 is unreliable** — MARTA has
    publicly acknowledged that broken faregates undercount Breeze-card
    taps. The NTD data reflects this undercount.
  - **Jan 2026 jump (+49.6%)** in rail UPT appears to be an FTA
    adjustment-methodology catch-up; worth flagging in Day 2 discussion
    but not a separate discontinuity.

### `acs_b08301_fulton_dekalb.csv` and `acs_b08141_fulton_dekalb.csv`

- **Source:** <https://api.census.gov/data/2024/acs/acs5> (2020–2024
  5-year estimates)
- **License:** U.S. government public domain
- **Tables:**
  - B08301 — Means of transportation to work
  - B08141 — Workers by vehicles available (counts workers, not
    households — a common misreading)
- **Geography:** Census tract level; Fulton (FIPS 121) + DeKalb (FIPS
  089), Georgia (FIPS 13). 530 tracts total.
- **Key variables:** `B08301_010E` (transit commuters),
  `B08301_003E` (drove-alone), `B08141_002E` (workers in zero-vehicle
  households).
- **Quirks:** Variable codes are cryptic; students rename them in Day 4
  as a cleaning exercise.

---

## `data/processed/`

Instructor-prepped files built by Phase 0. Student notebooks load from
here.

### `rail_stops.csv`

38 MARTA rail stations with `stop_id`, `stop_name`, `stop_lat`,
`stop_lon`, `line`. Built by joining `stop_times` → `trips` → `routes`
on `route_type == 1`. The Day 1 fallback because GTFS `location_type`
can't be used.

### `station_frequencies.csv`

Station-level trains-per-hour summary, **intentionally messy** for
Day 2 cleaning practice: inconsistent capitalization in `station_name`,
a handful of null `trains_per_hour` values, and 1–2 duplicate rows.
Columns: `station_name`, `line`, `stop_lat`, `stop_lon`,
`peak_trains_per_hour`.

### `ntd_marta_clean.csv`

Fully cleaned monthly MARTA ridership (2002–present) by mode. Used as
the visualization-session fallback. Columns: `date`, `mode_code`,
`mode_name`, `upt`.

### `ntd_marta_for_cleaning_session.csv`

**Intentionally messy** version of MARTA ridership for the Day 2
shared morning cleaning session: missing values, cryptic column names,
mixed types. Same underlying numbers as `ntd_marta_clean.csv`.

### `worldcup_reference.csv`

Hand-built from atlantafwc26.com, Mercedes-Benz Stadium press release,
and FIFA 2026 draw materials. 8 matches + venue coordinates + hotel
cluster centroids. Columns: `match_num`, `date`, `kickoff_et`,
`teams`, `round`, `venue`, `lat`, `lon`, `category`. `LAST_VERIFIED`
constant in `setup/download_data.py` tracks staleness.

---

## `data/checkpoints/`

Per-day outputs produced by student notebooks. Also committed from
Phase 0 so a student who misses Day N can still start Day N+1 from a
known-good state.

| File | Produced by | Consumed by |
|---|---|---|
| `day1_output_stops.csv` | Day 1 §3 | Day 2 §3 |
| `day2_output_cleaned_ridership.csv` | Day 2 §1 | Day 3 §1 |
| `day2_output_station_freq_clean.csv` | Day 2 §3 | Day 3 §2–3 |
| `day3_output_eda_summary.csv` | Day 3 §3 | Day 4 briefing |
| `marta_map.html` | Day 3 §3 | Viewed in the briefing |
| `day4_output_demand_estimates.csv` | Day 4 §2 | Day 5 briefing |
| `*.png` | Various | Day 5 briefing |

Student notebooks open with a "🔄 Recovery point" cell that loads from
these files — so even a student whose kernel state went sideways can
pick up from the last known-good checkpoint.

---

## Licensing of derived files

Files in `data/processed/` and `data/checkpoints/` are derived from
public-domain federal data (NTD, Census) and MARTA's openly
redistributable GTFS feed. They are redistributed under the
repository's **CC-BY 4.0** content license; attribution = this
repository.
