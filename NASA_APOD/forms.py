from flask import Flask
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from .extensions import db
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash


class kalendarz_form(FlaskForm):
    data_apod = DateField(
        "Wybierz datę dla której chcesz sprawdzić zdjęcie: ",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        name="date"
        )
    submit = SubmitField("Sprawdź")

# Model bazy danych
class User(db.Model):
    # Zmienne klasy
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)