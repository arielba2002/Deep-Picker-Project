# File: ./Deep-Picker-Project/app/backend/services/player_services_minimal.py
from schemas import player_schema
from typing import List, Dict
import datetime
import requests
import json
from pathlib import Path

# Module-level cache
_players_cache: List[dict] = []
_last_fetch_year: int = None
_headshots_cache: dict = {}

def _normalize_name(name: str) -> str:
    """Normalize a player name by removing special characters and converting to ASCII."""
    # First, handle Jr./Sr. suffixes with and without commas
    name = name.replace(" Jr.", ", Jr.").replace(" Sr.", ", Sr.")
    name = name.replace("CJ", "C.J.")

    # Replace common special characters with their ASCII equivalents
    replacements = {
        'ć': 'c', 'č': 'c', 'š': 's', 'ž': 'z',
        'Ć': 'C', 'Č': 'C', 'Š': 'S', 'Ž': 'Z',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N',
        'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O',
        'ä': 'a', 'Ä': 'A',
        'ë': 'e', 'Ë': 'E',
        'ï': 'i', 'Ï': 'I',
        'ÿ': 'y', 'Ÿ': 'Y',
        'œ': 'oe', 'Œ': 'OE',
        'æ': 'ae', 'Æ': 'AE',
        'ß': 'ss'
    }
    
    normalized = name
    for special, ascii_char in replacements.items():
        normalized = normalized.replace(special, ascii_char)
    
    return normalized

def _load_headshots() -> dict:
    """
    Loads the player headshots mapping from the JSON file.
    """
    global _headshots_cache
    if not _headshots_cache:
        headshots_path = Path(__file__).parent.parent / "config" / "player_headshots.json"
        try:
            with open(headshots_path, 'r') as f:
                _headshots_cache = json.load(f)
            print(f"[player_services] Loaded {len(_headshots_cache)} player headshots")
        except Exception as e:
            print(f"[player_services] Failed to load headshots ({e})")
            _headshots_cache = {}
    return _headshots_cache

def _fetch_players() -> List[dict]:
    """
    Fetches the full current-season roster from the NBA API once per process.
    """
    global _players_cache, _last_fetch_year

    # Use the calendar year as the "season"
    season = datetime.datetime.now().year

    # Re-fetch if first time or season changed
    if _last_fetch_year != season or not _players_cache:
        url = (
            f"http://rest.nbaapi.com/api/PlayerDataTotals/"
            f"query?season={season}&sortBy=PlayerName&pageSize=1000"
        )
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            raw_players = resp.json()
            print(f"[player_services] Fetched {len(raw_players)} players from NBA API")
        except Exception as e:
            print(f"[player_services] API fetch failed ({e}), using mock data")
            # Load headshots for mock data too
            headshots = _load_headshots()
            # Return mock data if API fails
            _players_cache = [
                {
                    "id": 1,
                    "playerName": "LeBron James",
                    "team": "LAL",
                    "position": "SF",
                    "age": 39,
                    "games": 82,
                    "gamesStarted": 82,
                    "minutesPg": 35.3,
                    "fieldGoals": 9,
                    "fieldAttempts": 18,
                    "fieldPercent": 0.540,
                    "threeFg": 3,
                    "threeAttempts": 8,
                    "threePercent": 0.375,
                    "twoFg": 6,
                    "twoAttempts": 10,
                    "twoPercent": 0.600,
                    "effectFgPercent": 0.590,
                    "ft": 6,
                    "ftAttempts": 8,
                    "ftPercent": 0.750,
                    "offensiveRb": 1,
                    "defensiveRb": 7,
                    "totalRb": 8,
                    "assists": 7,
                    "steals": 1,
                    "blocks": 1,
                    "turnovers": 3,
                    "personalFouls": 2,
                    "points": 25,
                    "season": season,
                    "playerId": "lebron-james",
                    "image": headshots.get(_normalize_name("LeBron James"), "")
                }
            ]
            _last_fetch_year = season
            return _players_cache

        # Load headshots mapping
        headshots = _load_headshots()

        # Normalize to your schema shape
        _players_cache = [
            {
                "id": p["id"],
                "playerName": p["playerName"],
                "team": p.get("team", ""),
                "position": p.get("position", ""),
                "age": p.get("age"),
                "games": p.get("games"),
                "gamesStarted": p.get("gamesStarted"),
                "minutesPg": p.get("minutesPg"),
                "fieldGoals": p.get("fieldGoals"),
                "fieldAttempts": p.get("fieldAttempts"),
                "fieldPercent": p.get("fieldPercent", 0.0),
                "threeFg": p.get("threeFg"),
                "threeAttempts": p.get("threeAttempts"),
                "threePercent": p.get("threePercent", 0.0),
                "twoFg": p.get("twoFg"),
                "twoAttempts": p.get("twoAttempts"),
                "twoPercent": p.get("twoPercent", 0.0),
                "effectFgPercent": p.get("effectFgPercent", 0.0),
                "ft": p.get("ft"),
                "ftAttempts": p.get("ftAttempts"),
                "ftPercent": p.get("ftPercent", 0.0),
                "offensiveRb": p.get("offensiveRb"),
                "defensiveRb": p.get("defensiveRb"),
                "totalRb": p.get("totalRb"),
                "assists": p.get("assists"),
                "steals": p.get("steals"),
                "blocks": p.get("blocks"),
                "turnovers": p.get("turnovers"),
                "personalFouls": p.get("personalFouls"),
                "points": p.get("points"),
                "season": p.get("season"),
                "playerId": p.get("playerId", ""),
                "image": headshots.get(_normalize_name(p["playerName"]), ""),
            }
            for p in raw_players
        ]

        # Remove duplicates based on player ID
        seen_ids = set()
        unique_players = []
        for player in _players_cache:
            if player["id"] not in seen_ids:
                seen_ids.add(player["id"])
                unique_players.append(player)
        
        _players_cache = unique_players
        print(f"[player_services] Cached {len(_players_cache)} unique players in memory")
        _last_fetch_year = season

    return _players_cache

