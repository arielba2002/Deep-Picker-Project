// src/components/Lineup.jsx
import React from "react";
import "./Lineup.css"; // Import the CSS for styling

function Lineup({ players, setSelectedPlayer, selectedPlayer, section }) {
  return (
    <div className="lineup-container">
      {players.map((player) => (
        <div
          key={player.id}
          className={`player ${
            selectedPlayer &&
            selectedPlayer.section === section &&
            selectedPlayer.id === player.id
              ? "selected"
              : ""
          }`}
          style={{ bottom: player.bottom, left: player.left }}
          onClick={() => setSelectedPlayer({ section, id: player.id })}
        >
          <img
            src={player.image}
            alt={player.name}
            className="player-image"
          />
          {/* Optionally, display the player's name below or on top of the image */}
          <div className="player-label">{player.name}</div>
        </div>
      ))}
    </div>
  );
}

export default Lineup;

