from flask import Flask
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired

class kalendarz_form(FlaskForm):
    data_apod = DateField(
        "Wybierz datę dla której chcesz sprawdzić zdjęcie: ",
        format="%Y-%m-%d",
        validators=[DataRequired()],
        name="date"
        )
    submit = SubmitField("Sprawdź")