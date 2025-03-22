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
        "players": [
            player for player in PLAYERS_DATA["players"] 
            if player["id"] in player_ids
        ]
    }

    print(selected_players)


    # load the model
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where services.py is
    model_path = os.path.join(script_dir, '..', '..', 'model', 'nba_team_predictor_model.keras')
    nba_team_predictor_model = load_model(model_path)

    nba_team_predictor_model.summary()

    # pre-process

    # # predict

    # Dummy implementation - just returns a fixed value
    # In a real implementation, this would use a model to predict the score
    return 105




