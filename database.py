import sqlite3

def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY,
            city TEXT NOT NULL,
            date TEXT NOT NULL,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_daily_summary(city, date, avg_temp, max_temp, min_temp, dominant_condition, reason):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (city, date, avg_temp, max_temp, min_temp, dominant_condition, reason))
    conn.commit()
    conn.close()

def get_daily_summaries():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM daily_summary')
    summaries = cursor.fetchall()
    conn.close()
    return summaries
