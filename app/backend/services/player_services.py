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
    # Validate that exactly 8 players are provided
    if len(player_ids) != 8:
        raise ValueError("Exactly 8 player IDs are required for prediction")
        
    # Dummy implementation - just returns a fixed value
    # In a real implementation, this would use a model to predict the score
    return 105