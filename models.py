from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    avg_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)
    min_temp = db.Column(db.Float, nullable=False)
    dominant_condition = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
