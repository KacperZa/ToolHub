from datetime import date
from flask import Blueprint, render_template, request, redirect, session, url_for
from .nasa_api import get_nasa_apod, get_nasa_apod_random, get_nasa_apod_timeline, dzisiaj
from .simply_func import analiza_zdania
from .forms import kalendarz_form, User
from .extensions import cache, db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    if "username" in session:
        return redirect(url_for('main.dashboard'))
    return render_template("index.html")
    

@bp.route('/apps')
def apps():
    cards = [
        {"emoji": "🚀", "opis":"Ciekawi ciebie kosmos? Jeśli tak, to wbijaj tutaj!", "url":"main.nasa_home"},
        {"emoji": "🔤", "opis":"Chcesz policzyć wyrazy w tekście? A może sprawdzić statystyki tekstu? Musisz to sprawdzić!", "url":"main.analyzer"},
        {"emoji": "🧮", "opis":"Lubisz matematyke? To coś dla ciebie!", "url":"main.math"},
        {"emoji": "🚀", "opis":"Ciekawi ciebie kosmos? Jeśli tak, to wbijaj tutaj!", "url":"main.nasa_home"},
        {"emoji": "🚀", "opis":"Ciekawi ciebie kosmos? Jeśli tak, to wbijaj tutaj!", "url":"main.nasa_home"},
        {"emoji": "🚀", "opis":"Ciekawi ciebie kosmos? Jeśli tak, to wbijaj tutaj!", "url":"main.nasa_home"},
        {"emoji": "🚀", "opis":"Ciekawi ciebie kosmos? Jeśli tak, to wbijaj tutaj!", "url":"main.nasa_home"},
    ]
    return render_template('apps.html', cards=cards)


# Login
@bp.route('/login', methods=["POST"])
def login():
    # Zbieranie info z formularza
    username = request.form['username']
    password = request.form['password']

    # Sprawdzanie czy jest w bazie danych
    user = User.query.filter_by(username = username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('main.dashboard'))
    else:
        return render_template("index.html")
    
    # Rejestracja
@bp.route('/register', methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username = username).first()
    if user:
        return render_template("index.html", error="Użytkownik już istnieje!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for("main.dashboard"))
# Dashboard
@bp.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username = session['username'])
    return redirect(url_for('main.home'))

# Logout
@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.home'))

@bp.route('/math')
def math():
    return render_template('matma.html')
    

@bp.route('/analyzer', methods=['POST', 'GET'])
def analyzer():

    tekst_analiza = None
    error = None
    if request.method == 'POST':
        # tekst = request.form.get['tekst', ''].strip()
        tekst = request.form['tekst'].strip()
        if  not tekst:
            session['error'] = "Pole nie może być puste"
        else:
            # tekst_analiza = analiza_zdania(tekst)
            analiza_wyniki = analiza_zdania(tekst)
            if analiza_wyniki:
                session['tekst_analiza'] = analiza_wyniki
            else: 
                session['error'] = "Wprowadzony tekst nie zawiera wyrazów do analizy"
        
        redirect(url_for('main.analyzer'))

    tekst_analiza = session.pop('tekst_analiza', None)
    error = session.pop('error', None)


    return render_template('analyzer.html', tekst_analiza = tekst_analiza, error = error)

        

@bp.route('/nasa_home')
def nasa_home():
    return render_template('nasa_home.html')

@bp.route('/apod', methods=['GET', 'POST'])
# @cache.cached(timeout=60*60)
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
# @cache.cached(timeout=60*60)
def random():
    wybrany_random = None
    wybrany_random = get_nasa_apod_random()

    return render_template('random.html', get_nasa_apod_random = wybrany_random)

  