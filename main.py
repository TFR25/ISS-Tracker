import csv
import plotly.express as px
import pandas
import requests
from datetime import datetime
import json

api_data = requests.get(url="http://api.open-notify.org/iss-now.json")
api_data.raise_for_status()
data = api_data.json()


def view_point_location():
    with open("data.json") as file:
        view_point_position = json.load(file)
        # replace view_point_lat and view_point_lng with your latitude and longitude. Utilize this website to find your
        # latitude and longitude https://www.latlong.net
        view_point_lat = view_point_position["my_location"]["lat"]
        view_point_lng = view_point_position["my_location"]["lng"]
        return view_point_lat, view_point_lng


view_lat, view_lng = view_point_location()


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


def path_time_history():
    """save ISS position date and time history to csv file for mapping"""
    with open("iss_data_path_history.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        latitude, longitude = get_iss_data()
        date, time = get_path_time()
        iss_data = [latitude, longitude, date, time, view_lat, view_lng]
        writer.writerow(iss_data)


path_time_history()


def plotter():
    df = pandas.read_csv("iss_data_path_history.csv")
    figure = px.scatter_geo(df, lat="latitude", lon="longitude")
    figure.update_layout(title="World Map", title_x=0.5)
    figure.add_scattergeo(lat=df["view_point_lat"], lon=df["view_point_lng"],
                          mode='markers', marker=dict(size=18, symbol="star", color="red"))
    figure.show()


plotter()
