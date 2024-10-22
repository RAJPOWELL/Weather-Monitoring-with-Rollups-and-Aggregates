from flask import Flask, render_template, jsonify
from weather_service import fetch_weather, process_daily_weather, check_thresholds
from models import db, WeatherSummary

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/<city>')
def get_city_weather(city):
    # Fetch the weather for the specified city
    weather_data = fetch_weather(city)
    return jsonify(weather_data)

@app.route('/daily-summary/<city>')
def daily_summary(city):
    # Generate daily weather summary
    summary = process_daily_weather(city)
    return jsonify(summary)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
    app.run(debug=False)
