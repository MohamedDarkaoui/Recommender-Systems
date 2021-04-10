from datetime import time
from flask import Blueprint, render_template, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import *
from config import config_data
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
itemDB = ItemDB(connection)
clientDB = ClientDB(connection)
interactionDB = interactionDB(connection)
metadataDB = MetadataDB(connection)
metadataElementDB = MetadataElementDB(connection)
scenarioDB = ScenarioDB(connection)
views = Blueprint('views', __name__)


@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/datasets/', methods=['GET', 'POST'])
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
            interactions.rename(columns={columns[0]: 'client_id', columns[1]: 'item_id', columns[2]: 'tmstamp'})
            interactions.columns = ['client_id', 'item_id', 'tmstamp']
            interactions.insert(0, 'dataset_id', dataset.id)
            
            items = interactions[['item_id','dataset_id']].copy()
            items.columns = ['id','dataset_id']
            items = items.drop_duplicates()

            clients = interactions[['client_id','dataset_id']]
            clients.columns = ['id','dataset_id']
            clients = clients.drop_duplicates()

            # insert items,clients and interactions
            print('inserting items')
            itemDB.add_item(items)
            print('inserting clients')
            clientDB.add_client(clients)
            print('inserting interactions')
            interactionDB.add_interaction(interactions)
            
            #insert metadata if exists
            if metadataCSV.content_type == 'text/csv':
                metadata = pd.read_csv(metadataCSV)
                columns = list(metadata.columns)
                metadata.drop(columns[0], axis=1)
                metadataOBJ = Metadata(dataset.id)

                #insert metadata
                metadataOBJ = metadataDB.add_metadata(metadataOBJ)

                #add dataset and metadata id columns
                metadata.insert(1, 'dataset_id', dataset.id)
                metadata.insert(2, 'metadata_id', metadataOBJ.id)

                #rename de item id
                metadata = metadata.rename(columns={columns[0]: 'item_id'})

                columns = list(metadata.columns)
                #CREATE TEMPORARY DESC DATAFRAMES
                tempDataframes = []
                for column in columns[3:]:
                    tempDataframes.append(pd.DataFrame([metadata[column]]).transpose())

                #REMOVE ALL DESC FROM METADATA
                metadata = metadata.drop(columns[3:], axis=1)
                
                #ADD EACH DESC TO METADATA INSER INTO DATASET AND THEN REMOVE IT
                for tempDataframe in tempDataframes:
                    #ADD DESC
                    descName = tempDataframe.columns[0]
                    metadata.insert(3, 'description', descName)
                    tempDataframe = tempDataframe.rename(columns={descName: 'data'})

                    #ADD DATA
                    metadata = pd.concat([metadata, tempDataframe], axis=1)

                    #COPY INTO DATABASE
                    #### HIER MOHAMED ######
                    ##copy_from(metadata) into database table metadataelement

                    #REMOVE FROM CURRENT DESC AND DATA FORM METADATA DATAFRAME
                    metadata = metadata.drop(metadata.columns[3:5], axis=1)

    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name, datasets[i].date_time, datasets[i].private)
    return render_template("datasets.html", datasets = datasets)

@views.route('/scenarios',methods=['GET', 'POST'])
@login_required
def scenarios():
    if request.method == 'POST' and request.form.get('which-form') == 'chooseScenario':
        scenarioName = request.form.get('scenarioName')
        datasetID = request.form.get('datasetSelect')
        time1 = request.form.get('startDate')
        time2 = request.form.get('endDate')
        umin = request.form.get('user_min')
        umax = request.form.get('user_max')
        imin = request.form.get('item_min')
        imax = request.form.get('item_max')

        if len(time1) == 0:
            time1 = '-infinity' 
        if len(time2) == 0:
            time2 = 'infinity'
        if len(umin) == 0:
            umin = '0'
        if len(umax) == 0:
            umax = 'infinity'
        if len(imin) == 0:
            imin = '0'
        if len(imax) == 0:
            imax = 'infinity'

        if len(scenarioName) > 0 and len(datasetID) > 0:
            dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
            scenario = Scenario(name=scenarioName,usr_id=str(current_user.id),date_time=dt_string,dataset_id=datasetID)
            scenario = scenarioDB.add_scenario(scenario)
            scen_elem = scenarioDB.get_interactionsPD(datasetID, time1=time1, time2=time2, imin=imin, imax=imax, umin=umin, umax=umax)
            scen_elem.insert(0, 'scenario_id', scenario.id)
            scenarioDB.add_scenario_elements(scen_elem)
            

    scenarios = scenarioDB.getScenariosFromUser(current_user)
    for i in range(len(scenarios)):
        scenarios[i] = (i+1, scenarios[i].name, scenarios[i].dataset_id, scenarios[i].date_time)

    
    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name)
    return render_template("scenarios.html", datasets = datasets,scenarios=scenarios)


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


@views.route('/datasets/<dataset_name>')
@login_required
def data_samples(dataset_name):

    dataset_id = datasetDB.getDatasetID(current_user.id,dataset_name)
    client_count = clientDB.getCountClients(dataset_id)
    item_count = itemDB.getCountItems(dataset_id)
    interaction_count = interactionDB.getCountInteractions(dataset_id)
    interaction_sample = interactionDB.getInteractionSample(dataset_id)

    print(dataset_id)

    return render_template("dataset_sample.html",dataset_name=dataset_name, 
    client_count=client_count,item_count=item_count,interaction_count=interaction_count,interaction_sample=interaction_sample)


@views.route('/scenarios/scenario_samples')
@login_required
def scen_samples():
    return render_template("scenario_sample.html")

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
