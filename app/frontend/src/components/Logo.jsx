import React from "react";
import logo from "../assets/logo.png";

export default function Logo({ size = 38, style = {} }) {
  return (
    <img
      src={logo}
      alt="Logo"
      style={{
        height: size,
        width: "auto",
        display: "block",
        borderRadius: 8,
        ...style,
      }}
    />
  );
}
