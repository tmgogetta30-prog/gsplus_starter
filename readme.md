# GS+ Starter (No-API) — Beginner Friendly

This tiny Streamlit app lets you paste a slate and simple stats into data/games.csv,
then shows picks with P(win), Volatility, and Notes. No coding or APIs needed.

## Run (Windows/macOS)
1) Install Python 3.11 from https://www.python.org/downloads/
2) Open Terminal / Command Prompt in this folder and run:

   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

   pip install -r requirements.txt
   streamlit run app.py

3) Update data/games.csv in Excel/Sheets and refresh the app.

## What you can edit in data/games.csv
- date, time_et, away, home
- away_sp_name, away_sp_era, away_sp_kpct, away_team_ops, away_last10_ops, away_bullpen_era, away_rookie_sp
- home_sp_name, home_sp_era, home_sp_kpct, home_team_ops, home_last10_ops, home_bullpen_era, home_rookie_sp
- park_factor_runs (1.00 = neutral)
- ump_confirmed (0/1), roof_confirmed (0/1)

Core rule (in app sidebar): P(win) ≥ 0.65 and opponent last-10 OPS ≤ .720.
