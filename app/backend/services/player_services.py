# File: ./Deep-Picker-Project/app/backend/services/player_services.py
from config.constants import PLAYERS_DATA
from schemas import player_schema
from typing import List

def get_all_players():
    """
    Get all players from the constant data.
    
    Returns:
        List of all players
    """
    return PLAYERS_DATA["players"]

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
    
    for player in PLAYERS_DATA["players"]:
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






# model functions:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Input, Dense, Dropout, TimeDistributed, GlobalAveragePooling1D, BatchNormalization, LSTM, Bidirectional, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from matplotlib.colors import Normalize
#  some constants
unwanted_stats = ["id", "playerName", "team", "season", "playerId", "gamesStarted", "image"]
per_game_stats = [
    "points", "assists", "steals", "blocks", "turnovers", "personalFouls",
    "offensiveRb", "defensiveRb", "totalRb", "fieldGoals", "fieldAttempts",
    "threeFg", "threeAttempts", "twoFg", "twoAttempts", "ft", "ftAttempts"
]
per_minute_stats = per_game_stats

def preprocess_team_season_data(team_season_data, team_key, stats_to_remove, per_game_stats, per_minute_stats,
                               games_col="games", minutes_col="minutesPg", position_col="position",
                               feature_scaler=None, label_scaler=None):
    """End-to-end pipeline to preprocess a single team_season."""
    df, labels = create_players_df(team_season_data, team_key)
    df = remove_unwanted_stats(df, stats_to_remove)
    df = normalize_columns(df, per_game_stats, games_col)
    df = normalize_columns(df, per_minute_stats, minutes_col)
    df = add_derived_features(df)  # Add derived features
    df = one_hot_encode_positions(df, position_col)
    df = sort_players_by_importance(df)  # Sort players by importance
    df, feature_scaler_used = scale_df(df, feature_scaler)
    X, Y, label_scaler_used = prepare_team_input_and_labels(df, labels, label_scaler)

    return X, Y, feature_scaler_used, label_scaler_used

def create_players_df(team_data, team_key):
    """Creates a DataFrame from team data."""
    labels = team_data.get("labels", [])
    player_list = team_data.get("players", [])
    df = pd.DataFrame(player_list)

    # Extract team and season information
    team_name, season = team_key.split("_")
    df["team"] = team_name
    df["season"] = int(season)

    return df, labels

def remove_unwanted_stats(df, stats_to_remove):
    """Removes unwanted statistic columns."""
    return df.drop(columns=stats_to_remove, errors="ignore")

def normalize_columns(df, cols, divisor_col):
    """Normalizes columns by dividing by a divisor column."""
    df = df.copy()
    for col in cols:
        if col in df.columns and divisor_col in df.columns:
            df[col] = df.apply(lambda row: row[col] / row[divisor_col] if row[divisor_col] != 0 else 0, axis=1)
    return df

