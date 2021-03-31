from datetime import time
from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from database.DBConnection import DBConnection 
from database.datasetDB import DatasetDB
from database.interactionDB import interactionDB
from database.itemDB import ItemDB
from database.clientDB import ClientDB
from database.metadataDB import MetadataDB
from database.metadataElementDB import MetadataElementDB
from database.entitiesDB import Dataset, Metadata
from werkzeug.security import generate_password_hash, check_password_hash
from config import config_data
from random import randint
from models import Users
from appCreator import db
import pandas as pd
from datetime import datetime
import csv
import io

from sqlalchemy import create_engine

# /etc/postgresql/##/main/pg_hba.conf aanpassen -> 'trust'

connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
#engine = create_engine('postgresql+psycopg2://postgres:mounir@localhost/ppdb')
#engine = create_engine('postgresql+psycopg2://postgres:khalil@localhost/ppdb')
engine = create_engine('postgresql+psycopg2://postgres:mohamed@localhost/ppdb')


datasetDB = DatasetDB(connection)
ItemDB = ItemDB(connection)
ClientDB = ClientDB(connection)
interactionDB = interactionDB(connection)
MetadataDB = MetadataDB(connection)
MetadataElementDB = MetadataElementDB(connection)
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
            dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
            dataset = Dataset(name=datasetName, usr_id=str(current_user.id), date_time=dt_string, private=True)
            dataset = datasetDB.add_dataset(dataset)
            
            # create pandas objects
            interactions = pd.read_csv(interactionsCSV)
            columns = list(interactions.columns)
            interactions.rename(columns={columns[0]: 'client_id', columns[1]: 'item_id', columns[2]: 'timestamp'})
            interactions.columns = ['client_id', 'item_id', 'timestamp']
            interactions.insert(0, 'dataset_id', dataset.id)
            
            items = interactions[['item_id','dataset_id']].copy()
            items.columns = ['id','dataset_id']
            items = items.drop_duplicates()

            clients = interactions[['client_id','dataset_id']]
            clients.columns = ['id','dataset_id']
            clients = clients.drop_duplicates()

            # insert items,clients and interactions
            ItemDB.add_item(items)
            ClientDB.add_client(clients)
            interactionDB.add_interaction(interactions)

            
            #insert metadata if exists
            if metadataCSV.content_type == 'text/csv':
            
                metadata = pd.read_csv(metadataCSV)
                columns = list(metadata.columns)
                metadataOBJ = Metadata(dataset.id)
                #insert metadata
                metadataOBJ = MetadataDB.add_metadata(metadataOBJ)
                for index, row in metadata.iterrows():
                    itemId = row[columns[0]]
                    #iterate through all columns
                    for column in columns[1:]:
                        #get info
                        data = row[column]
                        description = column
                        #add metadata_element
                        MetadataElementDB.add_metadataElement(item_id=itemId, dataset_id=dataset.id, 
                            metadata_id=metadataOBJ.id, description=description, data=data)

    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name, datasets[i].date_time, datasets[i].private)
    return render_template("datasets.html", datasets = datasets)

@views.route('/scenarios')
@login_required
def scenarios():

    
    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name)
    return render_template("scenarios.html", datasets = datasets)

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

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST' and request.form.get('which-form') == "change":
        current = request.form.get('Current')
        new = request.form.get('New')
        confirm = request.form.get('Confirm')
        username = request.form.get('Username')
        user = Users.query.filter_by(email=current_user.email).first()
        if username != "":
            user.username = username
            db.session.commit()
        if current != "" and new != "" and confirm != "":
            if new == confirm:
                if check_password_hash(user.password, current):
                    user.password = generate_password_hash(new, method='sha256')
                    db.session.commit()
    return render_template("profile.html", currentUser = current_user)