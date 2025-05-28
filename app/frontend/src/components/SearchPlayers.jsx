import React, { useState, useEffect } from "react";
import "./SearchPlayers.css";

function SearchPlayers({ selectedPlayer, updatePlayerName }) {
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    // If input is empty, fetch all players
    if (!inputValue.trim()) {
      return;
    }

    const delayDebounceFn = setTimeout(() => {
      fetch(`http://localhost:8888/api/v1/players/autocomplete/?prefix=${inputValue.trim()}`)
        .then((res) => res.json())
        .then((data) => {
          setSuggestions(data);
        })
        .catch((error) => {
          console.error("Error fetching suggestions:", error);
        });
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [inputValue]);

  const handleSuggestionClick = (suggestion) => {
    if (selectedPlayer) {
      updatePlayerName(selectedPlayer.section, selectedPlayer.id, suggestion.playerName, suggestion.image, suggestion.id);
      setInputValue("");
      // Don't clear suggestions, allow all to remain or refresh

    }
  };

  return (
    <div className="search-container">
      <div className="replace-player-card">
        <div className="replace-player-header">
          <span className="replace-icon" role="img" aria-label="replace">🔄</span>
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
                <span className="suggestion-name">{suggestion.playerName}</span>
              </li>
            ))}
          </ul>
        )}
        {!selectedPlayer && <p className="replace-player-disabled-msg">Please select a player to replace.</p>}
      </div>
    </div>
  );
}

export default SearchPlayers;