def add_derived_features(df):
    """Add derived features that might help the model discriminate between teams better."""
    # Shooting percentages
    if all(col in df.columns for col in ["fieldGoals", "fieldAttempts"]):
        df["fg_percentage"] = df.apply(lambda row: row["fieldGoals"] / row["fieldAttempts"] if row["fieldAttempts"] > 0 else 0, axis=1)

    if all(col in df.columns for col in ["threeFg", "threeAttempts"]):
        df["three_percentage"] = df.apply(lambda row: row["threeFg"] / row["threeAttempts"] if row["threeAttempts"] > 0 else 0, axis=1)

    if all(col in df.columns for col in ["ft", "ftAttempts"]):
        df["ft_percentage"] = df.apply(lambda row: row["ft"] / row["ftAttempts"] if row["ftAttempts"] > 0 else 0, axis=1)

    # Efficiency metrics
    if all(col in df.columns for col in ["points", "fieldAttempts"]):
        df["points_per_attempt"] = df.apply(lambda row: row["points"] / row["fieldAttempts"] if row["fieldAttempts"] > 0 else 0, axis=1)

    if all(col in df.columns for col in ["points", "minutes"]):
        df["points_per_minute"] = df.apply(lambda row: row["points"] / row["minutes"] if row["minutes"] > 0 else 0, axis=1)

    # Player importance metrics
    if all(col in df.columns for col in ["minutes", "games"]):
        df["minutes_per_game"] = df.apply(lambda row: row["minutes"] / row["games"] if row["games"] > 0 else 0, axis=1)

    # Usage metrics
    if all(col in df.columns for col in ["fieldAttempts", "minutes"]):
        df["attempts_per_minute"] = df.apply(lambda row: row["fieldAttempts"] / row["minutes"] if row["minutes"] > 0 else 0, axis=1)

    # Defensive metrics
    if all(col in df.columns for col in ["steals", "blocks"]):
        df["defensive_actions"] = df["steals"] + df["blocks"]

    # Advanced metrics - usage proxy
    if all(col in df.columns for col in ["fieldAttempts", "ftAttempts", "turnovers", "minutes"]):
        df["usage_proxy"] = df.apply(
            lambda row: (row["fieldAttempts"] + 0.44 * row["ftAttempts"] + row["turnovers"]) / row["minutes"]
            if row["minutes"] > 0 else 0,
            axis=1
        )

    # True shooting percentage
    if all(col in df.columns for col in ["points", "fieldAttempts", "ftAttempts"]):
        df["true_shooting"] = df.apply(
            lambda row: row["points"] / (2 * (row["fieldAttempts"] + 0.44 * row["ftAttempts"]))
            if (row["fieldAttempts"] + 0.44 * row["ftAttempts"]) > 0 else 0,
            axis=1
        )

    # Assist to turnover ratio
    if all(col in df.columns for col in ["assists", "turnovers"]):
        df["ast_to_ratio"] = df.apply(
            lambda row: row["assists"] / row["turnovers"] if row["turnovers"] > 0 else row["assists"],
            axis=1
        )

    return df

def one_hot_encode_positions(df, position_col="position"):
    """One-hot encodes player positions."""
    if position_col in df.columns:
        position_dummies = pd.get_dummies(df[position_col], prefix=position_col)

        # Ensure all standard positions exist
        standard_positions = ["PG", "SG", "SF", "PF", "C"]
        for pos in standard_positions:
            dummy_col = f"{position_col}_{pos}"
            if dummy_col not in position_dummies.columns:
                position_dummies[dummy_col] = 0

        position_dummies = position_dummies[[f"{position_col}_{pos}" for pos in standard_positions]]
        position_dummies = position_dummies.astype(int)

        df = pd.concat([df, position_dummies], axis=1)
        df = df.drop(columns=[position_col])
    return df

def sort_players_by_importance(df):
    """Sort players by minutes played to ensure key players are considered first."""
    if "minutes" in df.columns and "minutesPg" in df.columns:
        return df.sort_values(by=["minutes", "minutesPg"], ascending=False).reset_index(drop=True)
    elif "minutes" in df.columns:
        return df.sort_values(by="minutes", ascending=False).reset_index(drop=True)
    elif "minutesPg" in df.columns:
        return df.sort_values(by="minutesPg", ascending=False).reset_index(drop=True)
    return df

