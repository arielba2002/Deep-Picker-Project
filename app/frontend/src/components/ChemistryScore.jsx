import React, { useState } from "react";
import CircleProgressBar from "./CircleProgressBar";
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
      <h2 style={{marginBottom: 8}}>Chemistry Score</h2>
      <div className="score-display">
        {loading ? (
          <div className="spinner"></div>
        ) : (
          <CircleProgressBar value={score !== null ? score : 0} max={150} />
        )}
      </div>
      <div className="chemistry-score-subtitle">
        Team chemistry is measured from 0 (poor) to 150 (excellent).
      </div>
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

