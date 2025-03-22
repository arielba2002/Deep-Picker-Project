import React, { useState } from "react";
import "react-circular-progressbar/dist/styles.css";
import "./ChemistryScore.css";

function ChemistryScore({ lineupPlayers, benchPlayers }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculateScore = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8888/api/v1/players/predict-score/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({"player_ids": lineupPlayers.concat(benchPlayers).map(o => o.id)}),
      });
      const data = await response.json();
      console.log(JSON.stringify({"player_ids": lineupPlayers.concat(benchPlayers).map(o => o.id)}))
      setScore(data.predicted_score);
    } catch (error) {
      console.error("Error calculating chemistry score:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chemistry-score-container">
      <h2>Chemistry Score</h2>
      <div className="score-display">
        {loading ? (
          <div className="spinner"></div>
        ) : score !== null ? (
          <div className="score-value">{score}</div>
        ) : (
          <div className="score-value">{0}</div>
        )}
      </div>
      <br/>
      <button 
        className="calculate-button" 
        onClick={handleCalculateScore}
        disabled={loading}
      >
        {loading ? "Calculating..." : "Calculate Chemistry Score"}
      </button>
    </div>
  );
}

export default ChemistryScore;

