import numpy as np

def logistic(x):
    return 1 / (1 + np.exp(-x))

def game_prob(row, w):
    # Build linear terms for away and home (lower ERA/bullpen ERA is better; higher K%/OPS better)
    a = (
        -w['era']*row['away_sp_era']
        + w['k']*row['away_sp_kpct']
        + w['ops']*row['away_team_ops']
        + w['l10']*row['away_last10_ops']
        - w['pen']*row['away_bullpen_era']
    )
    h = (
        -w['era']*row['home_sp_era']
        + w['k']*row['home_sp_kpct']
        + w['ops']*row['home_team_ops']
        + w['l10']*row['home_last10_ops']
        - w['pen']*row['home_bullpen_era']
    )
    diff = h - a
    diff += (row.get('park_factor_runs', 1.0) - 1.0) * w['park_bias']  # small park effect
    p_home = logistic(diff * w['scale'])
    return p_home

def volatility_tags(row, thresholds):
    tags = []
    if row.get('away_rookie_sp', 0) == 1 or row.get('home_rookie_sp', 0) == 1:
        tags.append('Rookie SP')
    if row.get('park_factor_runs', 1.0) >= thresholds['park_hi']:
        tags.append('High-Run Park')
    if row.get('ump_confirmed', 0) == 0:
        tags.append('Umpire Unconfirmed')
    if row.get('roof_confirmed', 1) == 0:
        tags.append('Roof Unconfirmed')
    return tags

def core_filter(pick_side, p_home, row, core_rules):
    if pick_side == 'HOME':
        foe_l10 = row['away_last10_ops']
        prob = p_home
    else:
        foe_l10 = row['home_last10_ops']
        prob = 1 - p_home
    return bool(prob >= core_rules['core_min'] and foe_l10 <= core_rules['foe_l10_max'])
