import csv
import plotly.express as px
import pandas
import requests
from datetime import datetime
import json
from haversine import haversine
import smtplib
import time


def get_sunrise_sunset():
    with open("data.json") as file:
        private_data = json.load(file)
        sun_api_parameters = {
            "lat": private_data["my_location"]["lat"],
            "lng": private_data["my_location"]["lng"],
            "tzid": private_data["my_location"]["tzid"],
            "formatted": 0
        }
    sunset_sunrise_api_data = requests.get("https://api.sunrise-sunset.org/json", params=sun_api_parameters)
    sunset_sunrise_api_data.raise_for_status()
    sun_data = sunset_sunrise_api_data.json()
    with open("sunset_sunrise_api_data.json", "w") as outfile:
        json.dump(sun_data, outfile)
    sunset_sunrise = sunset_sunrise_api_data.json()
    """Extract sunrise and sunset hours"""
    sunrise = int(sunset_sunrise["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sunset_sunrise["results"]["sunset"].split("T")[1].split(":")[0])

    return sunrise, sunset


while True:

    api_data = requests.get(url="http://api.open-notify.org/iss-now.json")
    api_data.raise_for_status()
    data = api_data.json()


    def view_point_location():
        with open("data.json") as file:
            view_point_position = json.load(file)
            # replace view_point_lat and view_point_lng with your latitude and longitude. You can utilize this website
            # https://www.latlong.net to find your latitude and longitude.
            view_point_lat = view_point_position["my_location"]["lat"]
            view_point_lng = view_point_position["my_location"]["lng"]
            return view_point_lat, view_point_lng


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
        view_lat, view_lng = view_point_location()
        with open("iss_data_path_history.csv", "a", newline="") as outfile:
            writer = csv.writer(outfile, delimiter=",")
            latitude, longitude = get_iss_data()
            date, current_time = get_path_time()
            iss_data = [latitude, longitude, date, current_time, view_lat, view_lng]
            writer.writerow(iss_data)

            return


    def plotter():
        path_time_history()
        df = pandas.read_csv("iss_data_path_history.csv")
        figure = px.scatter_geo()
        figure.update_layout(title="ISS Tracker", title_x=0.5, legend=dict(
            title="Legend:",
            yanchor="top",
            y=-5,
            xanchor="left",
            x=0.4,
            orientation="h"
        ))
        figure.update_layout(height=600, margin={"r": 0, "t": 50, "l": 0, "b": 0}, autosize=True)

        figure.add_scattergeo(lat=df["view_lat"], lon=df["view_lng"],
                              mode="markers", name="Washington State  ", marker=dict(size=16, symbol="star",
                                                                                     color="red"))

        figure.add_scattergeo(lat=df["latitude"], lon=df["longitude"],
                              mode="markers", name="ISS",
                              marker=dict(size=16, symbol="arrow", angleref="previous",
                                          line=dict(width=2, color="DarkTurquoise"), color="blue"))

        figure.show()


    plotter()

    distance = haversine(get_iss_data(), view_point_location(), unit="mi")
    degrees_away = distance / 69


    def is_dark():
        light, dark = get_sunrise_sunset()
        current_time = datetime.now()
        hour = current_time.hour
        if hour >= dark:
            return True


    def send_email():
        try:
            with open("data.json", "r") as email:
                email_data = json.load(email)
        except FileNotFoundError:
            print("Error, file not located.")
        except json.decoder.JSONDecodeError:
            print("Error, file empty.")
        else:
            my_email = email_data["outlook"]["email"]
            my_pwd = email_data["outlook"]["password"]
            email_recipient = []
            for recipient in email_data['recipients']:
                email_recipient.append(recipient['email'])
            with smtplib.SMTP("smtp-mail.outlook.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_pwd)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email_recipient,
                    msg=f"Subject:ISS Sighting\n\n The ISS is nearing your position. Go Outside")


    if is_dark() and degrees_away <= 5:
        print(f"Go Outside ISS is {int(distance)} miles away. Which is approximately {int(degrees_away)} degrees away.")
        send_email()
    else:
        print(f"ISS is {int(distance)} miles away. Which is approximately {int(degrees_away)} degrees away.")
    time.sleep(60)
