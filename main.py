import requests
import json 
import dotenv
import os
from flask import Flask, render_template, request
from datetime import datetime, date, time 

dotenv.load_dotenv()
dzien = None
def get_nasa_apod(dzien):
    

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": os.getenv("API"),
        "date": dzien
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
        "api_key": os.getenv("API"),
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
        "api_key": os.getenv("API"),
        "count": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data[0]
    else:
        print(f"Error: {response.status_code}")
        return None

app = Flask(__name__, template_folder='templates', static_folder='static',)

# apod_info = get_nasa_apod(dzien)
# print(f"Tytuł: {apod_info['title']}")
# print(f"Data: {apod_info['date']}")
# print(f"Data: {apod_info['explanation']}")
dzisiaj = date.today().isoformat()
@app.route('/', methods=['GET', 'POST'])
def apod():
    # timestamp = int(time.time())
    error = None
    wybrana_data = None
    if request.method == 'POST':
        zdjecie = request.form.get('data_apod')


        if not zdjecie:
            error = "Data jest niepoprawna"
        else:
            wybrana_data = get_nasa_apod(zdjecie)
        
            if wybrana_data is None:
                    error = "Nie udało się pobrać danych z NASA API"
            
    return render_template('index.html', get_nasa_apod = wybrana_data, error = error, dzisiaj = dzisiaj)

@app.route('/today', methods = ['GET', 'POST'])
def today():
    # timestamp = int(time.time())

    error = None
    wybrana_data = None
    zdjecie_dzisiaj = date.today().isoformat()
    wybrana_data = get_nasa_apod(zdjecie_dzisiaj)
            
    return render_template('dzisiaj.html', get_nasa_apod = wybrana_data, error = error)

@app.route('/timeline', methods = ['GET', 'POST'])
def timeline():
    # timestamp = int(time.time())

    error = None
    wybrany_okres = None
    if request.method == 'POST':
        poczatek = request.form.get('poczatkowa_data')
        koniec = request.form.get('koncowa_data')

        if not poczatek or not koniec:
            error = "Data jest niepoprawna"
        else:
            wybrany_okres = get_nasa_apod_timeline(poczatek, koniec)
             
    return render_template('timeline.html', get_nasa_apod_timeline = wybrany_okres, error = error, dzisiaj = dzisiaj)

@app.route('/random', methods = ['GET', 'POST'])
def random():
    wybrany_random = None
    wybrany_random = get_nasa_apod_random()
    return render_template('random.html', get_nasa_apod_random = wybrany_random)

    


if __name__ == '__main__':
    app.run(debug=True)


# print (response.text)
