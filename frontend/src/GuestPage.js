import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from './AuthProvider';
import { FaChevronDown, FaChevronUp, FaTrash } from 'react-icons/fa';
import { MdAir } from 'react-icons/md';

const getAQILevel = (aqi) => {
  if (aqi <= 50) return { color: 'text-green-400', label: 'Good' };
  if (aqi <= 100) return { color: 'text-yellow-400', label: 'Moderate' };
  if (aqi <= 150) return { color: 'text-orange-400', label: 'Unhealthy for Sensitive Groups' };
  if (aqi <= 200) return { color: 'text-red-400', label: 'Unhealthy' };
  return { color: 'text-purple-400', label: 'Very Unhealthy' };
};

const CityCard = ({ cityData, onUntrack, authToken }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const latestAQI = cityData.history?.[0]?.AQI;
  const aqiInfo = getAQILevel(latestAQI);

  // Add getPMValue helper function
  const getPMValue = (entry, type) => {
    if (!entry.raw_data || !entry.raw_data[type]) return 'N/A';
    return `${entry.raw_data[type]} μg/m³`;
  };

  // Add prediction function
  const getPrediction = async () => {
    try {
      setIsPredicting(true);
      const response = await fetch(
        `${process.env.REACT_APP_API_BASE_URL}/prediction/predict/${cityData.city}`, // Updated path
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            history: cityData.history.slice(0, 5).map(entry => entry.AQI)
          })
        }
      );

      if (!response.ok) throw new Error('Failed to get prediction');
      
      const data = await response.json();
      setPrediction(data.predicted_aqi);
    } catch (err) {
      console.error('Prediction error:', err);
    } finally {
      setIsPredicting(false);
    }
  };

  return (
    <div className="bg-secondary rounded-lg shadow-custom overflow-hidden">
      <div 
        onClick={() => setIsExpanded(!isExpanded)}
        className="p-4 cursor-pointer hover:bg-opacity-80 transition-all duration-300 flex justify-between items-center"
      >
        <div className="flex items-center gap-3">
          <MdAir className={`text-2xl ${aqiInfo.color}`} />
          <div>
            <h3 className="text-xl font-semibold text-highlight">{cityData.city}</h3>
            <div className="flex items-center gap-2">
              {latestAQI && (
                <p className={`text-sm ${aqiInfo.color}`}>
                  AQI: {latestAQI} - {aqiInfo.label}
                </p>
              )}
              {prediction && (
                <p className={`text-sm ${getAQILevel(prediction).color}`}>
                  • Predicted: {prediction}
                </p>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={(e) => {
              e.stopPropagation();
              getPrediction();
            }}
            disabled={isPredicting || cityData.history.length < 5}
            className="text-highlight hover:text-blue-400 transition p-2 disabled:opacity-50"
            title={cityData.history.length < 5 ? "Need at least 5 measurements for prediction" : "Get prediction"}
          >
            {isPredicting ? "..." : "🔮"}
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onUntrack(cityData.city);
            }}
            className="text-danger hover:text-red-700 transition p-2"
          >
            <FaTrash />
          </button>
          {isExpanded ? <FaChevronUp /> : <FaChevronDown />}
        </div>
      </div>

      {/* Expandable content */}
      <div 
        className={`overflow-hidden transition-all duration-300 ${
          isExpanded ? 'max-h-100' : 'max-h-0'
        }`}
      >
        <div className="p-4 border-t border-gray-700">
          <div className="space-y-3">
            {cityData.history?.map((entry, index) => (
              <div key={index} 
                className="bg-primary p-3 rounded-lg flex items-center justify-between hover:bg-opacity-80 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-full rounded-full ${getAQILevel(entry.AQI).color}`} />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className={`text-lg font-bold ${getAQILevel(entry.AQI).color}`}>
                        {entry.AQI}
                      </span>
                      <span className="text-xs text-gray-400">
                        {getAQILevel(entry.AQI).label}
                      </span>
                    </div>
                    <div className="text-xs text-gray-400">
                      PM2.5: {getPMValue(entry, 'pm2_5')} • PM10: {getPMValue(entry, 'pm10')}
                    </div>
                  </div>
                </div>
                <span className="text-sm text-gray-400">
                  {new Date(entry.last_update).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const GuestPage = () => {
  const navigate = useNavigate();
  const { logout, userEmail, token } = useAuth();
  const [city, setCity] = useState("");
  const [trackedCities, setTrackedCities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    fetchTrackedCities();
    // Auto-refresh data every 5 minutes
    const interval = setInterval(fetchTrackedCities, 300000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fetchTrackedCities = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/tracked-cities`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      if (!response.ok) throw new Error('Failed to fetch tracked cities');
      
      const data = await response.json();
      setTrackedCities(data.tracked_cities || []);
    } catch (err) {
      setError("Error fetching tracked cities");
      console.error(err);
    }
  };

  const trackCity = async (cityName) => {
    try {
      setLoading(true);
      setError(null);
      setSuccessMessage("");

      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/tracked-cities/${cityName}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to track city');
      }

      await fetchTrackedCities();
      setCity("");
      setSuccessMessage(`Now tracking ${cityName}`);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      setError(err.message);
      setTimeout(() => setError(null), 3000);
    } finally {
      setLoading(false);
    }
  };

  const untrackCity = async (cityName) => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/user/tracked-cities/${cityName}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!response.ok) throw new Error('Failed to untrack city');

      await fetchTrackedCities(); // Refresh the list
    } catch (err) {
      setError("Error untracking city");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto min-h-screen p-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-highlight">
          Air Quality Monitor
        </h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400">Updates every 6 hours</span>
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-400">{userEmail}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-danger hover:bg-red-700 text-white rounded-lg transition duration-300"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Add city form */}
      <div className="bg-secondary p-6 rounded-lg shadow-custom mb-8">
        <form onSubmit={(e) => {
          e.preventDefault();
          if (city.trim()) trackCity(city);
        }} className="flex gap-4">
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Enter city name to track air quality..."
            className="flex-1 p-3 rounded-lg bg-primary text-white border border-gray-600 focus:outline-none focus:border-highlight"
          />
          <button
            type="submit"
            disabled={!city.trim() || loading}
            className="px-6 py-2 bg-highlight hover:bg-blue-600 text-white rounded-lg transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "..." : "Track City"}
          </button>
        </form>
      </div>

      {/* Tracked cities list */}
      <div className="space-y-4">
        {trackedCities.map((cityData) => (
          <CityCard 
            key={cityData.city}
            cityData={cityData}
            onUntrack={untrackCity}
            authToken={token}
          />
        ))}
      </div>

      {/* Messages */}
      {successMessage && (
        <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in">
          {successMessage}
        </div>
      )}
      {error && (
        <div className="fixed bottom-4 right-4 bg-danger text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in">
          {error}
        </div>
      )}
    </div>
  );
};

export default GuestPage;
