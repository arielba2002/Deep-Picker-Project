import React, { useState } from "react";
import CircleProgressBar from "./CircleProgressBar";
import "./ChemistryScore.css";

function ChemistryScore({ lineupPlayers, benchPlayers, setStats }) {
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
      // here i dont want to set the stat of the data.prediction["Chemistry Score"] which is the last element
      // setStats(data.prediction) will also add the Chemistry Score to the stats
      setStats(
        Object.fromEntries(
          Object.entries(data.prediction).slice(0, -1)
        )
      );

      setScore(data.prediction["Chemistry Score"]);
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
          <CircleProgressBar value={score !== null ? score : 0} max={100} />
        )}
      </div>
      <div className="chemistry-score-subtitle">
        0 (poor) to 100 (excellent)
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

