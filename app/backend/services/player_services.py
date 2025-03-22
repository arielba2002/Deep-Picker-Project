# File: ./Deep-Picker-Project/app/backend/services/player_services.py
from ..config.constants import PLAYERS_DATA
from ..schemas import player_schema
from typing import List

def get_all_players():
    """
    Get all players from the constant data.
    
    Returns:
        List of all players
    """
    return PLAYERS_DATA

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
                    team=player["team"]
                )
            )
            
            if len(matches) >= limit:
                break
                
    return matches