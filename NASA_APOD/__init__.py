from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from .routes import bp
from .extensions import cache, db

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='templates', static_folder='static',)

    # Konfiguracja
    app.config['CACHE_TYPE'] = "SimpleCache"
    
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    cache.init_app(app)

    # Importowanie tras
    from . import routes
    app.register_blueprint(routes.bp)

    return app