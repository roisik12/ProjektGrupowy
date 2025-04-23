import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from './AuthProvider';

const GuestPage = () => {
  const navigate = useNavigate();
  const { logout, userEmail } = useAuth();
  const [city, setCity] = useState("");
  const [airQualityData, setAirQualityData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fetchAirQuality = async () => {
    setLoading(true);
    setError(null);
    setAirQualityData([]);

    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/air-quality/${city}`);
    
      if (response.status === 404) {
        setError("Brak danych dla tego miasta.");
      } else if (response.status === 429) {
        setError("Zbyt dużo zapytań. Spróbuj ponownie za chwilę.");
      } else if (!response.ok) {
        throw new Error("Błąd podczas pobierania danych.");
      } else {
        const data = await response.json();
        setAirQualityData(data.history);
      }
    } catch (err) {
      setError(err.message);
    }
    
    setLoading(false);
  };

  const getNameFromEmail = (email) => {
    if (!email) return "Gościu";
    const namePart = email.split("@")[0];
    return namePart.charAt(0).toUpperCase() + namePart.slice(1);
  };

  return (
    <div className="w-full min-h-screen flex flex-col items-center justify-center fade-in">
      
      {/* Powitanie + Wyloguj */}
      <div className="flex flex-col md:flex-row items-center justify-center w-full max-w-4xl mb-8 gap-4">
        <h1 className="section-header text-center">👋 Witaj, {getNameFromEmail(userEmail)}!</h1>
        <button
          className="p-3 rounded-lg bg-red-500 hover:bg-red-600 text-white transition duration-300 shadow-lg"
          onClick={handleLogout}
        >
          Wyloguj się
        </button>
      </div>

      {/* Panel do wpisania miasta */}
      <div className="card fade-in mt-2 p-6 w-full max-w-2xl text-center">
        <h2 className="section-header mb-4">Sprawdź historię jakości powietrza</h2>

        <div className="flex flex-col items-center space-y-4">
          <input
            type="text"
            className="w-full p-3 rounded-lg border border-gray-500 bg-secondary text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-highlight"
            placeholder="Wpisz nazwę miasta..."
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <button
            onClick={fetchAirQuality}
            className="w-full p-3 rounded-lg bg-highlight text-white hover:bg-blue-400 transition duration-300 shadow-lg"
            disabled={!city.trim() || loading}
          >
            {loading ? (
              <div className="flex justify-center items-center">
                <div className="w-5 h-5 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : (
              "Sprawdź"
            )}
          </button>
        </div>

        {/* Wyniki */}
        {airQualityData.length > 0 && (
          <div className="mt-8 space-y-4">
            {airQualityData.map((entry, index) => (
              <div key={index} className="bg-primary p-4 rounded-lg shadow text-left">
                <p><strong>AQI:</strong> {entry.AQI}</p>
                <p><strong>Data pomiaru:</strong> {new Date(entry.last_update).toLocaleString()}</p>
              </div>
            ))}
          </div>
        )}

        {/* Komunikat o błędzie */}
        {error && (
          <div className="mt-6 text-center text-red-400 font-semibold">
            {error}
          </div>
        )}
      </div>

    </div>
  );
};

export default GuestPage;
