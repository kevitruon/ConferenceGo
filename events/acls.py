from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/v1/search?query={city} {state}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if "photos" in data:
        photos = data["photos"]
        if photos:
            picture_url = photos[0]["url"]
            return {"picture_url": picture_url}
    return {}


def get_weather_data(city, state):
    # Create the URL for the geocoding API with the city and state
    geocoding_url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={OPEN_WEATHER_API_KEY}"

    # Make the request to the geocoding API
    geocoding_response = requests.get(geocoding_url)

    # Parse the JSON response from the geocoding API
    geocoding_data = geocoding_response.json()
    if "coord" not in geocoding_data:
        return None

    # Get the latitude and longitude from the geocoding response
    latitude = geocoding_data["coord"]["lat"]
    longitude = geocoding_data["coord"]["lon"]

    # Create the URL for the current weather API with the latitude and longitude
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}"

    # Make the request to the current weather API
    weather_response = requests.get(weather_url)

    # Parse the JSON response from the current weather API
    weather_data = weather_response.json()

    # Get the main temperature and the weather's description and put them in a dictionary
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    weather_dict = {"temperature": temperature, "description": description}

    # Return the dictionary
    return weather_dict
