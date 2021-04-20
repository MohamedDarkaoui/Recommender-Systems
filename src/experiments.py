from database.scenarioDB import ScenarioDB
from views import *


@views.route('/experiments', methods=['GET', 'POST'])
@login_required
def experiments():
    #ADD EXPERIMENT    
    if request.method == 'POST':
        if request.form.get('which-form') == "createExperiment":
            makeExperiment(request)

        elif request.form.get('which-form') == 'deleteExperiment':
            deleteExperiment(request)

    models = modelDB.getModelsFromUser(current_user)
    experiments = experimentDB.getExperimentsFromUser(current_user)
    for i in range(len(experiments)):
        experiments[i].model_id = modelDB.getModelName(experiments[i].model_id)
        experiments[i] = (i+1, experiments[i])

    return render_template("experiments.html", models = models, experiments = experiments)

@views.route('/experiments/<experiment_name>', methods=['GET', 'POST'])
@login_required
def experimentdata(experiment_name):
    if not experimentDB.experimentExists(experiment_name, current_user.id):
        return redirect(url_for('views.experiments'))

    experiment = experimentDB.getExperimentByName(experiment_name, current_user.id)
    scenario_id = modelDB.getScenarioIDFromModel(experiment.model_id)
    clientsFromScenario = scenarioDB.getAllClients(scenario_id)
    itemsFromScenario = scenarioDB.getAllItems(scenario_id)

    if request.method == 'POST':
        if request.form.get('which-form') == 'addClient':
            algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
            maxItemId = scenarioDB.getMaxItem(scenario_id)
            addExperimentClient(request, experiment, scenario_id, algorithmName, maxItemId)

        elif request.form.get('which-form') == 'deleteClient':
            deleteExperimentClient(request, experiment.id)

        elif request.form.get('which-form') == 'deleteItem':
            algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id))
            maxItemId = scenarioDB.getMaxItem(scenario_id)
            deleteItem(request, experiment.id, alg, maxItemId, algorithmName)

    clients = experimentDB.getExperimentClients(experiment.id)
    return render_template("experimentdata.html", clients=clients, clientsFromScenario = clientsFromScenario, itemsFromScenario=itemsFromScenario)
    
def makeExperiment(request):
    experimentName = request.form.get('experimentName')
    modelName = request.form.get('modelName')

    experimentExists = experimentDB.experimentExists(experimentName, current_user.id)
    modelExists = modelDB.modelExists(modelName, current_user.id)

    if modelExists and not experimentExists and experimentName:
        modelId = int(modelDB.getModelId(modelName, current_user.id))
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        #add experiment
        newExperiment = Experiment(current_user.id, experimentName, modelId, dt_string)
        newExperiment = experimentDB.add_experiment(newExperiment)
        flash("Experiment succesfully made.")
        return

    if not experimentName:
        flash('Please enter a name for the experiment.')
    if experimentExists:
        flash('There exists a experiment with the same name.')
    if not modelName:
        flash('Please select a model.')
    elif not modelExists:
        flash('Selected model doesnt exists anymore.')

def deleteExperiment(request):
    experimentName = request.form.get("experimentName")
    if experimentDB.experimentExists(experimentName, current_user.id):
        experimentDB.deleteExperiment(experimentName,current_user.id)
    flash('Experiment succesfully deleted.')

