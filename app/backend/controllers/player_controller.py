# File: ./Deep-Picker-Project/app/backend/controllers/player_controller.py
from services import player_services
from schemas import player_schema
from typing import List

def get_all_players():
    """
    Get all players.
    
    Returns:
        List of all players
    """
    return player_services.get_all_players()

def search_players(prefix: str, limit: int = 4) -> List[player_schema.PlayerSuggestion]:
    """
    Search players by name prefix.
    
    Args:
        prefix: The prefix to search for
        limit: Maximum number of suggestions to return
        
    Returns:
        List of player suggestions matching the prefix
    """
    return player_services.search_players(prefix, limit)