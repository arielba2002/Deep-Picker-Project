// src/components/Bench.jsx
import React from "react";
import "./Bench.css";
import deni from '../assets/deni.png'

function Bench({ players, setSelectedPlayer, selectedPlayer, section }) {
  return (
    <div className="bench-container">
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
          onClick={() => setSelectedPlayer({ section, id: player.id })}
        >
          <img src={player.image} alt={player.name} className="bench-player-image" />
          <div className="player-label">{player.name}</div>
        </div>
      ))}
    </div>
  );
}

export default Bench;
