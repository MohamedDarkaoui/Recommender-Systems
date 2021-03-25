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
from entitiesDB.dataset import Dataset
from config import config_data
from random import randint
import pandas as pd
import csv

from sqlalchemy import create_engine

# /etc/postgresql/##/main/pg_hba.conf aanpassen -> 'trust'

connection = DBConnection(dbname=config_data['dbname'], dbuser=config_data['dbuser'])
engine = create_engine('postgresql+psycopg2://postgres:mounir@localhost/ppdb')
#engine = create_engine('postgresql+psycopg2://postgres:mohamed@localhost/ppdb')


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
            dataset = Dataset(id=randint(0,10^20), name=datasetName, usr_id=str(current_user.id), private=True)
            datasetDB.add_dataset(dataset)
            #insert interactions, items and clients
            interactions = pd.read_csv(interactionsCSV)
            columns = list(interactions.columns)
            items = interactions[columns[1]].unique()
            clients = interactions[columns[0]].unique()

            for item in items:
                ItemDB.add_item(str(item), str(dataset.id))
            for client in clients:
                ClientDB.add_client(str(client), str(dataset.id))

            interactions.rename(columns={columns[0]: 'client_id', columns[1]: 'item_id', columns[2]: 'timestamp'})
            interactions.columns = ['client_id', 'item_id', 'timestamp']
            interactions.insert(0, 'dataset_id', dataset.id)
            interactions.to_sql('interaction', engine, if_exists='append', index = False)
            
            #insert metadata if exists
            if metadataCSV.content_type == 'text/csv':
                metadata = pd.read_csv(metadataCSV)
                columns = list(metadata.columns)
                #insert metadata
                metadataId = randint(0,10^20)
                MetadataDB.add_metadata(id = metadataId, dataset_id = dataset.id)
                for index, row in metadata.iterrows():
                    print(index)
                    itemId = row[columns[0]]
                    #iterate through all columns
                    for column in columns[1:]:
                        #get info
                        data = row[column]
                        description = column
                        #add metadata_element
                        MetadataElementDB.add_metadataElement(item_id = itemId, dataset_id = dataset.id, 
                            metadata_id = metadataId, description = description, data = data)


    datasets = [('1', 'dataset1', '03/12/21'), ('2', 'datasetMohamed', '12/05/20')]
    return render_template("datasets.html", datasets = datasets)

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
    return render_template("profile.html", currentUser = current_user)
