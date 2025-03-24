import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import requests

## loading api key from .Env
load_dotenv()

## initialising fastapi
app = FastAPI()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL= "http://api.weatherapi.com/v1/current.json"

@app.get("/")
def home():
    return {"message":"Welcome to FastAPI Weather App!"}

@app.get("/weather/{city}")
def get_weather(city: str, aqi: str = "no"):
    """
    Fetch weather details for a given city using WeatherAPI.com.
    
    :param city: Name of the city
    :param aqi: Whether to include air quality data ("yes" or "no")
    :return: Weather details as JSON
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API Key is missing!")

    url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi={aqi}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found!")

    return {
        "city": city,
        "weather": data["current"]["condition"]["text"],
        "temperature": data["current"]["temp_c"],
        "humidity": data["current"]["humidity"],
        "wind_speed": data["current"]["wind_kph"],
        "air_quality": data["current"].get("air_quality", "Not Available") if aqi == "yes" else "Not Requested"
    }

