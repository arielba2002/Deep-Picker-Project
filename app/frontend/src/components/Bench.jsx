// src/components/Bench.jsx
import React from "react";
import "./Bench.css";

function Bench({ players, setSelectedPlayer, selectedPlayer, section }) {
  const handlePlayerClick = (player) => {
    if (selectedPlayer && selectedPlayer.section === section && selectedPlayer.id === player.id) {
      setSelectedPlayer(null); // Deselect if already selected
    } else {
      setSelectedPlayer({ section, id: player.id });
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
            onClick={() => handlePlayerClick(player)}
          >
            <img src={player.image} alt={player.name} className="bench-player-image" />
            <div className="player-label">{player.name}</div>
          </div>
        ))}
      </div>
      <div className="bench-bar"></div>
    </div>
  );
}

export default Bench;
