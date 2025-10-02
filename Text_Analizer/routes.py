from datetime import date
from flask import Blueprint, render_template, request
from .extensions import cache

analyzer_bp = Blueprint('analyzer', __name__, template_folder="templates")

@analyzer_bp.route('/')
def home():
    return render_template("index.html")