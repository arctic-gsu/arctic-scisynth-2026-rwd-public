# Weekly Schedule — RWD Track

ARCTIC SciSynth 2026, **June 8–12, 2026** (Georgia State University).

Each day has a shared-morning block (taught across all three SciSynth
tracks by different instructors) and a RWD-track afternoon project
block of ~2.5–3 hours. This document covers the afternoon block only.
Morning sessions cover Python basics, Pandas, data cleaning, data
visualization, and an intro to ML; see
`planning/proposed_data_analysis_sessions.docx`.

---

## Day 1 (Mon, June 8) — Project intro + GTFS exploration

**Afternoon: 2:00–5:00 PM**

**Learning objectives:**
- Understand the project question: can MARTA handle the World Cup?
- Load and explore a real GTFS feed with pandas.
- Produce a summary of MARTA's rail system size.

**Schedule:**
- 2:00–2:30 Project introduction (World Cup context, Super Bowl LIII
  anchor, the question)
- 2:30–3:30 Download + unzip GTFS, load `stops.txt`, explore structure
- 3:30–4:30 Filter to rail stations (with the `location_type` surprise),
  system summary statistics
- 4:30–5:00 Preview `station_frequencies.csv` for tomorrow

**Checkpoint:** `data/checkpoints/day1_output_stops.csv` — 38 MARTA
rail stations with line assignments.

**Notebooks:**
- `notebooks/day1_00_welcome_setup.ipynb` (standalone ~30 min setup)
- `notebooks/day1_explore_marta.ipynb` (main project work)

---

## Day 2 (Tue, June 9) — Ridership trends + station frequencies

**Afternoon: 2:00–5:00 PM**

**Learning objectives:**
- Level up from the morning cleaning session to the full multi-tab NTD
  Excel workbook.
- Build a ridership-by-mode trend plot and identify the COVID dip and
  fall-2023 faregate anomaly.
- Clean the intentionally-messy `station_frequencies.csv` and identify
  stadium-adjacent stations.

**Schedule:**
- 2:00–2:30 Level-up: load the raw multi-tab NTD Excel
- 2:30–3:30 Time-series ridership trends (rail + bus)
- 3:30–4:00 Data-quality discussion: broken faregates since fall 2023
- 4:00–4:45 Clean station frequencies, merge with Day 1 station list
- 4:45–5:00 Identify the two stadium-adjacent stations (SEC District,
  Vine City) and Five Points as a transfer hub

**Checkpoint:** `data/checkpoints/day2_output_cleaned_ridership.csv`
and `day2_output_station_freq_clean.csv`.

**Notebook:** `notebooks/day2_cleaning_ridership.ipynb`.

---

## Day 3 (Wed, June 10) — EDA + spatial visualization

**Afternoon: 2:00–5:00 PM**

**Learning objectives:**
- Systematic EDA with `.describe`, `.groupby`, `.value_counts`.
- Build an interactive Folium map of MARTA rail stations.
- Overlay World Cup venues and compute straight-line distances.

**Schedule:**
- 2:00–2:45 Guided EDA mini-lesson
- 2:45–3:45 Folium map of all rail stations, color-coded by line
- 3:45–4:30 Venue overlay (Mercedes-Benz Stadium, Centennial Olympic
  Park Fan Fest, hotel clusters) + distance computations
- 4:30–5:00 Size station markers by trains-per-hour frequency

**Checkpoint:** `data/checkpoints/day3_output_eda_summary.csv` +
`marta_map.html`.

**Notebook:** `notebooks/day3_eda_and_mapping.ipynb`.

---

## Day 4 (Thu, June 11) — Census enrichment + demand modeling

**Afternoon: 2:30–5:30 PM**

**Learning objectives:**
- Query the Census ACS API (Tables B08301 + B08141) for Fulton and
  DeKalb county tracts; clean cryptic column codes.
- Build a 3×3 demand-vs-capacity grid (mode share × per-train capacity).
- Cross-check against the Georgia Tech post-game ridership regression.
- Interpret which scenarios show a surplus vs. a deficit.

**Schedule:**
- 2:30–3:30 Census data pull + column cleanup
- 3:30–4:30 Demand estimation (75k × {15, 22, 35}% mode share) vs.
  capacity (24 trains/hr/direction × {232, ~400, 750}/train × 2.5 hr)
- 4:30–5:30 Georgia Tech cross-check + briefing-draft assembly

**Checkpoint:** `data/checkpoints/day4_output_demand_estimates.csv`.

**Notebook:** `notebooks/day4_demand_estimation.ipynb`.

---

## Day 5 (Fri, June 12) — Briefing + presentations

**Schedule:**
- Morning: finalize the Transit Readiness Briefing
- Afternoon: group presentations (5–10 min each), peer feedback,
  cross-group discussion
- Wrap-up: the first match is in 3 days

**Deliverable:** Transit Readiness Briefing. Structure: question → data
→ findings → comparison to SB LIII and GT regression → answer → scope
and limitations → what we'd study next.

**Notebook:** `notebooks/day5_briefing_template.ipynb`.

---

## Cross-day pipeline

Each day's checkpoint feeds the next day's starting state, so a
student with a broken notebook on Day N can load the committed
checkpoint at the top of their Day N+1 notebook and keep going.

```
Day 1  →  day1_output_stops.csv
Day 2  →  day2_output_cleaned_ridership.csv + day2_output_station_freq_clean.csv
Day 3  →  day3_output_eda_summary.csv + marta_map.html
Day 4  →  day4_output_demand_estimates.csv
Day 5  →  Transit Readiness Briefing
```
