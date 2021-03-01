from flask import Blueprint, render_template, redirect, url_for

views = Blueprint('views', __name__)


@views.route('/')
def default():
    return redirect("login")

@views.route('/home')
def home():
    return render_template("interface.html")
