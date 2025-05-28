# File: ./Deep-Picker-Project/app/backend/routes/player_routes.py
from fastapi import APIRouter, Query
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
        
    predicted_score = player_controller.predict_team_score(request.player_ids)
    return player_schema.PredictionResponse(predicted_score=predicted_score)