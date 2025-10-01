from datetime import date
import os
from dotenv import load_dotenv
import requests

load_dotenv()
dzisiaj = date.today().isoformat()

API_KEY = os.getenv("API")
def get_nasa_apod(data_apod):

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": API_KEY,
        "date": data_apod
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")

def get_nasa_apod_timeline(poczatek, koniec):
    

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": API_KEY,
        "start_date": poczatek,
        "end_date": koniec
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")

def get_nasa_apod_random():
    
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": API_KEY,
        "count": 1
    }
            #  {% comment %} Podaj datę dla której chcesz sprawdzić zdjęcia: <br>
            # <input type="date" name="data_apod" id="" required max="{{ dzisiaj }}"> <br>
            # <input type="submit" value="Sprawdź"> {% endcomment %}
           
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data[0]
    else:
        print(f"Error: {response.status_code}")
        return None