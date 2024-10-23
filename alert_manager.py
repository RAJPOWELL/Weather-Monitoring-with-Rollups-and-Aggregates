from config import ALERT_THRESHOLD_TEMP, EMAIL_RECIPIENT

# Check if any alerts should be triggered
def check_alerts(data):
    alerts = []
    if data['temp'] > ALERT_THRESHOLD_TEMP:
        alerts.append(f"Temperature exceeded threshold in {data['city']}: {data['temp']}°C")
    
    return alerts

# Send alerts to users via email or console
def alert_users(alerts):
    for alert in alerts:
        print(f"ALERT: {alert}")
        send_email(alert)

# Send email (dummy function for now)
def send_email(alert):
    print(f"Sending email to {EMAIL_RECIPIENT}: {alert}")
