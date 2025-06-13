import React, { useState, useEffect } from "react";
import "./TeamSelector.css";

function TeamSelector({ onTeamSelect, disabled = false }) {
  const [teams, setTeams] = useState([]);
  const [selectedTeam, setSelectedTeam] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Fetch all teams when component mounts
    const fetchTeams = async () => {
      try {
        const response = await fetch("http://localhost:8888/api/v1/teams/all");
        const data = await response.json();
        setTeams(data.teams);
      } catch (error) {
        console.error("Error fetching teams:", error);
      }
    };

    fetchTeams();
  }, []);

  const handleTeamSelect = async (teamName) => {
    if (!teamName || isLoading) return;

    setSelectedTeam(teamName);
    setIsLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8888/api/v1/teams/${encodeURIComponent(teamName)}/top-players`
      );
      const data = await response.json();
      
      if (data.players && data.players.length > 0) {
        onTeamSelect(data.players);
      }
    } catch (error) {
      console.error("Error fetching team players:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="team-selector-wrapper">
      <div className="team-selector-container">
        <h3 className="team-selector-title">Select a Team </h3>
        <p className="team-selector-subtitle">
          Select a team to automatically load their top 8 players by minutes played
        </p>
        
        <div className="team-dropdown-container">
          <select
            className={`team-dropdown ${disabled ? 'team-dropdown-disabled' : ''}`}
            value={selectedTeam}
            onChange={(e) => handleTeamSelect(e.target.value)}
            disabled={disabled || isLoading}
          >
            <option value="">Choose your team...</option>
            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
          
          {isLoading && (
            <div className="team-loading-indicator">
              Loading players...
            </div>
          )}
        </div>
        
        {disabled && (
          <p className="team-selector-disabled-msg">
            Clear all players to select a team
          </p>
        )}
      </div>
    </div>
  );
}

export default TeamSelector; 