def scale_df(df, scaler=None):
    """Scales numeric columns using RobustScaler for better handling of outliers."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if scaler is None:
        # Using RobustScaler instead of StandardScaler to handle outliers better
        scaler = RobustScaler()
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    else:
        # Use the provided scaler
        df[numeric_cols] = scaler.transform(df[numeric_cols])

    return df, scaler

def prepare_team_input_and_labels(df, labels, label_scaler=None):
    """Prepares input features and labels."""
    X = df.to_numpy()

    if not labels:
        return X, np.array([]), None

    Y = np.array(labels).reshape(-1, 1)

    if label_scaler is None:
        # Use StandardScaler instead of MinMaxScaler for labels
        # This allows predictions to go beyond the training range
        label_scaler = StandardScaler()
        Y_scaled = label_scaler.fit_transform(Y)
    else:
        # Use the provided scaler
        Y_scaled = label_scaler.transform(Y)

    return X, Y_scaled, label_scaler

def predict_team_points(model, team_data, team_key, feature_scaler=None, label_scaler=None,
                    max_players=8, unwanted_stats=unwanted_stats,
                    per_game_stats=per_game_stats, per_minute_stats=per_minute_stats):
    X_team, _, feature_scaler_used, label_scaler_used = preprocess_team_season_data(
        team_season_data=team_data,
        team_key=team_key,
        stats_to_remove=unwanted_stats,
        per_game_stats=per_game_stats,
        per_minute_stats=per_minute_stats,
        feature_scaler=feature_scaler,
        label_scaler=label_scaler
    )

    # Get original player data for reference
    df, _ = create_players_df(team_data, team_key)
    df = sort_players_by_importance(df)
    #top_players = df.head(max_players)[['playerName', 'position', 'games', 'minutes', 'points']]

    # Pad or truncate to max_players
    if X_team.shape[0] < max_players:
        padding = np.zeros((max_players - X_team.shape[0], X_team.shape[1]))
        X_team_padded = np.vstack([X_team, padding])
    else:
        X_team_padded = X_team[:max_players]

    # Reshape for model input (batch_size, max_players, features)
    X_team_input = np.expand_dims(X_team_padded, axis=0)

    # Make prediction
    prediction = model.predict(X_team_input).flatten()[0]

    # Convert prediction back to original scale
    prediction_original = label_scaler_used.inverse_transform([[prediction]])[0][0]

    return prediction_original



import os
from tensorflow.keras.models import load_model

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
    existing_player_ids = set(player["id"] for player in PLAYERS_DATA["players"])
    
    # Check if all player IDs exist
    for pid in player_ids:
        if pid not in existing_player_ids:
            raise ValueError(f"Player ID {pid} does not exist in the data")

    # Create a new JSON variable with only the selected players
    selected_players = {
        "labels": [
            9700
        ],
        "players": [
            player for player in PLAYERS_DATA["players"] 
            if player["id"] in player_ids
        ]
    }


    # load the model
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where services.py is
    model_path = os.path.join(script_dir, '..', '..', 'model', 'nba_team_predictor_model.keras')
    nba_team_predictor_model = load_model(model_path)

    nba_team_predictor_model.summary()

    #  some constants
    unwanted_stats = ["id", "playerName", "team", "season", "playerId", "gamesStarted", "image"]
    per_game_stats = [
        "points", "assists", "steals", "blocks", "turnovers", "personalFouls",
        "offensiveRb", "defensiveRb", "totalRb", "fieldGoals", "fieldAttempts",
        "threeFg", "threeAttempts", "twoFg", "twoAttempts", "ft", "ftAttempts"
    ]
    per_minute_stats = per_game_stats

    team_key = "ATL_2024"  # Example: Miami Heat 2023
    team_data = selected_players
    predicted_points = predict_team_points(
        model=nba_team_predictor_model,
        team_data=team_data,
        team_key=team_key,
        unwanted_stats=unwanted_stats,
        per_game_stats=per_game_stats,
        per_minute_stats=per_minute_stats
    )
    
    # Get actual points if available
    actual_points = None
    if "labels" in team_data and team_data["labels"]:
        actual_points = team_data["labels"][0]
    # Display results
    print(f"\n===== Team Prediction: {team_key} =====")
    print(f"Predicted season points: {predicted_points:.1f}")
    if actual_points:
        print(f"Actual season points: {actual_points}")
        print(f"Prediction error: {abs(actual_points - predicted_points):.1f} points")

    # Return the predicted points as int divided by 82 (assuming 82 games in a season)
    return int(predicted_points / 82)  # Return the predicted points per game
    




