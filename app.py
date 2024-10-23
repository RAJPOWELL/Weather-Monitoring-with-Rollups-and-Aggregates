from flask import Flask, jsonify, render_template
import requests
import time
import threading
from datetime import datetime

app = Flask(__name__)

API_KEY = 'ee1d1fe79609640e074c7fb90fe20d72'  # Replace with your OpenWeatherMap API key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
weather_data = {}

# Mapping OpenWeatherMap weather conditions to FontAwesome icons
WEATHER_ICONS = {
    'Clear': 'fa-sun',
    'Clouds': 'fa-cloud',
    'Rain': 'fa-cloud-showers-heavy',
    'Drizzle': 'fa-cloud-rain',
    'Thunderstorm': 'fa-bolt',
    'Snow': 'fa-snowflake',
    'Mist': 'fa-smog',
    'Smoke': 'fa-smog',
    'Haze': 'fa-smog',
    'Dust': 'fa-smog',
    'Fog': 'fa-smog',
}

def fetch_weather_data():
    global weather_data
    with app.app_context():  # Create application context for this thread
        for city in CITIES:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}")
            data = response.json()
            if response.status_code == 200:
                main = data['weather'][0]['main']
                icon_class = WEATHER_ICONS.get(main, 'fa-question-circle')  # Default icon if condition not found
                temp = data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
                feels_like = data['main']['feels_like'] - 273.15  # Convert Kelvin to Celsius
                humidity = data['main']['humidity']  # Get humidity
                wind_speed = data['wind']['speed']  # Get wind speed
                pressure = data['main']['pressure']  # Get pressure
                visibility = data['visibility'] / 1000  # Convert visibility from meters to kilometers
                dt = data['dt']
                weather_data[city] = {
                    'main': main,
                    'main_icon': icon_class,  # Use FontAwesome class for the icon
                    'temp': temp,
                    'feels_like': feels_like,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'pressure': pressure,
                    'visibility': visibility,
                    'dt': dt
                }
            else:
                print(f"Error fetching data for {city}: {data.get('message', 'Unknown error')}")

@app.route('/api/fetch_weather')
def fetch_weather():
    fetch_weather_data()  # Fetch weather data when the endpoint is hit
    return jsonify(weather_data)

@app.route('/')
def index():
    return render_template('index.html', weather_data=weather_data)

@app.route('/api/weather_summary')
def weather_summary():
    return jsonify(weather_data)

@app.template_filter('to_datetime')
def to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # Start the background thread to fetch weather data every 5 minutes
    threading.Thread(target=fetch_weather_data, daemon=True).start()
    app.run(debug=False)
