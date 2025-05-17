import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function RequireAuth({ children }) {
  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/signin");
    }
  }, [navigate]);
  return children;
}
