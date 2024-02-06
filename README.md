# ISS Tracker
<div align="center"><img src="https://github.com/TFR25/ISS-Tracker/assets/101258399/673bbee4-2e2d-4fdb-8067-046634d27f09"></div>

## Introduction
This Python program, ISS Tracker, is designed to track the International Space Station (ISS) in real-time and provide notifications when the ISS is within a certain distance from a specified location during nighttime. The program utilizes data from two APIs to obtain the current ISS location and sunrise/sunset times, as well as the Haversine formula to calculate the distance between the ISS and a specified viewing point.

## Features
- Real-time tracking of the ISS using the Open Notify API.
- Calculation of the distance and degrees away from the ISS to a specified viewing point.
- Determination of whether it is currently dark based on sunrise and sunset times.
- Notification via email when the ISS is within a specified distance during nighttime.
- Logging of ISS position data to a CSV file for mapping purposes using Plotly Express.

## Dependencies
Make sure to install the required Python libraries before running the program. You can install them using the following command:
```bash
pip install plotly-express pandas requests haversine smtplib
```

## Configuration
1. Create a file named `data.json` with the following structure:
   ```json
   {
     "my_location": {
       "lat": YOUR_LATITUDE,
       "lng": YOUR_LONGITUDE,
       "tzid": "YOUR_TIMEZONE_ID"
     },
     "outlook": {
       "email": "YOUR_EMAIL",
       "password": "YOUR_PASSWORD"
     },
     "recipients": [
       {"email": "RECIPIENT_EMAIL_1"},
       {"email": "RECIPIENT_EMAIL_2"}
       // Add more recipients as needed
     ]
   }
   ```
   - Replace `YOUR_LATITUDE` and `YOUR_LONGITUDE` with the latitude and longitude of your viewing point.
   - Replace `YOUR_TIMEZONE_ID` with the timezone ID of your location.
   - Replace `YOUR_EMAIL` and `YOUR_PASSWORD` with your Outlook email credentials.
   - Add the email addresses of recipients in the `recipients` array.

## Usage

The program will continuously track the ISS, log its position, and provide notifications when conditions are met.

## Important Note
Make sure to keep the `data.json` file secure, especially if it contains sensitive information such as email credentials.
