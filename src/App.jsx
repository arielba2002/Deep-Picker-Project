// src/App.jsx
import React, { useState } from "react";
import "./App.css";

import ChemistryScore from "./components/ChemistryScore";
import RecommendedPlayers from "./components/RecommendedPlayers";
import Lineup from "./components/Lineup";
import Bench from "./components/Bench";
import SearchPlayers from "./components/SearchPlayers";
import deni from './assets/deni.png'
import sunshine from './assets/sunshine.jpg'


function App() {

  const [lineupPlayers, setLineupPlayers] = useState([
    { id: 1, name: "PG", bottom: "20%", left: "50%", image: deni },
    { id: 2, name: "SG", bottom: "33%", left: "80%", image: deni },
    { id: 3, name: "SF", bottom: "67%", left: "25%", image: deni },
    { id: 4, name: "PF", bottom: "67%", left: "60%", image: deni },
    { id: 5, name: "C",  bottom: "55%", left: "38%", image: deni },
  ]);

  const [benchPlayers, setBenchPlayers] = useState([
    { id: 6, name: "Bench1", image: deni },
    { id: 7, name: "Bench2", image: deni },
    { id: 8, name: "Bench3", image: deni },
  ]);

  const [selectedPlayer, setSelectedPlayer] = useState(null);

  // Updates the player's name based on the section and id
  const updatePlayerName = (section, id, newName, newImage, newID) => {
    if (section === "lineup") {
      setLineupPlayers(prev =>
        prev.map(player =>
          player.id === id ? { ...player, name: newName, id: newID, image: newImage } : player
        )
      );
    } else if (section === "bench") {
      setBenchPlayers(prev =>
        prev.map(player =>
          player.id === id ? { ...player, name: newName, id: newID, image: newImage } : player
        )
      );
    }
  };

  return (
    <div className="app-container">
       <aside className="left-panel">
        <ChemistryScore
        lineupPlayers={lineupPlayers} 
        benchPlayers={benchPlayers}
        />
        <RecommendedPlayers />
      </aside>
      <main className="court-panel">
      <Lineup
          players={lineupPlayers}
          setSelectedPlayer={setSelectedPlayer}
          selectedPlayer={selectedPlayer}
          section="lineup"
        />
        <Bench
          players={benchPlayers}
          setSelectedPlayer={setSelectedPlayer}
          selectedPlayer={selectedPlayer}
          section="bench"
        />
      </main>
      <aside className="right-panel">
        <SearchPlayers
          selectedPlayer={selectedPlayer}
          updatePlayerName={updatePlayerName}
        />
      </aside>
    </div>
  );
}

export default App;