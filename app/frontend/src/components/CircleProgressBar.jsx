import React from "react";

// Utility to interpolate color from red (0) to green (max)
function getColor(value, max) {
  const percent = Math.max(0, Math.min(1, value / max));
  // Red to yellow to green
  const r = percent < 0.5 ? 255 : Math.round(255 - (percent - 0.5) * 2 * 255);
  const g = percent < 0.5 ? Math.round(percent * 2 * 255) : 255;
  return `rgb(${r},${g},0)`;
}

export default function CircleProgressBar({ value, max = 100, size = 140, strokeWidth = 14 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.max(0, Math.min(value, max));
  const offset = circumference - (progress / max) * circumference;
  const color = getColor(progress, max);

  return (
    <svg width={size} height={size}>
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        stroke="#eee"
        strokeWidth={strokeWidth}
        fill="none"
      />
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        stroke={color}
        strokeWidth={strokeWidth}
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        style={{ transition: "stroke-dashoffset 0.7s, stroke 0.7s" }}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        dominantBaseline="central"
        fontSize={size * 0.28}
        fontWeight="bold"
        fill={color}
        style={{ pointerEvents: 'none', userSelect: 'none' }}
      >
        {progress}
      </text>
    </svg>
  );
}
