import requests
from datetime import datetime
from models import WeatherSummary, db

API_KEY = ''
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def fetch_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(WEATHER_API_URL, params=params)
    return response.json()

def process_daily_weather(city):
    # Aggregate weather data (sample for average/min/max temperature)
    temps = [fetch_weather(city)['main']['temp'] for _ in range(5)]  # Example data from last 5 records
    avg_temp = sum(temps) / len(temps)
    max_temp = max(temps)
    min_temp = min(temps)
    dominant_condition = fetch_weather(city)['weather'][0]['main']
    
    # Save to DB
    summary = WeatherSummary(city=city, avg_temp=avg_temp, max_temp=max_temp, min_temp=min_temp, dominant_condition=dominant_condition)
    db.session.add(summary)
    db.session.commit()
    
    return {
        'city': city,
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'dominant_condition': dominant_condition
    }

def check_thresholds(city, temp, threshold=35):
    if temp > threshold:
        print(f'ALERT: {city} temperature {temp}C exceeds threshold of {threshold}C!')
