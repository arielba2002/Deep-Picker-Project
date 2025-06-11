# File: ./Deep-Picker-Project/app/backend/services/player_services.py
from config.constants import PLAYERS_DATA
from schemas import player_schema
from typing import List
import json
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf
import pandas as pd
import numpy as np
import os
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

# In services/player_services.py
def search_players(prefix: str, limit: int = 4) -> List[player_schema.PlayerSuggestion]:
    """
    Search players by name prefix.
    
    Args:
        prefix: The prefix to search for
        limit: Maximum number of suggestions to return
        
    Returns:
        List of player suggestions matching the prefix
    """
    if not prefix:
        return []
        
    prefix = prefix.lower()
    matches = []
    
    for player in PLAYERS_DATA:
        if player["playerName"].lower().startswith(prefix):
            matches.append(
                player_schema.PlayerSuggestion(
                    id=player["id"],
                    playerName=player["playerName"],
                    team=player["team"],
                    image=player["image"]  # Add this line
                )
            )
            
            if len(matches) >= limit:
                break
                
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
    existing_player_ids = set(player["id"] for player in PLAYERS_DATA)
    
    # Check if all player IDs exist
    for pid in player_ids:
        if pid not in existing_player_ids:
            raise ValueError(f"Player ID {pid} does not exist in the data")

    # Create a new JSON variable with only the selected players
    team_data = [
            player for player in PLAYERS_DATA 
            if player["id"] in player_ids
    ]

    scaled_prediction = nba_team_predictor_model.predict(preprocess_player_list(team_data))
    
    prediction = y_scaler.inverse_transform(scaled_prediction)
    
    
    performance_labels = [
    "Points", "Assists", "Rebounds", "Blocks", "Steals",
    "Win %", "Conf Rank", "FGM", "FGA", "3PM", "3PA",
    "FTM", "FTA", "OREB", "DREB", "Fouls", "Turnovers"
    ]
    
    negative_labels = ["Conf Rank", "Fouls", "Turnovers"]
    negative_indexes = [i for i, label in enumerate(performance_labels) if label in negative_labels]

    adjusted_scaled_prediction = scaled_prediction.copy()
    for idx in negative_indexes:
        adjusted_scaled_prediction[0, idx] = 1 - adjusted_scaled_prediction[0, idx]

    # Compute chemistry score as a percentage
    team_strength_percentage = adjusted_scaled_prediction.mean() * 100

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
    
    predicted_stats["Chemistry Score"] = chemistry_score
    print(f"Predicted Stats: {predicted_stats}")

    return predicted_stats
