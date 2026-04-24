# ARCTIC SciSynth 2026 — Real-World Data Analysis Track

Notebook-based curriculum for the Real-World Data Analysis (RWD) track of
the ARCTIC SciSynth 2026 summer camp at Georgia State University
(**June 8–12, 2026**). Students spend the week assessing whether
Atlanta's MARTA rail system can handle the demand surge from the 2026
FIFA World Cup, with a "Transit Readiness Briefing" as the final
deliverable.

## The question

Mercedes-Benz Stadium hosts **8 FIFA World Cup matches between June 15
and July 15, 2026** (including a semifinal). Capacity in the World Cup
configuration is **75,000**. The camp runs the week before the first
match. **Can MARTA rail handle it?**

Students answer that question with real data: the MARTA GTFS feed, FTA
NTD monthly ridership, and Census ACS commute data — anchored against
the 155,000-rider Super Bowl LIII benchmark and a published Georgia
Tech post-game ridership regression.

## Who this is for

Undergraduates with minimal technical background. Python basics,
Pandas, and data visualization are taught in shared morning sessions;
this track's afternoon notebooks build on those. Instructor materials
(solutions, teaching guides) are maintained separately.

## Week at a glance

| Day | Afternoon focus | Deliverable |
|---|---|---|
| Mon | GTFS exploration | MARTA system summary |
| Tue | NTD cleaning + ridership trends + station frequencies | Trend chart + stadium-adjacent stations |
| Wed | Guided EDA + Folium mapping with venue overlay | Interactive map |
| Thu | Census enrichment + demand-vs-capacity modeling | 3×3 scenario grid |
| Fri | Briefing + presentations | Transit Readiness Briefing |

Full learning objectives and timing: [`SCHEDULE.md`](SCHEDULE.md).

## Notebooks

The Colab badges open each notebook directly in a cloud Jupyter
session. The first cell in every notebook handles repo clone +
dependency install automatically.

| Day | Student notebook |
|---|---|
| 1 (welcome) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day1_00_welcome_setup.ipynb) [`day1_00_welcome_setup.ipynb`](notebooks/day1_00_welcome_setup.ipynb) |
| 1 (project) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day1_explore_marta.ipynb) [`day1_explore_marta.ipynb`](notebooks/day1_explore_marta.ipynb) |
| 2 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day2_cleaning_ridership.ipynb) [`day2_cleaning_ridership.ipynb`](notebooks/day2_cleaning_ridership.ipynb) |
| 3 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day3_eda_and_mapping.ipynb) [`day3_eda_and_mapping.ipynb`](notebooks/day3_eda_and_mapping.ipynb) |
| 4 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day4_demand_estimation.ipynb) [`day4_demand_estimation.ipynb`](notebooks/day4_demand_estimation.ipynb) |
| 5 | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/arctic-gsu/arctic-scisynth-2026-rwd-public/blob/main/notebooks/day5_briefing_template.ipynb) [`day5_briefing_template.ipynb`](notebooks/day5_briefing_template.ipynb) |

## Quickstart (local, conda)

```bash
# Clone
git clone https://github.com/arctic-gsu/arctic-scisynth-2026-rwd-public.git
cd arctic-scisynth-2026-rwd-public

# Create + activate environment
conda env create -f setup/environment.yml
conda activate arctic-scisynth-2026-rwd

# Verify setup
python setup/check_setup.py

# Datasets are committed in data/raw/. To re-fetch:
python setup/download_data.py
```

## Quickstart (Colab)

Open notebooks via the badges in the table above, **not** via Colab's
"File → Open notebook → GitHub" browser. That picker calls
`api.github.com` via OAuth, which the `arctic-gsu` org blocks for
third-party apps; badges open notebooks via a direct URL and work
fine.

1. Click any Open-in-Colab badge.
2. The first code cell runs `setup/colab_bootstrap.py`, which clones
   this repo into `/content/arctic-scisynth-2026-rwd-public`, installs
   dependencies, and chdir's into the repo root. Running it is
   idempotent.
3. Proceed through the notebook normally.

## Repository layout

```
arctic-scisynth-2026-rwd-public/
├── README.md                 # You are here
├── SCHEDULE.md               # Day-by-day learning objectives + timing
├── LICENSE                   # CC-BY 4.0 (content) + MIT (code)
├── setup/                    # Environment, data download, bootstrap
├── data/
│   ├── raw/                  # Downloaded datasets (committed, ~32 MB)
│   ├── processed/            # Instructor-prepped files
│   └── checkpoints/          # Per-day outputs (safety net)
├── notebooks/                # Student-facing notebooks
└── tests/                    # pytest test suite
```

## License

Dual license: **CC-BY 4.0** for content (notebooks, markdown,
curriculum), **MIT** for code. See [`LICENSE`](LICENSE).

## Credits

Designed by Andalib Samandari for the ARCTIC program at Georgia State
University. Curriculum patterns draw on Data Carpentry, Software
Carpentry, and Microsoft's Data Science for Beginners (all
CC-licensed). Transit-planning benchmarks: Santanam et al. 2021
(arXiv:2106.05359) and MARTA operational reports.
