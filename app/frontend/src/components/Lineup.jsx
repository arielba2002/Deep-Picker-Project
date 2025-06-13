// src/components/Lineup.jsx
import React from "react";
import "./Lineup.css"; // Import the CSS for styling

function Lineup({ players, setSelectedPlayer, selectedPlayer, section }) {
  const handlePlayerClick = (player) => {
    if (
      selectedPlayer &&
      selectedPlayer.section === section &&
      selectedPlayer.id === player.id
    ) {
      setSelectedPlayer(null); // Deselect if already selected
    } else {
      setSelectedPlayer({ section, id: player.id });
    }
  };

  // Define basketball positions with better spacing and visibility
  const positions = {
    pointGuard:    { left: '70%', bottom: '25%'  },
    shootingGuard: { left: '30%', bottom: '25%' },
    smallForward:  { left: '12%', bottom: '56%'  },
    powerForward:  { left: '88%', bottom: '50%' },
    center:        { left: '50%', bottom: '45%' },
  };

  // Add position labels for better visibility
  const positionLabels = {
    pointGuard:    'PG',
    shootingGuard: 'SG',
    smallForward:  'SF',
    powerForward:  'PF',
    center:        'C',
    shootingPoint: 'SP',
    comboGuard:    'CG',
    swingman:      'SW',
    stretchFour:   'SF4',
    postPlayer:    'PP',
    pointForward:      'PF',
    smallBallCenter:   'SBC',
    stretchFive:       'SF5',
    pickAndRoll:       'PnR',
    wing:              'W'
  };

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
          style={
            player.position && positions[player.position]
              ? positions[player.position]
              : { bottom: '50%', left: '50%' }
          }
          onClick={() => handlePlayerClick(player)}
        >
          <img
            src={player.image}
            alt={player.name}
            className="player-image"
          />
          <div className="player-label">{player.name}</div>
          <div className="player-position">
            {positionLabels[player.position] || ""}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Lineup;