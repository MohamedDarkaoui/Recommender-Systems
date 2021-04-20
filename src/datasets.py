from views import *

@views.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():
    if request.method == 'POST':
        if request.form.get('which-form') == "uploadDataset":
            addDataset(request)
        elif request.form.get('which-form') == "deleteDataset":
            deleteDataset(request)
            
    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name, datasets[i].date_time, datasets[i].private)
    return render_template("datasets.html", datasets = datasets)

@views.route('/datasets/<dataset_name>')
@login_required
def data_samples(dataset_name):

    dataset_id = datasetDB.getDatasetID(current_user.id,dataset_name)
    client_count = clientDB.getCountClients(dataset_id)
    item_count = itemDB.getCountItems(dataset_id)
    interaction_count = interactionDB.getCountInteractions(dataset_id)
    interaction_sample = interactionDB.getInteractionSample(dataset_id)
    metadata_sample = metadataElementDB.getMetadataSample(dataset_id)
 
    return render_template("dataset_sample.html",dataset_name=dataset_name, 
    client_count=client_count,item_count=item_count,interaction_count=interaction_count,interaction_sample=interaction_sample,metadata_sample=metadata_sample)

def addDataset(request):
    datasetName = request.form.get('datasetname')
    interactionsCSV = request.files['csvinteractions']
    metadataCSV = request.files.getlist('csvmetadata')
    clientIdColumn = request.form.get('userIdColumn')        
    itemIdColumn = request.form.get('itemIdColumn')
    timestampColumn = request.form.get('timestampColumn')


    if interactionsCSV.content_type == 'text/csv' and len(datasetName) > 0:
        # insert dataset
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        dataset = Dataset(name=datasetName, usr_id=str(current_user.id), date_time=dt_string, private=True)
        dataset = datasetDB.add_dataset(dataset)

        # create pandas objects
        interactions = pd.read_csv(interactionsCSV)
        columns = list(interactions.columns)
        
        interactions.rename(columns={clientIdColumn: 'client_id', itemIdColumn: 'item_id', timestampColumn: 'tmstamp'})
        interactions = interactions['client_id', 'item_id', 'tmstamp']
        interactions.insert(0, 'dataset_id', dataset.id)
        
        items = interactions[['item_id','dataset_id']].copy()
        items.columns = ['id','dataset_id']
        items = items.drop_duplicates()

        clients = interactions[['client_id','dataset_id']]
        clients.columns = ['id','dataset_id']
        clients = clients.drop_duplicates()

        # insert items,clients and interactions
        itemDB.add_item(items)
        clientDB.add_client(clients)
        interactionDB.add_interaction(interactions)
        
        #insert metadata if exists
        if request.form.get('metadataCheck') == 'on': # and metadataCSV.content_type == 'text/csv':
            print("ONNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
            print(metadataCSV)
            for mdata in metadataCSV:
                print("YOOOOO")
                addMetadata(mdata,dataset)

        flash('Dataset succesfully made.')
        
def addMetadata(metadataCSV,dataset):
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
        if metadata['data'].dtypes == 'object':
            metadata['data'] = metadata['data'].astype(str).str.replace("\r","")
        #COPY INTO DATABASE
        metadataElementDB.add_metadataElements(metadata)

        #REMOVE FROM CURRENT DESC AND DATA FORM METADATA DATAFRAME
        metadata = metadata.drop(metadata.columns[3:5], axis=1)

def deleteDataset(request):
    name = request.form.get('datasetName')
    datasetDB.deleteDataset(name,current_user.id)
    flash('Dataset succesfully deleted.')