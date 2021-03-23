from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd
import csv


views = Blueprint('views', __name__)


@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():
    if request.method == 'POST' and request.form.get('which-form') == "uploadDataset":
        datasetName = request.form.get('datasetname')
        interactionsCSV = request.files['csvinteractions']
        metadataCSV = request.files['csvmetadata']
        print(datasetName)
        print(interactionsCSV.filename)
        print(metadataCSV.filename)
        df = pd.read_csv(interactionsCSV)
        print(df)

    
    return render_template("datasets.html")

@views.route('/scenarios')
@login_required
def scenarios():
    return render_template("scenarios.html")

@views.route('/models')
@login_required
def models():
    return render_template("models.html")

@views.route('/experiments')
@login_required
def experiments():
    return render_template("experiments.html")

@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html")

@views.route('/users')
@login_required
def users():
    return render_template("users.html")    

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html")
