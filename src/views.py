from datetime import time
from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from database.DBConnection import DBConnection 
from database.datasetDB import DatasetDB
from database.interactionDB import interactionDB
from database.itemDB import ItemDB
from database.clientDB import ClientDB
from entitiesDB.dataset import Dataset
from config import config_data
from random import randint
import pandas as pd
import csv

from sqlalchemy import create_engine

# /etc/postgresql/##/main/pg_hba.conf aanpassen -> 'trust'

connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])

datasetDB = DatasetDB(connection)
ItemDB = ItemDB(connection)
ClientDB = ClientDB(connection)
interactionDB = interactionDB(connection)

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

        if interactionsCSV.content_type == 'text/csv' and len(datasetName) > 0:
            
            # insert dataset
            dataset = Dataset(id=randint(0,10^20), name=datasetName, usr_id=str(current_user.id), private=True)
            datasetDB.add_dataset(dataset)
            
            #insert interaction
            interactions = pd.read_csv(interactionsCSV)
            columns = list(interactions.columns)
            items = interactions[columns[1]].unique()
            clients = interactions[columns[0]].unique()
            for item in items:
                ItemDB.add_item(str(item), str(dataset.id))
            for client in clients:
                ClientDB.add_client(str(client), str(dataset.id))

            
            # deze voegt heel onze interaction tabel toe in de dataset, MAAAAAAAAAR
            # vervangt alle colommen in die tabel nr nieuwe namen
            engine = create_engine('postgresql+psycopg2://postgres:mohamed@localhost/ppdb')
            interactions.to_sql('interaction', engine, if_exists='replace', index = False)
            
            """
            for index, row in interactions.iterrows():
                print(index)
                client_id = row[columns[0]]
                item_id = row[columns[1]]
                timestamp = row[columns[2]]

                interactionDB.add_interaction(dataset_id=dataset.id,client_id=str(client_id),item_id=str(item_id),timestamp=str(timestamp))
            """
    
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
