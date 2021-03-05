from flask import Blueprint, render_template, redirect

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    return render_template("home.html")