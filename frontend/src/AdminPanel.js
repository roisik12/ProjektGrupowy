import React, { useState, useEffect } from "react";
import { useNavigate, Navigate } from "react-router-dom";
import { useAuth } from './AuthProvider';
import TestPanel from "./TestPanel";
import { getToken } from "./firebase";

const AdminPanel = () => {
  const [users, setUsers] = useState([]);
  const [city, setCity] = useState("");
  const [aqi, setAqi] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate();
  const { token, userRole, logout } = useAuth();

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch("http://localhost:8001/admin/users", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          const data = await res.json();
          setUsers(data);
        } else if (res.status === 401 || res.status === 403) {
          logout();
          navigate('/login');
        }
      } catch (error) {
        console.error('Failed to fetch users:', error);
      }
    };

    if (token && userRole === 'admin') {
      fetchUsers();
    }
  }, [token, userRole, navigate, logout]);

  if (userRole !== 'admin') {
    return <Navigate to="/unauthorized" />;
  }

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleSubmit = async () => {
    setMessage("");
    setError("");

    try {
      const idToken = await getToken();
      const response = await fetch(`http://localhost:8001/air-quality/${encodeURIComponent(city)}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${idToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          AQI: parseInt(aqi, 10),
          last_update: new Date().toISOString(),
        }),
      });

      if (!response.ok) {
        throw new Error('Błąd podczas zapisu danych');
      }

      const data = await response.json();
      setMessage(data.message);
      setCity("");
      setAqi("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4 sm:p-6 animate-fade-in">
      
      {/* Nagłówek */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-highlight">
          Panel administratora
        </h1>
        <button
          className="text-sm sm:text-base bg-danger hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-300"
          onClick={handleLogout}
        >
          Wyloguj się
        </button>
      </div>

      {/* Lista użytkowników */}
      <div className="bg-secondary p-4 sm:p-6 rounded-lg shadow-custom mb-6 animate-slide-in-up">
        <h2 className="text-xl sm:text-2xl font-semibold text-highlight mb-4">
          Użytkownicy
        </h2>
        {users.length > 0 ? (
          <ul className="space-y-2">
            {users.map((user) => (
              <li key={user.uid} className="text-white text-sm sm:text-base">
                {user.email} - {user.role}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400 text-sm">Brak użytkowników</p>
        )}
      </div>

      {/* Panel testowy */}
      <div className="bg-secondary p-4 sm:p-6 rounded-lg shadow-custom animate-fade-in mb-6">
        <TestPanel />
      </div>

      {/* Formularz dodawania danych AQI */}
      <div className="bg-secondary p-4 sm:p-6 rounded-lg shadow-custom animate-fade-in">
        <h2 className="text-xl sm:text-2xl font-semibold text-highlight mb-4">
          Dodaj dane jakości powietrza
        </h2>

        <div className="flex flex-col items-center space-y-4">
          <input
            type="text"
            className="w-full p-3 rounded-lg border border-gray-500 bg-primary text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-highlight"
            placeholder="Wpisz miasto"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <input
            type="number"
            className="w-full p-3 rounded-lg border border-gray-500 bg-primary text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-highlight"
            placeholder="Wpisz AQI (np. 85)"
            value={aqi}
            onChange={(e) => setAqi(e.target.value)}
          />

          <button
            onClick={handleSubmit}
            className="w-full p-3 rounded-lg bg-highlight text-white hover:bg-blue-400 transition duration-300 shadow-lg"
            disabled={!city.trim() || !aqi.trim()}
          >
            Dodaj dane
          </button>

          {/* Komunikat */}
          {message && (
            <div className="text-green-400 font-semibold">{message}</div>
          )}
          {error && (
            <div className="text-red-400 font-semibold">{error}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;
