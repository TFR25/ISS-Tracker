import requests

api_data = requests.get(url="http://api.open-notify.org/iss-now.json")
api_data.raise_for_status()