def addExperimentClient(request, experiment, scenario_id, algorithmName, maxItemId):
    clients = experimentDB.getExperimentClients(experiment.id)
    clientName = request.form.get('clientName')
    existsClient = experimentDB.experimentClientExists(clientName, experiment.id)
    if clientName and not existsClient:
        type = request.form.get('flexRadioDefault')
        if type in ['emptyClient', 'randomClient', 'isCopyFromScenario', 'randomItems']:
            history = []
            historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
        
            if type == 'emptyClient':
                pass
            elif type == 'randomClient':
                client = scenarioDB.getRandomClient(scenario_id)
                history = scenarioDB.getClientHistory(scenario_id,client)
                for item in history:
                    historyMatrix[0, item] = 1

            elif type == 'randomItems':
                #read amount
                amount = request.form.get('amountItems')
                if not amount:
                    flash('Please enter an amount of items.')
                    return
                    
                history = scenarioDB.getRandomItems(scenario_id, amount)
                for item in history:
                    historyMatrix[0, item] = 1

            elif type == 'isCopyFromScenario':
                copyClientId = request.form.get('copyClientId')
                if not copyClientId:
                    flash('Please select a client.')
                    return
                history = scenarioDB.getClientHistory(scenario_id, copyClientId)               
                for item in history:
                    historyMatrix[0, item] = 1
            
            #create algorithm
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id))

            #predict call
            predictions = alg.predict(historyMatrix)
            recommendations, scores = util.predictions_to_recommendations(predictions, top_k=20)
            recommendations = recommendations[0].tolist()
            if algorithmName == 'ease':
                recommendations = recommendations[0]

            #add client
            newClient = Experiment_Client(clientName, experiment.id, recommendations, history)
            experimentDB.addExperimentClient(newClient)

        elif type == 'isCopyFromExperiment':
            copyClientName = request.form.get('copyClientName')
            if not copyClientName:
                flash('Please select a client.')
                return

            for client in clients:
                if client.name == copyClientName:
                    newClient = client
                    newClient.name = clientName
                    experimentDB.addExperimentClient(newClient)

        elif type == 'allClientsWithItem':
            itemId = request.form.get('fromItemId')
            if not itemId:
                flash('Please select a client.')
                return

            listOfClients = scenarioDB.getAllClientsWithItem(scenario_id, itemId)
            #create algorithm
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id))

            for index, client in enumerate(listOfClients):
                historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
                history = scenarioDB.getClientHistory(scenario_id,client)
                for item in history:
                    historyMatrix[0, item] = 1

                #predict call
                predictions = alg.predict(historyMatrix)
                recommendations, scores = util.predictions_to_recommendations(predictions, top_k=20)
                recommendations = recommendations[0].tolist()
                if algorithmName == 'ease':
                    recommendations = recommendations[0]

                #add client
                newClientName = clientName + '#' + str(index+1)
                newClient = Experiment_Client(newClientName, experiment.id, recommendations, history)
                experimentDB.addExperimentClient(newClient)

        flash('Experiment client succesfully made.')

    elif not clientName:
        flash('Please enter a name for the client.')
    
    elif existsClient:
        flash('There already exists a client with the given name.')

def deleteExperimentClient(request, experiment_id):
    name = request.form.get('clientName')
    if experimentDB.experimentClientExists(name, experiment_id):
        experimentDB.deleteExperimentClient(name, experiment_id)

    flash('Experiment client succesfully deleted.')
    
def createAlgorithm(name, matrix):
    alg = None
    if name == 'ease':
        from Algorithms.src.algorithm.ease import EASE
        alg = EASE()
        alg.similarity_matrix_ = matrix

    elif name == 'iknn':
        from Algorithms.src.algorithm.item_knn import ItemKNN
        alg = ItemKNN()
        alg.similarity_matrix_ = matrix
        
    elif name == 'pop':
        from Algorithms.src.algorithm.popularity import Popularity
        alg = Popularity()
        alg.item_counts = matrix
        
    elif name == 'wmf':
        from Algorithms.src.algorithm.wmf import WMF
        alg = WMF()
        alg.model = alg.create_model()
        alg.model.item_factors = matrix
    
    return alg

def deleteItem(request, experiment_id, alg, maxItemId, algorithmName):
    clientName = request.form.get('clientName')
    if experimentDB.experimentClientExists(clientName, experiment_id):
        itemId = int(request.form.get('itemId'))
        client = experimentDB.getExperimentClient(clientName, experiment_id)

        client.history
        if itemId in client.history:
            client.history.remove(itemId)
        
        historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
        for item in client.history:
            historyMatrix[0, item] = 1
        
        #predictCall
        predictions = alg.predict(historyMatrix)
        recommendations, scores = util.predictions_to_recommendations(predictions, top_k=20)
        recommendations = recommendations[0].tolist()
        if algorithmName == 'ease':
            recommendations = recommendations[0]
        
        experimentDB.updateExperimentClient(clientName, experiment_id, client.history, recommendations)
        flash('Item removed.')


