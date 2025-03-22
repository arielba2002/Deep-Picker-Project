# File: ./Deep-Picker-Project/app/backend/schemas/player_schema.py
from pydantic import BaseModel
from typing import Optional

class PlayerBase(BaseModel):
    id: int
    playerName: str
    position: str
    age: int
    team: str
    season: int
    
class Player(PlayerBase):
    games: int
    gamesStarted: int
    minutesPg: float
    fieldGoals: int
    fieldAttempts: int
    fieldPercent: float
    threeFg: int
    threeAttempts: int
    threePercent: Optional[float] = None
    twoFg: int
    twoAttempts: int
    twoPercent: float
    effectFgPercent: float
    ft: int
    ftAttempts: int
    ftPercent: Optional[float] = None
    offensiveRb: int
    defensiveRb: int
    totalRb: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    personalFouls: int
    points: int
    playerId: str
    
    class Config:
        from_attributes = True

class PlayerSuggestion(BaseModel):
    id: int
    playerName: str
    team: str