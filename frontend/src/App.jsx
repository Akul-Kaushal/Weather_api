import { useState } from "react";
import axios from "axios";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aqi, setAqi] = useState(false);

  const fetchWeather = async () => {
    setLoading(true);
    setError(null);
    setWeather(null);

    try {
      const response = await axios.get("http://127.0.0.1:8000/weather", {
        params: { city, aqi: aqi ? "yes" : "no" },
      });

      setWeather(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to fetch data");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-4xl font-bold mb-4 flex items-center">🌦 Weather App</h1>

      <div className="flex space-x-2 mb-4">
        <input
          type="text"
          placeholder="Enter city..."
          className="px-4 py-2 rounded-lg bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />
        <button
          className="bg-blue-600 px-6 py-2 rounded-lg hover:bg-blue-500 transition"
          onClick={fetchWeather}
          disabled={loading}
        >
          {loading ? "Loading..." : "Get Weather"}
        </button>
      </div>

      <label className="flex items-center space-x-2">
        <input
          type="checkbox"
          checked={aqi}
          onChange={() => setAqi(!aqi)}
          className="form-checkbox h-5 w-5 text-blue-500"
        />
        <span>Include AQI</span>
      </label>

      {error && <p className="text-red-500 mt-4">{error}</p>}

      {weather && (
        <div className="mt-6 bg-gray-800 p-6 rounded-lg shadow-lg text-center">
          <h2 className="text-2xl font-semibold">{weather.city}</h2>
          <p className="text-lg">{weather.weather}</p>
          <p>🌡 Temp: {weather.temperature}°C</p>
          <p>💧 Humidity: {weather.humidity}%</p>
          <p>💨 Wind: {weather.wind_speed} kph</p>

          {aqi && weather.air_quality !== "Not Requested" && (
            <div className="mt-4">
              <h3 className="text-xl font-semibold">AQI Data</h3>
              <p>CO: {weather.air_quality.co}</p>
              <p>NO₂: {weather.air_quality.no2}</p>
              <p>O₃: {weather.air_quality.o3}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
