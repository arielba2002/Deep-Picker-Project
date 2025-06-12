import React, { useState, useEffect, useRef } from "react";
import "./SearchPlayers.css";
import Toast from "./Toast";

function SearchPlayers({ selectedPlayer, updatePlayerName, lineupPlayers, benchPlayers }) {
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showToast, setShowToast] = useState(false);
  const searchContainerRef = useRef(null);

  // Get all current player IDs from lineup and bench
  const currentPlayerIds = [...lineupPlayers, ...benchPlayers]
    .filter(player => player.id !== "not chosen")
    .map(player => player.id);

  useEffect(() => {
    // If input is empty, fetch all players
    if (!inputValue.trim()) {
      setSuggestions([]);
      return;
    }

    const delayDebounceFn = setTimeout(() => {
      fetch(`http://localhost:8888/api/v1/players/autocomplete/?prefix=${inputValue.trim()}`)
        .then((res) => res.json())
        .then((data) => {
          // Filter out players that are already in lineup or bench
          const filteredSuggestions = data.filter(
            suggestion => !currentPlayerIds.includes(suggestion.id)
          );
          setSuggestions(filteredSuggestions);
        })
        .catch((error) => {
          console.error("Error fetching suggestions:", error);
        });
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [inputValue, currentPlayerIds]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target)) {
        setSuggestions([]);
        setInputValue("");
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const handleSuggestionClick = (suggestion) => {
    if (selectedPlayer) {
      // Check if player is already in lineup or bench
      if (currentPlayerIds.includes(suggestion.id)) {
        setShowToast(true);
        return;
      }
      
      updatePlayerName(selectedPlayer.section, selectedPlayer.id, suggestion.playerName, suggestion.image, suggestion.id);
      setInputValue("");
      setSuggestions([]);
    }
  };

  return (
    <div className="search-container" ref={searchContainerRef}>
      <div className="replace-player-card">
        <div className="replace-player-header">
          <h2>Replace Selected Player</h2>
        </div>
        <div className="replace-player-subtitle">Search and select a new player to substitute in your lineup or bench.</div>
        <input
          type="text"
          placeholder="Search for a player name..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          disabled={!selectedPlayer}
          className={`search-input${!selectedPlayer ? " search-input-disabled" : ""}`}
        />
        {suggestions.length > 0 && (
          <ul className="suggestions-list">
            {suggestions.map((suggestion) => (
              <li
                key={suggestion.id}
                onClick={() => handleSuggestionClick(suggestion)}
                className="suggestion-item"
              >
                <img
                  src={suggestion.image}
                  alt={suggestion.name}
                  className="suggestion-image"
                />
                <div className="suggestion-info">
                  <span className="suggestion-name">{suggestion.playerName}</span>
                  <span className="suggestion-position">{suggestion.position || 'Position not specified'}</span>
                </div>
              </li>
            ))}
          </ul>
        )}
        {!selectedPlayer && <p className="replace-player-disabled-msg">Please select a player to replace.</p>}
      </div>
      {showToast && (
        <Toast
          message="This player is already in your lineup or bench!"
          onClose={() => setShowToast(false)}
        />
      )}
    </div>
  );
}

export default SearchPlayers;