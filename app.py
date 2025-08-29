import streamlit as st
import pandas as pd
import numpy as np
from utils import game_prob, volatility_tags, core_filter

st.set_page_config(page_title="GS+ Starter", layout="wide")
st.title("GS+ Starter — Split Panel Picks (Beginner Friendly)")

with st.sidebar:
    st.header("Settings")
    stats_refreshed = st.text_input("Stats refreshed through (date)", value="Aug 27, 2025")

    st.markdown("### Weights (v2.1-style inside v3.2 guardrails)")
    era = st.number_input("Weight: SP ERA (negative)", value=0.9, min_value=0.0, step=0.1)
    k = st.number_input("Weight: SP K% (positive)", value=1.5, min_value=0.0, step=0.1)
    ops = st.number_input("Weight: Team OPS (positive)", value=1.2, min_value=0.0, step=0.1)
    l10 = st.number_input("Weight: Last-10 OPS (positive)", value=1.0, min_value=0.0, step=0.1)
    pen = st.number_input("Weight: Bullpen ERA (negative)", value=0.5, min_value=0.0, step=0.1)
    scale = st.number_input("Logistic scale", value=4.0, min_value=0.5, step=0.5)
    park_bias = st.number_input("Park bias (small)", value=0.25, min_value=0.0, step=0.05)

    st.markdown("### Volatility thresholds")
    park_hi = st.number_input("High-Run Park if park_factor_runs ≥", value=1.10, min_value=1.0, step=0.01)

    st.markdown("### Core Rules")
    core_min = st.number_input("Core min P(win)", value=0.65, min_value=0.5, max_value=0.9, step=0.01)
    foe_l10_max = st.number_input("Opponent max L10 OPS", value=0.720, min_value=0.600, max_value=0.900, step=0.005)

    st.markdown("---")
    st.markdown("Edit `data/games.csv` and refresh the app.")

weights = dict(era=era, k=k, ops=ops, l10=l10, pen=pen, scale=scale, park_bias=park_bias)
thresholds = dict(park_hi=park_hi)
core_rules = dict(core_min=core_min, foe_l10_max=foe_l10_max)

st.subheader(f"Stats refreshed through: {stats_refreshed}")

# Load data
path = "data/games.csv"
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.error("Missing data/games.csv. Create it from the sample below.")
    st.stop()

# Ensure numeric types
num_cols = [
    'away_sp_era','away_sp_kpct','away_team_ops','away_last10_ops','away_bullpen_era','away_rookie_sp',
    'home_sp_era','home_sp_kpct','home_team_ops','home_last10_ops','home_bullpen_era','home_rookie_sp',
    'park_factor_runs','ump_confirmed','roof_confirmed'
]
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0.0)

rows = []
for _, r in df.iterrows():
    p_home = game_prob(r, weights)
    pick_side = 'HOME' if p_home >= 0.5 else 'AWAY'
    pick_team = r['home'] if pick_side == 'HOME' else r['away']
    vol_tags = volatility_tags(r, thresholds)
    vol = 'High' if ('Rookie SP' in vol_tags or 'High-Run Park' in vol_tags) else ('Med' if vol_tags else 'Low')
    is_core = core_filter(pick_side, p_home, r, core_rules)
    rows.append({
        "Time (ET)": r.get("time_et",""),
        "Matchup": f"{r['away']} @ {r['home']}",
        "Starters": f"{r['away_sp_name']} vs {r['home_sp_name']}",
        "Pick": pick_team,
        "P(win)": round(p_home if pick_side=='HOME' else (1 - p_home), 3),
        "Vol": vol,
        "Core": "✅" if is_core else "",
        "Notes": ", ".join(vol_tags) if vol_tags else "—"
    })

out = pd.DataFrame(rows)
st.dataframe(out, use_container_width=True)

st.markdown("### Core Safe Plays")
core_df = out[out["Core"]=="✅"][["Time (ET)","Matchup","Pick","P(win)","Vol","Notes"]]
st.dataframe(core_df, use_container_width=True) if not core_df.empty else st.write("No Core picks under current thresholds.")

st.caption("Starter app: simple scoring & guardrails. Swap CSV with real data later.")
