import React, { useState, useEffect } from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";
import ChemistryScore from "./components/ChemistryScore";
import RecommendedPlayers from "./components/RecommendedPlayers";
import Lineup from "./components/Lineup";
import Bench from "./components/Bench";
import SearchPlayers from "./components/SearchPlayers";
import unchosen from './assets/unchosen.png'
import RequireAuth from "./components/RequireAuth";
import Header from "./components/Header";
import AdminUsers from "./components/AdminUsers";

function App() {
  const [backendStatus, setBackendStatus] = useState("");
  const [error, setError] = useState("");

  // Test backend connection on component mount
  useEffect(() => {
    testBackendConnection();
  }, []);

  const testBackendConnection = async () => {
    try {
      const response = await fetch("/api/test");
      const data = await response.json();
      if (response.ok) {
        setBackendStatus(`✅ ${data.message}`);
      } else {
        setBackendStatus(`❌ Error: ${data.detail || 'Unknown error'}`);
      }
    } catch (err) {
      setError(`Failed to connect to backend: ${err.message}`);
      console.error("Backend connection error:", err);
    }
  };

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

  const dummyPlayers = [
    {name: "Lebron James", image: "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png", team: "LAL"},
    {name: "Stephen Curry", image: "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png", team: "GSW"},
    {name: "Giannis Antetokounmpo", image: "https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png", team: "MIL"}
  ]

  const [selectedPlayer, setSelectedPlayer] = useState(null);

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
          <div className="App">
            <Header />
            {/* Connection status indicator */}
            <div style={{
              padding: '10px',
              margin: '10px',
              borderRadius: '4px',
              backgroundColor: backendStatus ? '#e8f5e9' : '#ffebee',
              color: backendStatus ? '#2e7d32' : '#c62828',
              textAlign: 'center',
              fontWeight: 'bold'
            }}>
              {error ? error : (backendStatus || 'Connecting to backend...')}
            </div>
            <div className="app-container">
              <aside className="left-panel">
                <ChemistryScore
                  lineupPlayers={lineupPlayers}
                  benchPlayers={benchPlayers}
                />
                <RecommendedPlayers
                  players={dummyPlayers}
                />
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
          </div>
        </RequireAuth>
      } />
    </Routes>
  );
}

export default App;