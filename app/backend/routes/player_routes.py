# File: ./Deep-Picker-Project/app/backend/routes/player_routes.py
from fastapi import APIRouter, Query
from typing import List
from schemas import player_schema
from controllers import player_controller

router = APIRouter()

@router.get(
    "/players/",
    response_model=List[player_schema.Player],
    summary="Get all players",
    description="Retrieve a list of all NBA players for 2024 season"
)
def get_all_players():
    """
    Get all players.
    
    Returns:
        List of all players
    """
    return player_controller.get_all_players()

@router.get(
    "/players/autocomplete/",
    response_model=List[player_schema.PlayerSuggestion],
    summary="Search players by name prefix",
    description="Returns a list of player suggestions that match the provided name prefix"
)
def search_players(
    prefix: str = Query(..., min_length=1, description="The prefix to search for"),
    limit: int = Query(4, ge=1, le=20, description="Maximum number of suggestions to return")
):
    """
    Search for players whose names begin with the provided prefix.
    
    Args:
        prefix: The prefix to search for in player names
        limit: Maximum number of results to return (default: 4)
        
    Returns:
        List of player suggestions matching the prefix
    """
    return player_controller.search_players(prefix, limit)