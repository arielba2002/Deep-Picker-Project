import React, { useState, useEffect } from "react";
import "./SearchPlayers.css";
import sunshine from '../assets/sunshine.jpg'

function SearchPlayers({ selectedPlayer, updatePlayerName }) {
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  // Debounced API call to fetch suggestions based on the input value
  useEffect(() => {
    if (!inputValue.trim()) {
      setSuggestions([]);
      return;
    }

    setSuggestions([{name: "lebron", image: sunshine, id: 991}]);
    return;

    const delayDebounceFn = setTimeout(() => {
      fetch(`https://your-backend-api.com/api/players?suggest=${inputValue.trim()}`)
        .then((res) => res.json())
        .then((data) => {
          // Assume the response is an array of suggestion objects: [{ id, name }]
          setSuggestions(data);
        })
        .catch((error) => {
          console.error("Error fetching suggestions:", error);
        });
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [inputValue]);

  // When a suggestion is clicked, update the player's name immediately
  const handleSuggestionClick = (suggestion) => {
    if (selectedPlayer) {
      updatePlayerName(selectedPlayer.section, selectedPlayer.id, suggestion.name, suggestion.image, suggestion.id);
      setInputValue("");
      setSuggestions([]);
    }
  };

  return (
    <div className="search-container">
      <h2>Replace Selected Player</h2>
      <input
        type="text"
        placeholder="Search for a player name..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={!selectedPlayer}
        className="search-input"
      />

      {/* Display suggestions */}
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
            <span className="suggestion-name">{suggestion.name}</span>
          </li>
          ))}
        </ul>
      )}
      {!selectedPlayer && <p>Please select a player to replace.</p>}
    </div>
  );
}

export default SearchPlayers;