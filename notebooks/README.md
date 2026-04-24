# Student notebooks

Six notebooks that run the week. Open them in order.

| File | Estimated time | What you'll build |
|---|---|---|
| `day1_00_welcome_setup.ipynb` | ~30 min | Environment check + your first CSV load |
| `day1_explore_marta.ipynb` | ~2.5 hrs | Load MARTA's GTFS feed; filter to rail; save Day 1 checkpoint |
| `day2_cleaning_ridership.ipynb` | ~3 hrs | Clean the raw NTD Excel; plot ridership trends; clean a messy station file |
| `day3_eda_and_mapping.ipynb` | ~3 hrs | EDA with the three pandas summary verbs; build a Folium map; measure venue distances |
| `day4_demand_estimation.ipynb` | ~3 hrs | Census commute data; 3×3 demand-vs-capacity grid; Georgia Tech regression cross-check |
| `day5_briefing_template.ipynb` | ~2.5 hrs | Write your 400–600 word Transit Readiness Briefing |

## How the week flows

Every day's notebook starts by loading **checkpoint files** from
`data/checkpoints/`. Those files are produced by the previous day's
notebook *and* committed in git. This means:

- If you don't finish Day 2 in time, **Day 3 still works** — it loads
  the committed `day2_output_*.csv` files.
- If your kernel gets into a bad state mid-notebook, run the next
  **🔄 Recovery point** cell. It reloads clean state from checkpoints.

## Exercise markers

- 🎯 **Your Turn!** — fill in the `???` placeholder yourself.
- ✅ **Checkpoint** — a small assertion confirms you got the right
  answer. If it fails, fix your code before moving on.
- 💡 **Click for solution** — hidden by default; reveal if you're
  stuck after honest effort.
- 🔄 **Recovery point** — jump forward cleanly if you're lost.
- ⚡ **Skip if behind** — an instructor signal that this cell is
  cut-able under time pressure.
- 🟢 🔵 ⬛ — difficulty tiers on Day 4 only. Everyone does 🟢 + 🔵;
  ⬛ is for students with extra time.

## How to work through a notebook

1. **Run the setup cell first** (the one with the long import block).
   In Colab this clones the repo and pip-installs; locally it's a
   no-op if you've already activated the conda env.
2. **Read the markdown blocks** before running the next code cell.
   The notebooks explain *why* each step matters, not just *what*
   it does.
3. **Try the 🎯 exercises yourself.** The 💡 solution is right there,
   but looking at it before you've tried is wasted time — you don't
   learn by reading code, you learn by writing it.
4. **If a checkpoint fails**, read the assertion message carefully.
   Most often it tells you exactly what's wrong.
5. **If you get stuck**, raise your hand — most failures have a
   documented cause and fix.

## If you run into trouble

- **In Colab:** restart runtime → Runtime → Restart runtime → re-run
  every cell from the top.
- **Locally:** Kernel → Restart & Run All.
- **Still stuck:** Jump to the next 🔄 Recovery point cell; it loads
  from a committed checkpoint so you can continue.

