# File: ./Deep-Picker-Project/app/backend/services/player_services.py
from schemas import player_schema
from pathlib import Path
import os
import requests
import datetime
import json
from typing import List, Dict
import json
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras.layers import Lambda # Import Lambda layer

def mean_pool(t):
    return tf.reduce_mean(t, axis=1)

def max_pool(t):
    return tf.reduce_max(t, axis=1)

custom_objects = {
    'mean_pool': mean_pool,
    'max_pool': max_pool
}

script_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where services.py is

with open(os.path.join(script_dir, '..', '..', 'model', 'x_scaler.pkl'), 'rb') as f:
    x_scaler = pickle.load(f)

with open(os.path.join(script_dir, '..', '..', 'model', 'y_scaler.pkl'), 'rb') as f:
    y_scaler = pickle.load(f)

# load the model
model_path = os.path.join(script_dir, '..', '..', 'model', 'nba_team_predictor_model.h5')
nba_team_predictor_model = load_model(model_path, custom_objects=custom_objects)

unwanted_stats = ["id", "playerName", "team", "season", "playerId", "gamesStarted", "image"]
per_minute_stats = [
    "points", "assists", "steals", "blocks", "turnovers", "personalFouls",
    "offensiveRb", "defensiveRb", "totalRb", "fieldGoals", "fieldAttempts",
    "threeFg", "threeAttempts", "twoFg", "twoAttempts", "ft", "ftAttempts"
]

def remove_unwanted_stats(df, stats_to_remove):
    """Removes unwanted statistic columns from the DataFrame."""
    return df.drop(columns=stats_to_remove, errors="ignore")

def normalize_columns(df, cols, divisor_col):
    """Normalizes specified columns by dividing them by a divisor column."""
    df = df.copy()
    for col in cols:
        if col in df.columns and divisor_col in df.columns:
            df[col] = df.apply(lambda row: row[col] / row[divisor_col] if row[divisor_col] != 0 else 0, axis=1)
    return df

def one_hot_encode_positions(df, position_col="position"):
    """
    Converts the player position column into one-hot encoded columns,
    ensuring consistent output for the 5 standard basketball positions.

    :param df: Player statistics DataFrame.
    :param position_col: Name of the column containing player positions.
    :return: DataFrame with one-hot encoded position columns.
    """
    if position_col in df.columns:
        standard_positions = ["PG", "SG", "SF", "PF", "C"]

        # Initialize zero columns
        for pos in standard_positions:
            df[f"{position_col}_{pos}"] = 0

        # Iterate through rows to set appropriate columns to 1
        for idx, value in df[position_col].dropna().items():
            # Normalize and split multi-position strings
            positions = [p.strip().upper() for p in value.replace("/", "-").split("-")]
            for pos in positions:
                col_name = f"{position_col}_{pos}"
                if col_name in df.columns:
                    df.at[idx, col_name] = 1

        # Drop the original column
        df = df.drop(columns=[position_col])

    return df

def preprocess_player_list(player_list, stats_to_remove=unwanted_stats, per_minute_stats=per_minute_stats,
                                minutes_col="minutesPg", position_col="position"):
    """End-to-end pipeline to preprocess player list entry."""
    df = pd.DataFrame(player_list)
    df = remove_unwanted_stats(df, stats_to_remove)
    df = normalize_columns(df, per_minute_stats, minutes_col)
    df = one_hot_encode_positions(df, position_col)
    X = df.to_numpy()
    X = x_scaler.transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
    X = X[np.newaxis, :, :] # Add batch dimension

    return X

def get_all_players():
    """
    Get all players from the constant data.
    
    Returns:
        List of all players
    """
    return PLAYERS_DATA


# Module-level cache
_players_cache: List[dict] = []
_last_fetch_year: int = None
_headshots_cache: dict = {}

def _normalize_name(name: str) -> str:
    """Normalize a player name by removing special characters and converting to ASCII."""
    # First, handle Jr./Sr. suffixes with and without commas
    name = name.replace(" Jr.", ", Jr.").replace(" Sr.", ", Sr.")
    name = name.replace("CJ", "C.J.")

    # Replace common special characters with their ASCII equivalents
    replacements = {
        'ć': 'c', 'č': 'c', 'š': 's', 'ž': 'z',
        'Ć': 'C', 'Č': 'C', 'Š': 'S', 'Ž': 'Z',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O',
        'ä': 'a', 'Ä': 'A',
        'ë': 'e', 'Ë': 'E',
        'ï': 'i', 'Ï': 'I',
        'ÿ': 'y', 'Ÿ': 'Y',
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
        'ß': 'ss'
    }
    
    normalized = name
    for special, ascii_char in replacements.items():
        normalized = normalized.replace(special, ascii_char)
    
    return normalized

