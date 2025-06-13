# File: ./Deep-Picker-Project/app/backend/controllers/player_controller.py
from services import player_services
from schemas import player_schema
from typing import List, Dict

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


def predict_team_score(player_ids: List[int]) -> int:
    """
    Predict the score for a team composed of the specified players.
    
    Args:
        player_ids: List of player IDs in the team
        
    Returns:
        Predicted score
    """
    return player_services.predict_score(player_ids)


def get_all_teams() -> List[str]:
    """
    Get all unique team names.
    
    Returns:
        List of team names
    """
    return player_services.get_all_teams()


def get_top_8_players_by_team(team_name: str) -> List[dict]:
    """
    Get the top 8 players for a specific team based on minutes played.
    
    Args:
        team_name: Name of the team
        
    Returns:
        List of top 8 players for the team
    """
    return player_services.get_top_8_players_by_team(team_name)


def get_all_teams_with_top_8_players() -> Dict[str, List[dict]]:
    """
    Get all teams with their top 8 players.
    
    Returns:
        Dictionary of teams with their top 8 players
    """
    return player_services.get_all_teams_with_top_8_players()