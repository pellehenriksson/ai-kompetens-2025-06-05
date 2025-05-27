# create file of masters winners
import os
import re
import json

import pandas as pd
import httpx

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") # load the api key from another file (.env)

def clean_name(s: str) -> str:
    return re.sub(r"\s*\([^)]*\)", "", s)

def create_winners_file() -> None:

    df = pd.read_html("https://sv.wikipedia.org/wiki/The_Masters_Tournament")[1]
    df.columns = ["year", "winner", "country", "score", "margin"]

    df["winner"] = df["winner"].apply(clean_name)

    df.to_csv("data/masters-winners.csv", columns=["year", "winner", "country"], index=False)


def get_current_temperature(latitude: str, longitude: str) -> dict:

    url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={API_KEY}&location.latitude={latitude}&location.longitude={longitude}"
    response = httpx.get(url)
    result = json.loads(response.text)

    return result

def get_location_coordinates(location: str) -> dict:
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"

    response = httpx.get(url)
    result = json.loads(response.text)
    location = result["results"][0]["geometry"]["location"]

    return {"latitude": location["lat"], "longitude": location["lng"]}

if __name__ == "__main__":
    location = get_location_coordinates("amsterdam")
    temp = get_current_temperature(**location)

    print(temp)

    """
    {'currentTime': '2025-05-27T15:39:41.098141936Z', 'timeZone': {'id': 'Europe/Amsterdam'}, 'isDaytime': True, 'weatherCondition': {'iconBaseUri': 'https://maps.gstatic.com/weather/v1/drizzle', 'description': {'text': 'Light rain', 'languageCode': 'en'}, 'type': 'LIGHT_RAIN'}, 'temperature': {'degrees': 13.4, 'unit': 'CELSIUS'}, 'feelsLikeTemperature': {'degrees': 12.3, 'unit': 'CELSIUS'}, 'dewPoint': {'degrees': 11.1, 'unit': 'CELSIUS'}, 'heatIndex': {'degrees': 13.4, 'unit': 'CELSIUS'}, 'windChill': {'degrees': 12.3, 'unit': 'CELSIUS'}, 'relativeHumidity': 87, 'uvIndex': 1, 'precipitation': {'probability': {'percent': 92, 'type': 'RAIN'}, 'snowQpf': {'quantity': 0, 'unit': 'MILLIMETERS'}, 'qpf': {'quantity': 0.0203, 'unit': 'MILLIMETERS'}}, 'thunderstormProbability': 10, 'airPressure': {'meanSeaLevelMillibars': 1011.83}, 'wind': {'direction': {'degrees': 220, 'cardinal': 'SOUTHWEST'}, 'speed': {'value': 14, 'unit': 'KILOMETERS_PER_HOUR'}, 'gust': {'value': 27, 'unit': 'KILOMETERS_PER_HOUR'}}, 'visibility': {'distance': 13, 'unit': 'KILOMETERS'}, 'cloudCover': 100, 'currentConditionsHistory': {'temperatureChange': {'degrees': -4.2, 'unit': 'CELSIUS'}, 'maxTemperature': {'degrees': 17.7, 'unit': 'CELSIUS'}, 'minTemperature': {'degrees': 12.8, 'unit': 'CELSIUS'}, 'snowQpf': {'quantity': 0, 'unit': 'MILLIMETERS'}, 'qpf': {'quantity': 3.1065, 'unit': 'MILLIMETERS'}}}
    """