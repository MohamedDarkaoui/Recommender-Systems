from flask import Blueprint, render_template, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/')
def default():
    return redirect("login")

@views.route('/home')
def home():
    return render_template("base.html")

@views.route('/datasets')
def datasets():
    return render_template("datasets.html")

@views.route('/experiments')
def experiments():
    return render_template("experiments.html")

@views.route('/models')
def models():
    return render_template("models.html")

@views.route('/scenarios')
def scenarios():
    return render_template("scenarios.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

