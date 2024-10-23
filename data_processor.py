from datetime import datetime

# Process daily summaries, aggregates like min, max, avg temp
def process_daily_summary(weather_data, city):
    daily_data = [entry for entry in weather_data[city] if is_today(entry['dt'])]
    
    if not daily_data:
        return {}
    
    temps = [entry['temp'] for entry in daily_data]
    
    summary = {
        'city': city,
        'average_temp': sum(temps) / len(temps),
        'max_temp': max(temps),
        'min_temp': min(temps),
        'dominant_condition': find_dominant_condition(daily_data)
    }
    
    return summary

def is_today(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.date() == datetime.utcnow().date()

# Calculate the dominant weather condition
def find_dominant_condition(daily_data):
    conditions = {}
    for entry in daily_data:
        condition = entry['main']
        if condition not in conditions:
            conditions[condition] = 0
        conditions[condition] += 1
    
    return max(conditions, key=conditions.get)
