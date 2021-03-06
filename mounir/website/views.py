from flask import Blueprint, render_template, redirect

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    return render_template("dashboard.html")

@views.route('/datasets')
def datasets():
    return render_template("datasets.html")

@views.route('/scenarios')
def scenarios():
    return render_template("scenarios.html")

@views.route('/models')
def models():
    return render_template("models.html")

@views.route('/experiments')
def experiments():
    return render_template("experiments.html")

@views.route('/settings')
def settings():
    return render_template("settings.html")

@views.route('/profile')
def profile():
    return render_template("profile.html")