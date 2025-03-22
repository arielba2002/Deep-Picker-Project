import React from "react";
import "./RecommendedPlayers.css";

function RecommendedPlayers({ players }) {
  return (
    <div className="recommended-players-container">
      <h2>Recommended Players</h2>
      <div className="recommended-players-list">
        {players.map((player) => (
          <div key={player.id} className="recommended-player-card">
            <img
              src={player.image}
              alt={player.name}
              className="recommended-player-image"
            />
            <div className="recommended-player-info">
              <div className="recommended-player-name">{player.name}</div>
              <div className="recommended-player-improvement">{player.team}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendedPlayers;
