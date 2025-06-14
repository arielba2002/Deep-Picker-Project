import React, { useEffect, useState } from "react";

// Utility to get color based on percentage ranges
function getColor(value, max) {
  const percent = (value / max) * 100;
  
  if (percent <= 40) {
    return "#e74c3c"; // Red for 0-40%
  } else if (percent <= 70) {
    return "#f1c40f"; // Yellow for 41-70%
  } else {
    return "#2ecc71"; // Green for 71-100%
  }
}

export default function CircleProgressBar({ value, max = 100, size = 140, strokeWidth = 14 }) {
  const [animatedValue, setAnimatedValue] = useState(0);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.max(0, Math.min(value, max));
  const offset = circumference - (animatedValue / max) * circumference;
  const color = getColor(progress, max);

  useEffect(() => {
    // Reset animation when value changes
    setAnimatedValue(0);
    const timer = setTimeout(() => {
      setAnimatedValue(progress);
    }, 50);

    return () => clearTimeout(timer);
  }, [progress]);

  return (
    <div style={{ 
      display: 'flex', 
      flex: 1, 
      justifyContent: 'center', 
      alignItems: 'center',
      padding: '24px'
    }}>
      <svg width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#d6d6d6"
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
          style={{ 
            transition: "stroke-dashoffset 500ms ease-out",
            transform: "rotate(-90deg)",
            transformOrigin: "center"
          }}
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dominantBaseline="central"
          fontSize={size * 0.28}
          fontWeight="800"
          fill={color}
          style={{ 
            pointerEvents: 'none', 
            userSelect: 'none',
            filter: "drop-shadow(0px 1px 2px rgba(0,0,0,0.1))"
          }}
        >
          {progress}
        </text>
      </svg>
    </div>
  );
}
