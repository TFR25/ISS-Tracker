import requests
from datetime import datetime

api_data = requests.get(url="http://api.open-notify.org/iss-now.json")
api_data.raise_for_status()
data = api_data.json()


def get_iss_data():
    """get ISS latitude and longitude position"""
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude


def get_path_time():
    """get current time"""
    now = datetime.now()
    iss_path_date = now.strftime("%m-%d-%y")
    iss_path_time = now.strftime("%H:%M:%S")
    return iss_path_date, iss_path_time