def _load_headshots() -> dict:
    """
    Loads the player headshots mapping from the JSON file.
    """
    global _headshots_cache
    if not _headshots_cache:
        headshots_path = Path(__file__).parent.parent / "config" / "player_headshots.json"
        try:
            with open(headshots_path, 'r') as f:
                _headshots_cache = json.load(f)
            print(f"[player_services] Loaded {len(_headshots_cache)} player headshots")
        except Exception as e:
            print(f"[player_services] Failed to load headshots ({e})")
            _headshots_cache = {}
    return _headshots_cache

def _fetch_players() -> List[dict]:
    """
    Fetches the full current-season roster from the NBA API once per process (or on year rollover).
    """
    global _players_cache, _last_fetch_year

    # Use the calendar year as the "season"
    season = datetime.datetime.now().year

    # Re-fetch if first time or season changed
    if _last_fetch_year != season or not _players_cache:
        url = (
            f"http://rest.nbaapi.com/api/PlayerDataTotals/"
            f"query?season={season}&sortBy=PlayerName&pageSize=1000"
        )
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            raw_players = resp.json()
            print(f"[player_services] Fetched {len(raw_players)} players from NBA API")
        except Exception as e:
            print(f"[player_services] API fetch failed ({e})")
            raise e

        # Load headshots mapping
        headshots = _load_headshots()

        # Normalize to your schema shape
        _players_cache = [
        {
            "id":            p["id"],
            "playerName":    p["playerName"],
            "team":          p.get("team", ""),
            "position":      p.get("position", ""),
            "age":           p.get("age"),

            # box-score stats
            "games":         p.get("games"),
            "gamesStarted":  p.get("gamesStarted"),
            "minutesPg":     p.get("minutesPg"),

            "fieldGoals":    p.get("fieldGoals"),
            "fieldAttempts": p.get("fieldAttempts"),
            "fieldPercent":  p.get("fieldPercent", 0.0),

            "threeFg":       p.get("threeFg"),
            "threeAttempts": p.get("threeAttempts"),
            "threePercent":  p.get("threePercent", 0.0),

            "twoFg":         p.get("twoFg"),
            "twoAttempts":   p.get("twoAttempts"),
            "twoPercent":    p.get("twoPercent", 0.0),

            "effectFgPercent": p.get("effectFgPercent", 0.0),

            "ft":            p.get("ft"),
            "ftAttempts":    p.get("ftAttempts"),
            "ftPercent":     p.get("ftPercent", 0.0),

            "offensiveRb":   p.get("offensiveRb"),
            "defensiveRb":   p.get("defensiveRb"),
            "totalRb":       p.get("totalRb"),

            "assists":       p.get("assists"),
            "steals":        p.get("steals"),
            "blocks":        p.get("blocks"),
            "turnovers":     p.get("turnovers"),
            "personalFouls": p.get("personalFouls"),
            "points":        p.get("points"),

            # season info 
            "season":        p.get("season"),
            "playerId":      p.get("playerId", ""),

            # headshot URL - use normalized name for lookup
            "image":         headshots.get(_normalize_name(p["playerName"]), ""),
        }
            for p in raw_players
        ]

        # Remove duplicates based on player ID
        seen_ids = set()
        unique_players = []
        for player in _players_cache:
            if player["id"] not in seen_ids:
                seen_ids.add(player["id"])
                unique_players.append(player)
        
        _players_cache = unique_players
        print(f"[player_services] Cached {len(_players_cache)} unique players in memory")
        _last_fetch_year = season

    return _players_cache


# Public service functions
def get_all_players() -> List[dict]:
    """
    Returns the full cached roster for the current season.
    """
    return _fetch_players()


def search_players(prefix: str, limit: int = 100) -> List[player_schema.PlayerSuggestion]:
    """
    Search players by name prefix against the in-memory cache.
    Returns unique players (no duplicates) based on player ID and player name.
    """
    if not prefix:
        return []

    prefix_lower = prefix.lower()
    matches: List[player_schema.PlayerSuggestion] = []
    seen_ids = set()  # Track seen player IDs to avoid duplicates
    seen_names = set()  # Track seen player names to avoid duplicates

    for p in _fetch_players():
        if prefix_lower in p["playerName"].lower():
            # Only add if we haven't seen this player ID or name before
            if p["id"] not in seen_ids and p["playerName"] not in seen_names:
                seen_ids.add(p["id"])
                seen_names.add(p["playerName"])
                matches.append(
                    player_schema.PlayerSuggestion(
                        id=p["id"],
                        playerName=p["playerName"],
                        image=p["image"],
                        position=p["position"]
                    )
                )
                if len(matches) >= limit:
                    break

    print(f"[player_services] Search returned {len(matches)} unique players for prefix '{prefix}'")
    return matches

