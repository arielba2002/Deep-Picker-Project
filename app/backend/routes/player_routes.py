# File: ./Deep-Picker-Project/app/backend/routes/player_routes.py
from fastapi import APIRouter, Query, HTTPException, status
from typing import List
from schemas import player_schema
from controllers import player_controller

router = APIRouter()

@router.get(
    "/players/all",
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
    limit: int = Query(200, ge=1, le=1000, description="Maximum number of suggestions to return")
):
    """
    Search for players whose names begin with the provided prefix.
    
    Args:
        prefix: The prefix to search for in player names
        limit: Maximum number of results to return (default: 200)
        
    Returns:
        List of player suggestions matching the prefix
    """
    return player_controller.search_players(prefix, limit)


@router.post(
    "/players/predict-score/",
    response_model=player_schema.PredictionResponse,
    summary="Predict team score",
    description="Predicts the score for a team composed of 8 specified players"
)
def predict_score(request: player_schema.PredictionRequest):
    """
    Predict the score for a team based on 8 player IDs.
    
    Args:
        request: PredictionRequest containing player_ids
        
    Returns:
        PredictionResponse with the predicted score
    """
    if len(request.player_ids) != 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly 8 player IDs are required"
        )
        
    prediction = player_controller.predict_team_score(request.player_ids)
    return player_schema.PredictionResponse(prediction=prediction)


@router.get(
    "/teams/all",
    response_model=player_schema.TeamResponse,
    summary="Get all teams",
    description="Retrieve a list of all NBA teams"
)
def get_all_teams():
    """
    Get all teams.
    
    Returns:
        List of all team names
    """
    teams = player_controller.get_all_teams()
    return player_schema.TeamResponse(teams=teams)


@router.get(
    "/teams/{team_name}/top-players",
    response_model=player_schema.TeamPlayersResponse,
    summary="Get top 8 players for a team",
    description="Retrieve the top 8 players for a specific team based on minutes played"
)
def get_team_top_players(team_name: str):
    """
    Get the top 8 players for a specific team.
    
    Args:
        team_name: Name of the team
        
    Returns:
        TeamPlayersResponse with the team name and its top 8 players
    """
    try:
        players = player_controller.get_top_8_players_by_team(team_name)
        return player_schema.TeamPlayersResponse(team=team_name, players=players)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team '{team_name}' not found or has no players"
        )


@router.get(
    "/teams/all-with-players",
    response_model=player_schema.TeamWithPlayersResponse,
    summary="Get all teams with their top 8 players",
    description="Retrieve all teams along with their top 8 players based on minutes played"
)
def get_all_teams_with_players():
    """
    Get all teams with their top 8 players.
    
    Returns:
        TeamWithPlayersResponse with all teams and their top 8 players
    """
    teams_with_players = player_controller.get_all_teams_with_top_8_players()
    return player_schema.TeamWithPlayersResponse(teams=teams_with_players)

