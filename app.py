from flask import Flask, jsonify, render_template
import requests
import time
import threading
from datetime import datetime
import sqlite3

app = Flask(__name__)

API_KEY = 'ee1d1fe79609640e074c7fb90fe20d72'  # Replace with your OpenWeatherMap API key
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
weather_data = {}

# User-configurable alert thresholds
ALERT_THRESHOLDS = {
    "temperature": 25,  # Celsius
    "condition": "Rain"  # Example condition for alerts
}

# List to store alerts
alerts = []

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

# Database initialization
def init_db():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_weather (
                date TEXT PRIMARY KEY,
                avg_temp REAL,
                max_temp REAL,
                min_temp REAL,
                dominant_condition TEXT
            )
        ''')
        conn.commit()

def fetch_weather_data():
    global weather_data, alerts
    with app.app_context():  # Create application context for this thread
        today = datetime.now().date()
        daily_records = []

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

                # Check for alerts based on thresholds
                check_alerts(city, temp, main)

                # Store today's weather data for aggregation
                daily_records.append({
                    'temp': temp,
                    'main': main,
                    'city': city,
                    'dt': dt
                })

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

        # Calculate daily aggregates and store in database
        if daily_records:
            calculate_daily_aggregates(today, daily_records)

def check_alerts(city, temp, main_condition):
    global alerts
    # Check if temperature exceeds threshold
    if temp > ALERT_THRESHOLDS["temperature"]:
        alerts.append(f"Alert! Temperature in {city} exceeds {ALERT_THRESHOLDS['temperature']}°C: Current Temperature: {temp:.2f}°C.")
    
    # Check if the main weather condition matches the alert condition
    if main_condition == ALERT_THRESHOLDS["condition"]:
        alerts.append(f"Alert! Current weather in {city} is '{main_condition}'.")

def calculate_daily_aggregates(today, records):
    temps = [record['temp'] for record in records]
    conditions = [record['main'] for record in records]

    avg_temp = sum(temps) / len(temps) if temps else 0
    max_temp = max(temps) if temps else 0
    min_temp = min(temps) if temps else 0

    # Determine the dominant condition
    dominant_condition = max(set(conditions), key=conditions.count)

    # Store in the database
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO daily_weather (date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?)
        ''', (today.isoformat(), avg_temp, max_temp, min_temp, dominant_condition))
        conn.commit()

@app.route('/api/fetch_weather')
def fetch_weather():
    fetch_weather_data()  # Fetch weather data when the endpoint is hit
    return jsonify(weather_data)

@app.route('/')
def index():
    return render_template('index.html', weather_data=weather_data, alerts=alerts)

@app.route('/api/weather_summary')
def weather_summary():
    return jsonify(weather_data)

@app.route('/api/daily_summary')
def daily_summary():
    with sqlite3.connect('weather.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM daily_weather')
        summaries = cursor.fetchall()

    # Format summaries for JSON response
    summary_list = []
    for date, avg_temp, max_temp, min_temp, dominant_condition in summaries:
        summary_list.append({
            'date': date,
            'avg_temp': avg_temp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'dominant_condition': dominant_condition
        })

    return jsonify(summary_list)

@app.template_filter('to_datetime')
def to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # Initialize database
    init_db()

    # Start the background thread to fetch weather data every 5 minutes
    threading.Thread(target=fetch_weather_data, daemon=True).start()
    
    # Change the host to '0.0.0.0' to allow external access
    app.run(host='0.0.0.0', port=5000, debug=False)