def predict_score(player_ids: List[int]) -> int:
    """
    Generate a prediction score based on player IDs.
    This is a dummy implementation that returns a fixed value.
    
    Args:
        player_ids: List of player IDs to use for prediction
        
    Returns:
        Predicted score as an integer
    """
    if len(player_ids) != 8:
        raise ValueError("Exactly 8 player IDs are required for prediction")

    # Check for duplicate player IDs
    if len(set(player_ids)) != len(player_ids):
        raise ValueError("All player IDs must be different from each other")

    # Create a set of existing player IDs
    players = get_all_players()
    existing_player_ids = set(p["id"] for p in players)

    # Check if all player IDs exist
    for pid in player_ids:
        if pid not in existing_player_ids:
            raise ValueError(f"Player ID {pid} does not exist in the data")

    # Create a new JSON variable with only the selected players
    team_data = [
            player for player in players
            if player["id"] in player_ids
    ]

    scaled_prediction = nba_team_predictor_model.predict(preprocess_player_list(team_data))
    
    prediction = y_scaler.inverse_transform(scaled_prediction)
    
    
    performance_labels = [
    "Points", "Assists", "Rebounds", "Blocks", "Steals",
    "Win %", "Conf Rank", "FGM", "FGA", "3PM", "3PA",
    "FTM", "FTA", "OREB", "DREB", "Fouls", "Turnovers"
    ]
    

    adjusted_scaled_prediction = scaled_prediction.copy()


    win_pct = adjusted_scaled_prediction[0, 5] * 1.2
    print(adjusted_scaled_prediction[0, 5])
    print("Win %:", win_pct)

    # chemistry score is based on the win percentage
    team_strength_percentage = win_pct * 100





    # Round and clip chemistry score between 0 and 100
    chemistry_score = int(round(team_strength_percentage))
    chemistry_score = max(0, min(100, chemistry_score))

    predicted_stats = {}

    for j, label in enumerate(performance_labels):
        predicted = float(prediction[0, j])
        if label == "Win %":
            predicted_stats[label] = round(predicted, 3)
        elif label == "Conf Rank":
            predicted_stats[label] = int(round(predicted))
            print(round(predicted))
            print(predicted)
        else:
            predicted_stats[label] = round(predicted, 1)
    
    # i want to create from 3PA and 3PM the 3P% and from FTA and FTM the FT% amd from FGA and FGM the FG%
    if "3PA" in predicted_stats and "3PM" in predicted_stats:
        three_percent = (predicted_stats["3PM"] / predicted_stats["3PA"]) * 100 if predicted_stats["3PA"] > 0 else 0
        predicted_stats["3P%"] = round(three_percent, 1)
    if "FTA" in predicted_stats and "FTM" in predicted_stats:
        ft_percent = (predicted_stats["FTM"] / predicted_stats["FTA"]) * 100 if predicted_stats["FTA"] > 0 else 0
        predicted_stats["FT%"] = round(ft_percent, 1)
    if "FGA" in predicted_stats and "FGM" in predicted_stats:
        fg_percent = (predicted_stats["FGM"] / predicted_stats["FGA"]) * 100 if predicted_stats["FGA"] > 0 else 0
        predicted_stats["FG%"] = round(fg_percent, 1)
    
    # but i want each of them to be after the original stats, i want the % stats to be after the A and M stats
    ordered_stats = {}
    for label in performance_labels:
        if label in predicted_stats:
            ordered_stats[label] = predicted_stats[label]
        if label == "3PA":
            ordered_stats["3P%"] = predicted_stats["3P%"]
        if label == "FTA":
            ordered_stats["FT%"] = predicted_stats["FT%"]
        if label == "FGA":
            ordered_stats["FG%"] = predicted_stats["FG%"]
    predicted_stats = ordered_stats


    predicted_stats["Chemistry Score"] = chemistry_score
    print(f"Predicted Stats: {predicted_stats}")

    return predicted_stats

def get_all_teams() -> List[str]:
    """
    Get all unique team names from the current players data.
    Filters out invalid team codes like 2TM and 3TM.
    
    Returns:
        List of team names
    """
    players = _fetch_players()
    # Filter out invalid team codes and get unique teams
    teams = list(set(player["team"] for player in players 
                    if player["team"] and not player["team"].endswith("TM")))
    return sorted(teams)


def get_top_8_players_by_team(team_name: str) -> List[dict]:
    """
    Get the top 8 players for a specific team based on minutes played (minutesPg).
    
    Args:
        team_name: Name of the team
        
    Returns:
        List of top 8 players for the team, sorted by minutes played (descending)
    """
    players = _fetch_players()
    
    # Filter players by team
    team_players = [player for player in players if player["team"] == team_name]
    
    # Sort by minutes played (descending) and take top 8
    team_players.sort(key=lambda x: x["minutesPg"] or 0, reverse=True)
    top_8_players = team_players[:8]
    
    return top_8_players


def get_all_teams_with_top_8_players() -> Dict[str, List[dict]]:
    """
    Get all teams with their top 8 players based on minutes played.
    
    Returns:
        Dictionary where keys are team names and values are lists of top 8 players
    """
    teams = get_all_teams()
    teams_with_players = {}
    
    for team in teams:
        teams_with_players[team] = get_top_8_players_by_team(team)
    
    return teams_with_players
