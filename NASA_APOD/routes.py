from datetime import date
from flask import Blueprint, render_template, request
from .nasa_api import get_nasa_apod, get_nasa_apod_random, get_nasa_apod_timeline, dzisiaj
from .forms import kalendarz_form
from .extensions import cache

bp = Blueprint('main', __name__)

# @app.route('/')
# def home():
#     if "username" in session:
#         return redirect(url_for('dashboard'))
#     return render_template('index.html')
@bp.route('/')
def home():
    return render_template("index.html")

@bp.route('/apod', methods=['GET', 'POST'])
@cache.cached(timeout=60*60)
def apod():

    form = kalendarz_form()

    error = None
    wybrana_data = None
    if form.validate_on_submit():
        zdjecie = form.data_apod.data.strftime("%Y-%m-%d")

        wybrana_data = get_nasa_apod(zdjecie)
        
        if wybrana_data is None:
            error = "Nie udało się pobrać danych z NASA API"
            
    return render_template('apod.html', get_nasa_apod = wybrana_data, error = error, dzisiaj = dzisiaj, form = form)

@bp.route('/today', methods = ['GET', 'POST'])
@cache.cached(timeout=60*60)
def today():

    error = None
    wybrana_data = None
    zdjecie_dzisiaj = date.today().isoformat()
    wybrana_data = get_nasa_apod(zdjecie_dzisiaj)
            
    return render_template('dzisiaj.html', get_nasa_apod = wybrana_data, error = error)

@bp.route('/timeline', methods = ['GET', 'POST'])
@cache.cached(timeout=60*60)
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

@bp.route('/random', methods = ['GET', 'POST'])
@cache.cached(timeout=60*60)
def random():
    wybrany_random = None
    wybrany_random = get_nasa_apod_random()

    return render_template('random.html', get_nasa_apod_random = wybrany_random)

  