def get_all_players() -> List[dict]:
    """Returns the full cached roster for the current season."""
    return _fetch_players()

def search_players(prefix: str, limit: int = 100) -> List[player_schema.PlayerSuggestion]:
    """Search players by name prefix against the in-memory cache."""
    if not prefix:
        return []

    prefix_lower = prefix.lower()
    matches: List[player_schema.PlayerSuggestion] = []
    seen_ids = set()
    seen_names = set()

    for p in _fetch_players():
        if prefix_lower in p["playerName"].lower():
            if p["id"] not in seen_ids and p["playerName"] not in seen_names:
                seen_ids.add(p["id"])
                seen_names.add(p["playerName"])
                matches.append(
                    player_schema.PlayerSuggestion(
                        id=p["id"],
                        playerName=p["playerName"],
                        image=p["image"],
                    )
                )
                if len(matches) >= limit:
                    break

    print(f"[player_services] Search returned {len(matches)} unique players for prefix '{prefix}'")
    return matches

def predict_score(player_ids: List[int]) -> Dict[str, float]:
    """Generate a prediction score based on player IDs (dynamic calculation)."""
    if len(player_ids) != 8:
        raise ValueError("Exactly 8 player IDs are required for prediction")

    if len(set(player_ids)) != len(player_ids):
        raise ValueError("All player IDs must be different from each other")

    players = get_all_players()
    existing_player_ids = set(p["id"] for p in players)

    for pid in player_ids:
        if pid not in existing_player_ids:
            raise ValueError(f"Player ID {pid} does not exist in the data")

    # Get the selected players
    selected_players = [p for p in players if p["id"] in player_ids]
    
    # Calculate team stats based on selected players
    total_points = sum(p.get("points", 0) for p in selected_players)
    total_assists = sum(p.get("assists", 0) for p in selected_players)
    total_rebounds = sum(p.get("totalRb", 0) for p in selected_players)
    total_blocks = sum(p.get("blocks", 0) for p in selected_players)
    total_steals = sum(p.get("steals", 0) for p in selected_players)
    total_fg = sum(p.get("fieldGoals", 0) for p in selected_players)
    total_fga = sum(p.get("fieldAttempts", 0) for p in selected_players)
    total_3pm = sum(p.get("threeFg", 0) for p in selected_players)
    total_3pa = sum(p.get("threeAttempts", 0) for p in selected_players)
    total_ftm = sum(p.get("ft", 0) for p in selected_players)
    total_fta = sum(p.get("ftAttempts", 0) for p in selected_players)
    total_oreb = sum(p.get("offensiveRb", 0) for p in selected_players)
    total_dreb = sum(p.get("defensiveRb", 0) for p in selected_players)
    total_fouls = sum(p.get("personalFouls", 0) for p in selected_players)
    total_turnovers = sum(p.get("turnovers", 0) for p in selected_players)
    
    # Calculate averages and projections for 82-game season
    avg_points = total_points / len(selected_players) if selected_players else 0
    avg_assists = total_assists / len(selected_players) if selected_players else 0
    avg_rebounds = total_rebounds / len(selected_players) if selected_players else 0
    
    # Project team stats (multiply by team multiplier)
    team_points = avg_points * 5.2  # 5 starters contributing more
    team_assists = avg_assists * 4.8
    team_rebounds = avg_rebounds * 4.5
    team_blocks = (total_blocks / len(selected_players)) * 3.2 if selected_players else 0
    team_steals = (total_steals / len(selected_players)) * 4.1 if selected_players else 0
    team_fg = (total_fg / len(selected_players)) * 5.1 if selected_players else 0
    team_fga = (total_fga / len(selected_players)) * 5.3 if selected_players else 0
    team_3pm = (total_3pm / len(selected_players)) * 4.9 if selected_players else 0
    team_3pa = (total_3pa / len(selected_players)) * 5.2 if selected_players else 0
    team_ftm = (total_ftm / len(selected_players)) * 4.7 if selected_players else 0
    team_fta = (total_fta / len(selected_players)) * 4.8 if selected_players else 0
    team_oreb = (total_oreb / len(selected_players)) * 3.8 if selected_players else 0
    team_dreb = (total_dreb / len(selected_players)) * 4.2 if selected_players else 0
    team_fouls = (total_fouls / len(selected_players)) * 4.6 if selected_players else 0
    team_turnovers = (total_turnovers / len(selected_players)) * 4.3 if selected_players else 0
    
    # Calculate percentages
    fg_percent = (team_fg / team_fga * 100) if team_fga > 0 else 0
    three_percent = (team_3pm / team_3pa * 100) if team_3pa > 0 else 0
    ft_percent = (team_ftm / team_fta * 100) if team_fta > 0 else 0
    
    # Calculate win percentage based on team strength
    # Higher points, assists, rebounds, lower turnovers = better win %
    strength_score = (team_points * 0.4 + team_assists * 0.3 + team_rebounds * 0.2 - team_turnovers * 0.1)
    win_percentage = min(0.850, max(0.150, strength_score / 180))  # Normalize to 15-85% range
    
    # Calculate conference rank (inverse of win %)
    conf_rank = max(1, min(15, int(16 - (win_percentage * 15))))
    
    # Calculate chemistry score based on multiple factors
    # Factors: balanced stats, win percentage, assists (teamwork), low turnovers
    assist_balance = min(100, team_assists * 2.5)  # Assists indicate teamwork
    turnover_penalty = max(0, 100 - team_turnovers * 2)  # Fewer turnovers = better chemistry
    win_bonus = win_percentage * 100
    
    chemistry_score = int((assist_balance * 0.4 + turnover_penalty * 0.3 + win_bonus * 0.3))
    chemistry_score = max(1, min(100, chemistry_score))  # Clamp between 1-100
    
    return {
        "Points": round(team_points, 1),
        "Assists": round(team_assists, 1),
        "Rebounds": round(team_rebounds, 1),
        "Blocks": round(team_blocks, 1),
        "Steals": round(team_steals, 1),
        "Win %": round(win_percentage, 3),
        "Conf Rank": conf_rank,
        "FGM": round(team_fg, 1),
        "FGA": round(team_fga, 1),
        "FG%": round(fg_percent, 1),
        "3PM": round(team_3pm, 1),
        "3PA": round(team_3pa, 1),
        "3P%": round(three_percent, 1),
        "FTM": round(team_ftm, 1),
        "FTA": round(team_fta, 1),
        "FT%": round(ft_percent, 1),
        "OREB": round(team_oreb, 1),
        "DREB": round(team_dreb, 1),
        "Fouls": round(team_fouls, 1),
        "Turnovers": round(team_turnovers, 1),
        "Chemistry Score": chemistry_score
    }

def get_all_teams() -> List[str]:
    """Get all unique team names from the current players data."""
    players = _fetch_players()
    teams = list(set(player["team"] for player in players 
                    if player["team"] and not player["team"].endswith("TM")))
    return sorted(teams)

def get_top_8_players_by_team(team_name: str) -> List[dict]:
    """Get the top 8 players for a specific team based on minutes played."""
    players = _fetch_players()
    
    # Filter players by team
    team_players = [player for player in players if player["team"] == team_name]
    
    # Sort by minutes played (descending) and take top 8
    team_players.sort(key=lambda x: x["minutesPg"] or 0, reverse=True)
    top_8_players = team_players[:8]
    
    return top_8_players

def get_all_teams_with_top_8_players() -> Dict[str, List[dict]]:
    """Get all teams with their top 8 players based on minutes played."""
    teams = get_all_teams()
    teams_with_players = {}
    
    for team in teams:
        teams_with_players[team] = get_top_8_players_by_team(team)
    
    return teams_with_players 