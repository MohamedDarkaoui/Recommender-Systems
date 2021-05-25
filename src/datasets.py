from views import *
from experiments import is_url_image

@views.route('/datasets', methods=['GET', 'POST'])
@login_required
def datasets():
    if request.method == 'POST':
        if request.form.get('which-form') == "uploadDataset":
            addDataset(request)
        elif request.form.get('which-form') == "deleteDataset":
            deleteDataset(request)
        elif request.form.get('which-form') == "makePublic":
            changeDatasetPublic(request)
        elif request.form.get('which-form') == "makePrivate":
            changeDatasetPrivate(request)

    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name, datasets[i].date_time, datasets[i].private, datasets[i].id, datasets[i].usr_id, True)

    followedDatasets = datasetDB.getFollowedDatasets(current_user)
    for i in range(len(followedDatasets)):
        owner = Users.query.filter_by(id=followedDatasets[i].usr_id).first()
        followedDatasets[i] = (i+len(datasets)+1, followedDatasets[i].name + ' (' + owner.username + ')', followedDatasets[i].date_time,
            followedDatasets[i].private, followedDatasets[i].id, followedDatasets[i].usr_id, False)

    return render_template("datasets.html", datasets = datasets+followedDatasets)

@views.route('/datasets/<dataset_id>')
@login_required
def data_samples(dataset_id):
    try:
        dataset_id=int(dataset_id)
    except:
        return redirect(url_for('views.datasets'))
    
    if not datasetDB.datasetExistsById(dataset_id):
        return redirect(url_for('views.datasets'))
    
    dataset = datasetDB.getDatasetById(dataset_id)
    if dataset.usr_id != current_user.id and not datasetDB.followsDataset(current_user, dataset_id):
        return redirect(url_for('views.datasets'))

    
    dataset_name = datasetDB.getDatasetName(dataset_id)
    client_count = clientDB.getCountClients(dataset_id)
    item_count = itemDB.getCountItems(dataset_id)
    interaction_count = interactionDB.getCountInteractions(dataset_id)
    interaction_sample = interactionDB.getInteractionSample(dataset_id)
    metadata_sample = metadataElementDB.getMetadataSample(dataset_id)
    
    metadata_sample.insert(3, 'isItAnUrlForImage', False)
    for index, row in metadata_sample.iterrows():
        if is_url_image(row['data']):
            metadata_sample.loc[index, 'isItAnUrlForImage'] = True


    return render_template("dataset_sample.html",dataset_name=dataset_name, 
    client_count=client_count,item_count=item_count,interaction_count=interaction_count,
    interaction_sample=interaction_sample,metadata_sample=metadata_sample)

def addDataset(request):
    datasetName = request.form.get('datasetname')
    interactionsCSV = request.files['csvinteractions']
    metadataCSV = request.files.getlist('csvmetadata')

    clientIdColumn = request.form.get('userIdColumn')
    itemIdColumn = request.form.get('itemIdColumn')
    timestampColumn = request.form.get('timestampColumn')

    datasetExists = datasetDB.datasetExists(datasetName, current_user.id)

    if interactionsCSV.content_type == 'text/csv' and not datasetExists and datasetName:
        # create pandas objects
        interactions = pd.read_csv(interactionsCSV)
        if timestampColumn not in interactions.columns and 'timestamp' not in interactions.columns:
            timestampColumn = 'tmstamp'
            interactions[timestampColumn] = '0001-01-01'

        columns = list(interactions.columns)
        if not (clientIdColumn in columns and itemIdColumn in columns and timestampColumn in columns):
            flash('Column doesn\'t exist in the csv file.')
            return
        
        if clientIdColumn == itemIdColumn or itemIdColumn == timestampColumn or timestampColumn == clientIdColumn:
            flash('There cannot be 2 columns with the same name.')
            return

        # insert dataset
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        dataset = Dataset(name=datasetName, usr_id=str(current_user.id), date_time=dt_string, private=True)
        dataset = datasetDB.add_dataset(dataset)

        #MAKE STRUCTURE FOR INTERACTIONS
        interactions = interactions.rename(columns={clientIdColumn: 'client_id', itemIdColumn: 'item_id', timestampColumn: 'tmstamp'})
        interactions = interactions[['client_id','item_id','tmstamp']]
        interactions.insert(0, 'dataset_id', dataset.id)

        #MAKE STRUCTURE ITEMS
        items = interactions[['item_id','dataset_id']]
        items.columns = ['id','dataset_id']
        items = items.drop_duplicates()

        #MAKE STRUCTURE CLIENTS
        clients = interactions[['client_id','dataset_id']]
        clients.columns = ['id','dataset_id']
        clients = clients.drop_duplicates()

        try:
            # insert items,clients and interactions
            itemDB.add_item(items)
            clientDB.add_client(clients)
            interactionDB.add_interaction(interactions)
        except:
            datasetDB.deleteDataset(dataset.name, current_user.id)
            flash('Unable to create the dataset.')
            return
            
        #insert metadata if exists
        if request.form.get('metadataCheck') == 'on':
            for mdata in metadataCSV:
                if mdata.filename:
                    if mdata.content_type == 'text/csv':
                        if not addMetadata(mdata, dataset, itemIdColumn):
                            return

        flash('Dataset succesfully added.')
    
    if not datasetName:
        flash('Please enter a name for the dataset.')
    elif datasetExists:
        flash('There already exists a dataset with the same name.')
    if interactionsCSV.content_type != 'text/csv':
        flash('Please select a csv file for the interactions.')

def addMetadata(metadataCSV, dataset, itemIdColumn):
    metadata = pd.read_csv(metadataCSV)
    columns = list(metadata.columns)
    if itemIdColumn not in columns:
        flash('Item id column doesn\'t exist in the metadata csv file.')
        return False

    newColumns = [itemIdColumn]
    for column in columns:
        if column and column != itemIdColumn:
            newColumns.append(column)

    metadata = metadata[newColumns]
    metadataOBJ = Metadata(dataset.id)
    try:
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
        
        #ADD EACH DESC TO METADATA INSERT INTO DATASET AND THEN REMOVE IT
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
        return True

    except:
        datasetDB.deleteDataset(dataset.name, current_user.id)
        flash('Unexpected error in the metadata, unable to create the dataset.')
        return False

def deleteDataset(request):
    name = request.form.get('datasetName')
    owner = int(request.form.get('owner'))
    dataset_id = request.form.get('dataset_id')
    if owner != current_user.id:
        datasetDB.unfollowDataset(current_user, dataset_id)
        flash('Dataset succesfully unfollowed.')
        return

    if datasetDB.datasetExists(name, current_user.id):
        datasetDB.deleteDataset(name,current_user.id)
        flash('Dataset succesfully deleted.')

def changeDatasetPublic(request):
    dataset_id = request.form.get('dataset_id')
    if datasetDB.datasetExistsById(dataset_id):
        if datasetDB.isPrivate(dataset_id):
            datasetDB.changePrivacy(current_user, dataset_id, False)

def changeDatasetPrivate(request):
    dataset_id = request.form.get('dataset_id')
    if datasetDB.datasetExistsById(dataset_id):
        if not datasetDB.isPrivate(dataset_id):
            datasetDB.changePrivacy(current_user, dataset_id, True)
    