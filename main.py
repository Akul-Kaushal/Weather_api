import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import requests

from fastapi.middleware.cors import CORSMiddleware




## loading api key from .Env
load_dotenv()

## initialising fastapi
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change to ["http://localhost:5173"] for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL= "http://api.weatherapi.com/v1/current.json"

@app.get("/")
def home():
    return {"message":"Welcome to FastAPI Weather App!"}

@app.get("/weather")
def get_weather(city: str, aqi: str = "no"):
    """
    Fetches weather details for a given city using WeatherAPI.com.

    :param city: Name of the city
    :param aqi: Whether to include air quality data ("yes" or "no")
    :return: Weather details as JSON
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key is missing!")

    # Correct API request format
    weather_url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi={aqi}"
    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    weather_data = weather_response.json()

    return {
        "city": city,
        "weather": weather_data["current"]["condition"]["text"],
        "temperature": weather_data["current"]["temp_c"],
        "humidity": weather_data["current"]["humidity"],
        "wind_speed": weather_data["current"]["wind_kph"],
        "air_quality": weather_data["current"].get("air_quality", "Not Available") if aqi == "yes" else "Not Requested"
    }


# @app.get("/weather/{city}")
# def get_weather(city: str, aqi: str = "no"):
#     """
#     Fetch weather details for a given city using WeatherAPI.com.
    
#     :param city: Name of the city
#     :param aqi: Whether to include air quality data ("yes" or "no")
#     :return: Weather details as JSON
#     """
#     if not API_KEY:
#         raise HTTPException(status_code=500, detail="API Key is missing!")

#     url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi={aqi}"
#     response = requests.get(url)
#     data = response.json()

#     if response.status_code != 200:
#         raise HTTPException(status_code=404, detail="City not found!")

#     return {
#         "city": city,
#         "weather": data["current"]["condition"]["text"],
#         "temperature": data["current"]["temp_c"],
#         "humidity": data["current"]["humidity"],
#         "wind_speed": data["current"]["wind_kph"],
#         "air_quality": data["current"].get("air_quality", "Not Available") if aqi == "yes" else "Not Requested"
#     }

