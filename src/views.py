from datetime import time
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import *
from config import config_data
from models import Users
from appCreator import db
from algorithm import *
import pandas as pd
import numpy as np
from datetime import datetime
import csv
import io



from sqlalchemy import create_engine

# /etc/postgresql/##/main/pg_hba.conf aanpassen -> 'trust'

connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
datasetDB = DatasetDB(connection)
itemDB = ItemDB(connection)
clientDB = ClientDB(connection)
interactionDB = interactionDB(connection)
metadataDB = MetadataDB(connection)
metadataElementDB = MetadataElementDB(connection)
scenarioDB = ScenarioDB(connection)
modelDB = ModelDB(connection)
experimentDB = ExperimentDB(connection)
views = Blueprint('views', __name__)

from datasets import datasets, data_samples
from scenarios import scenarios, scen_samples
from _models import models
from experiments import experiments, experimentdata


@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/users')
@login_required
def users():
    users = Users.query.all()
    return render_template("users.html", users = enumerate(users))

@views.route('users/<username>')
@login_required
def user(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('views.users'))
    #get public datasets
    datasets = datasetDB.getDatasetsFromUser(user)
    for i in range(len(datasets)):
        client_count = clientDB.getCountClients(datasets[i].id)
        item_count = itemDB.getCountItems(datasets[i].id)
        interaction_count = interactionDB.getCountInteractions(datasets[i].id)
        datasets[i] = (datasets[i], interaction_count, item_count, client_count)

    #get private experiments
    experiments = experimentDB.getExperimentsFromUser(user)

    return render_template("user.html", datasets=enumerate(datasets), experiments=enumerate(experiments))

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and request.form.get('which-form') == "change":
        current = request.form.get('Current')
        new = request.form.get('New')
        confirm = request.form.get('Confirm')
        username = request.form.get('Username')
        user = Users.query.filter_by(email=current_user.email).first()

        if username:
            if check_password_hash(user.password, current):
                user.username = username
                db.session.commit()
                flash('Username succesfully changed.')

        if current and new and confirm:
            if new == confirm:
                if check_password_hash(user.password, current):
                    user.password = generate_password_hash(new, method='sha256')
                    db.session.commit()
                    flash('Password succesfully changed.')
                    
    return render_template("profile.html", currentUser = current_user)
