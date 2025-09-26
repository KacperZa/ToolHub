import requests
import json 
import dotenv
import os
from flask import Flask, render_template, request
from datetime import datetime, date, time 
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired

dotenv.load_dotenv()
dzien = None

app = Flask(__name__, template_folder='templates', static_folder='static',)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

class kalendarz_form(FlaskForm):
    data_apod = DateField("Wybierz datę dla której chcesz sprawdzić zdjęcie: ", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Sprawdź")
    
def get_nasa_apod(data_apod):

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": os.getenv("API"),
        # "date": dzien
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


# apod_info = get_nasa_apod(dzien)
# print(f"Tytuł: {apod_info['title']}")
# print(f"Data: {apod_info['date']}")
# print(f"Data: {apod_info['explanation']}")
dzisiaj = date.today().isoformat()
@app.route('/', methods=['GET', 'POST'])
def apod():

    form = kalendarz_form()

    error = None
    wybrana_data = None
    if form.validate_on_submit():
        zdjecie = form.data_apod.data.strftime("%Y-%m-%d")

        wybrana_data = get_nasa_apod(zdjecie)
        
        if wybrana_data is None:
            error = "Nie udało się pobrać danych z NASA API"
            
    return render_template('index.html', get_nasa_apod = wybrana_data, error = error, dzisiaj = dzisiaj, form = form)

@app.route('/today', methods = ['GET', 'POST'])
def today():

    error = None
    wybrana_data = None
    zdjecie_dzisiaj = date.today().isoformat()
    wybrana_data = get_nasa_apod(zdjecie_dzisiaj)
            
    return render_template('dzisiaj.html', get_nasa_apod = wybrana_data, error = error)

@app.route('/timeline', methods = ['GET', 'POST'])
def timeline():

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
