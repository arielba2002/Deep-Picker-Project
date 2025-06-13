import React, { useState } from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";

import ChemistryScore from "./components/ChemistryScore";
import StatsPanel from "./components/StatsPanel";
import Lineup from "./components/Lineup";
import Bench from "./components/Bench";
import SearchPlayers from "./components/SearchPlayers";
import TeamSelector from "./components/TeamSelector";
import unchosen from './assets/unchosen.png'
import RequireAuth from "./components/RequireAuth";
import Header from "./components/Header";
import AdminUsers from "./components/AdminUsers";

function App() {

  const [lineupPlayers, setLineupPlayers] = useState([
    { id: 1, name: "not chosen", position: "pointGuard", image: unchosen },
    { id: 2, name: "not chosen", position: "shootingGuard", image: unchosen },
    { id: 3, name: "not chosen", position: "smallForward", image: unchosen },
    { id: 4, name: "not chosen", position: "powerForward", image: unchosen },
    { id: 5, name: "not chosen", position: "center", image: unchosen },
  ]);

  const [benchPlayers, setBenchPlayers] = useState([
    { id: 6, name: "not chosen", image: unchosen },
    { id: 7, name: "not chosen", image: unchosen },
    { id: 8, name: "not chosen", image: unchosen },
  ]);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  const [stats, setStats] = useState({
  })

  // Helper function to map API positions to component positions
  const mapPositionToComponent = (apiPosition) => {
    const positionMap = {
      'PG': 'pointGuard',
      'SG': 'shootingGuard', 
      'SF': 'smallForward',
      'PF': 'powerForward',
      'C': 'center'
    };
    return positionMap[apiPosition] || 'center'; // Default to center if unknown
  };

  // Helper function to check if any players are selected
  const hasPlayersSelected = () => {
    const allPlayers = [...lineupPlayers, ...benchPlayers];
    return allPlayers.some(player => player.name !== "not chosen");
  };

  // Helper function to clear all players
  const clearAllPlayers = () => {
    setLineupPlayers([
      { id: 1, name: "not chosen", position: "pointGuard", image: unchosen },
      { id: 2, name: "not chosen", position: "shootingGuard", image: unchosen },
      { id: 3, name: "not chosen", position: "smallForward", image: unchosen },
      { id: 4, name: "not chosen", position: "powerForward", image: unchosen },
      { id: 5, name: "not chosen", position: "center", image: unchosen },
    ]);
    setBenchPlayers([
      { id: 6, name: "not chosen", image: unchosen },
      { id: 7, name: "not chosen", image: unchosen },
      { id: 8, name: "not chosen", image: unchosen },
    ]);
    setSelectedPlayer(null);
  };

  // Handle team selection
  const handleTeamSelect = (teamPlayers) => {
    if (teamPlayers.length < 8) {
      console.warn(`Team has only ${teamPlayers.length} players, need 8`);
    }

    // Group players by position for better distribution
    const playersByPosition = {
      'PG': [],
      'SG': [],
      'SF': [],
      'PF': [],
      'C': []
    };

    // Group players by their positions
    teamPlayers.forEach(player => {
      const position = player.position || 'C';
      if (playersByPosition[position]) {
        playersByPosition[position].push(player);
      } else {
        playersByPosition['C'].push(player); // Default to center
      }
    });

    // Assign players to lineup positions (5 players)
    const newLineupPlayers = [];
    const positions = ['PG', 'SG', 'SF', 'PF', 'C'];
    const usedPlayers = new Set();

    positions.forEach((pos, index) => {
      // Try to find a player for this position
      let playerForPosition = playersByPosition[pos].find(p => !usedPlayers.has(p.id));
      
      // If no player found for this position, find any available player
      if (!playerForPosition) {
        for (const posKey of Object.keys(playersByPosition)) {
          playerForPosition = playersByPosition[posKey].find(p => !usedPlayers.has(p.id));
          if (playerForPosition) break;
        }
      }

      if (playerForPosition) {
        usedPlayers.add(playerForPosition.id);
        newLineupPlayers.push({
          id: playerForPosition.id,
          name: playerForPosition.playerName,
          position: mapPositionToComponent(pos),
          image: playerForPosition.image || unchosen
        });
      } else {
        // Fallback if no players available
        newLineupPlayers.push({
          id: index + 1,
          name: "not chosen",
          position: mapPositionToComponent(pos),
          image: unchosen
        });
      }
    });

    // Assign remaining players to bench (3 players)
    const newBenchPlayers = [];
    const remainingPlayers = teamPlayers.filter(p => !usedPlayers.has(p.id));
    
    for (let i = 0; i < 3; i++) {
      if (remainingPlayers[i]) {
        newBenchPlayers.push({
          id: remainingPlayers[i].id,
          name: remainingPlayers[i].playerName,
          image: remainingPlayers[i].image || unchosen
        });
      } else {
        newBenchPlayers.push({
          id: i + 6,
          name: "not chosen", 
          image: unchosen
        });
      }
    }

    setLineupPlayers(newLineupPlayers);
    setBenchPlayers(newBenchPlayers);
  };

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
    <Routes>
      <Route path="/signin" element={<SignIn />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/admin/users" element={<AdminUsers />} />
      <Route path="/*" element={
        <RequireAuth>
          <>
            <Header />
            <div className="app-container">
              <aside className="left-panel">
                <ChemistryScore
                  lineupPlayers={lineupPlayers}
                  benchPlayers={benchPlayers}
	          setStats={setStats}
                />
	        <StatsPanel stats={stats} />
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
                <button 
                  className="clear-team-button"
                  onClick={clearAllPlayers}
                >
                  Clear All Players
                </button>
                <TeamSelector 
                  onTeamSelect={handleTeamSelect}
                  disabled={false}
                />
                <SearchPlayers
                  selectedPlayer={selectedPlayer}
                  updatePlayerName={updatePlayerName}
                  lineupPlayers={lineupPlayers}
                  benchPlayers={benchPlayers}
                />
              </aside>
            </div>
          </>
        </RequireAuth>
      } />
    </Routes>
  );
}

export default App;
