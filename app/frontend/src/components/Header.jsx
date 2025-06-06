import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "./Logo";

// Decode JWT payload (naive base64 method)
function getUserFromToken() {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.name || payload.sub || payload.email.split("@")[0] || "User";
  } catch {
    return null;
  }
}

export default function Header() {
  const navigate = useNavigate();
  const username = getUserFromToken();
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef(null);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/signin");
  };

  // Close dropdown on outside click
  useEffect(() => {
    function onOutsideClick(e) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    }
    if (open) document.addEventListener("mousedown", onOutsideClick);
    return () => document.removeEventListener("mousedown", onOutsideClick);
  }, [open]);

  if (!username) return null;

  return (
    <header className="header">
      <a className="header-left" href="/" aria-label="Home">
        <Logo size={80} />
        <span className="brand">Deep Picker</span>
      </a>
      <div className="user-section" ref={dropdownRef}>
        <button
          className="user-greeting user-dropdown-toggle"
          onClick={() => setOpen((o) => !o)}
          aria-haspopup="true"
          aria-expanded={open}
          tabIndex={0}
          onKeyDown={e => {
            if (e.key === "Enter" || e.key === " ") setOpen(o => !o);
            if (e.key === "Escape") setOpen(false);
          }}
        >
          <span className="user-name">Profile</span>
          <span className="dropdown-arrow">▾</span>
        </button>

        {open && (
          <nav
            className="user-dropdown professional-dropdown"
            role="menu"
            tabIndex={-1}
            aria-label="User menu"
            style={{ right: 0, left: "auto", maxWidth: "calc(100vw - 24px)" }}
            onKeyDown={e => {
              if (e.key === "Escape") setOpen(false);
            }}
          >
            <div className="dropdown-caret" aria-hidden="true" />
            <ul>
              <li className="dropdown-user-row" role="menuitem">
                <span className="dropdown-username">Hi, {username}</span>
              </li>
              <li>
                <div className="dropdown-divider" />
              </li>
              <li role="menuitem">
                <button className="logout-btn" onClick={handleLogout}>
                  Logout
                </button>
              </li>
            </ul>
          </nav>
        )}
      </div>
    </header>
  );
}
