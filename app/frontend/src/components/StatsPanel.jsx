// src/components/StatsPanel.jsx
import React from "react";
import "./StatsPanel.css";

function StatsPanel({ stats }) {
  return (
    <div className="stats-panel-container">
      <h2>Lineup & Bench Stats</h2>
      <ul className="stats-list">
        {stats.map((stat, idx) => (
          <li key={idx} className="stat-item">
            <span className="stat-label">{stat.label}</span>
            <span className="stat-value">{stat.value}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StatsPanel;

