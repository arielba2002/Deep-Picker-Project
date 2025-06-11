import React, { useState } from "react";
import "./App.css";
import { Routes, Route } from "react-router-dom";
import SignIn from "./components/SignIn";
import SignUp from "./components/SignUp";

import ChemistryScore from "./components/ChemistryScore";
import Lineup from "./components/Lineup";
import Bench from "./components/Bench";
import SearchPlayers from "./components/SearchPlayers";
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