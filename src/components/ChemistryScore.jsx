// src/components/ChemistryScore.jsx
import React, { useState } from "react";
import { CircularProgressbar } from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";
//import "./ChemistryScore.css"; // Optional, for additional styling

function ChemistryScore({ lineupPlayers, benchPlayers }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculateScore = async () => {
    setLoading(true);
    try {
      //const response = await fetch("https://your-backend-api.com/api/chemistry", {
      //  method: "POST",
      //  headers: {
      //    "Content-Type": "application/json",
      //  },
      //  body: JSON.stringify(JSON.stringify(lineupPlayers.concat(benchPlayers))),
      //});
      //const data = await response.json();
      // Assuming the API returns an object with a "score" property.
      console.log(JSON.stringify(lineupPlayers.concat(benchPlayers )))
      setScore(82);
    } catch (error) {
      console.error("Error calculating chemistry score:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chemistry-score-container">
      <h2>Chemistry Score</h2>
      <div className="score-display" style={{ width: 200, height: 200 }}>
        {score !== null ? (
          <CircularProgressbar value={score} text={`${score}%`} />
        ) : (
          <CircularProgressbar value={0} text={`0%`} />
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

