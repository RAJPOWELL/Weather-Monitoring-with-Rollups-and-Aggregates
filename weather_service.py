import requests
from config import API_KEY, BASE_URL

# Convert Kelvin to Celsius
def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

# Fetch weather data from OpenWeather API
def fetch_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    return {
        'city': city,
        'main': data['weather'][0]['main'],
        'temp': kelvin_to_celsius(data['main']['temp']),
        'feels_like': kelvin_to_celsius(data['main']['feels_like']),
        'dt': data['dt']  # Unix timestamp
    }
