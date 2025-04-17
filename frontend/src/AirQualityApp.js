import { useState, useEffect } from "react";

export default function AirQualityApp() {
  const [airQuality, setAirQuality] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Symulacja pobierania danych o jakości powietrza
    setTimeout(() => {
      setAirQuality({
        city: "Warszawa",
        aqi: 42,
        status: "Dobra",
      });
      setLoading(false);
    }, 1500);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-primary text-white p-6 animate-fade-in">
      <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-highlight mb-2">
        Jakość Powietrza
      </h1>
      <p className="text-gray-400 mb-6">{new Date().toLocaleDateString()}</p>

      {loading ? (
        <p className="text-gray-400 animate-pulse text-sm sm:text-base">
          Ładowanie danych...
        </p>
      ) : (
        <div className="bg-secondary p-4 sm:p-6 rounded-lg shadow-custom w-72 sm:w-80 text-center animate-slide-in-up">
          <h2 className="text-lg sm:text-xl font-semibold text-highlight">{airQuality.city}</h2>
          <p className="text-3xl sm:text-4xl font-bold text-green-400 mt-2">{airQuality.aqi}</p>
          <p className="text-base sm:text-lg text-gray-300 mt-2">{airQuality.status}</p>
        </div>
      )}
    </div>
  );
}
