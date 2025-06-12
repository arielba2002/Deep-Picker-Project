// src/components/StatsPanel.jsx
import React from "react";
import "./StatsPanel.css";

function StatsPanel({ stats }) {
  return (
    <div className="stats-panel-container">
      <h2>Team Stats</h2>
      <ul className="stats-list">
        {Object.entries(stats).map(([key, value], idx) => (
          <li key={idx} className="stat-item">
            <span className="stat-label">{key}</span>
            <span className="stat-value">{value}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StatsPanel;

