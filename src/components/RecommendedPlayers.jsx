// src/components/RecommendedPlayers.jsx
import React from "react";

function RecommendedPlayers() {
  const recommendedPlayers = [
    { name: "Player A", improvement: "+12%" },
    { name: "Player B", improvement: "+10%" },
    { name: "Player C", improvement: "+7%" },
  ];

  return (
    <div>
      <h2>Recommended Players</h2>
      <ul>
        {recommendedPlayers.map((player) => (
          <li key={player.name}>
            {player.name} {player.improvement}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RecommendedPlayers;

