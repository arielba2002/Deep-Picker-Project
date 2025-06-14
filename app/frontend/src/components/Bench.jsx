// src/components/Bench.jsx
import React from "react";
import "./Bench.css";

function Bench({ players, setSelectedPlayer, selectedPlayer, section }) {
  const handlePlayerClick = (playerId) => {
    if (selectedPlayer && selectedPlayer.section === section && selectedPlayer.id === playerId) {
      // If the clicked player is already selected, unselect it
      setSelectedPlayer(null);
    } else {
      // Otherwise, select the clicked player
      setSelectedPlayer({ section, id: playerId });
    }
  };

  return (
    <div className="bench-container">
      <div className="bench-players-row">
        {players.map(player => (
          <div
            key={player.id}
            className={`bench-player ${
              selectedPlayer &&
              selectedPlayer.section === section &&
              selectedPlayer.id === player.id
                ? "selected"
                : ""
            }`}
            onClick={() => handlePlayerClick(player.id)}
          >
            <img src={player.image} alt={player.name} className="bench-player-image" />
            <div className="bench-player-label">{player.name}</div>
          </div>
        ))}
      </div>
      <div className="bench-bar"></div>
    </div>
  );
}

export default Bench;
