
from flask.globals import current_app
from database.scenarioDB import ScenarioDB
from views import *

top_k = 20

@views.route('/experiments', methods=['GET', 'POST'])
@login_required
def experiments():
    #ADD EXPERIMENT    
    if request.method == 'POST':
        if request.form.get('which-form') == "createExperiment":
            makeExperiment(request)
        elif request.form.get('which-form') == 'deleteExperiment':
            deleteExperiment(request)
        elif request.form.get('which-form') == 'makePublic':
            changeExperimentPublic(request)
        elif request.form.get('which-form') == 'makePrivate':
            changeExperimentPrivate(request)

    models = modelDB.getModelsFromUser(current_user)
    experiments = experimentDB.getExperimentsFromUser(current_user)
    for i in range(len(experiments)):
        experiments[i].model_id = modelDB.getModelName(experiments[i].model_id)
        experiments[i] = (i+1, experiments[i], True)

    followedExperiments = experimentDB.getFollowedExperiments(current_user)
    for i in range(len(followedExperiments)):
        owner = Users.query.filter_by(id=followedExperiments[i].usr_id).first()
        followedExperiments[i].model_id = modelDB.getModelName(followedExperiments[i].model_id) + ' (' + owner.username + ')'
        followedExperiments[i] = (i+len(followedExperiments)+1, followedExperiments[i], False)

    return render_template("experiments.html", models = models, experiments = experiments + followedExperiments)

@views.route('/experiments/<experiment_id>', methods=['GET', 'POST'])
@login_required
def experimentdata(experiment_id):
    try:
        experiment_id=int(experiment_id)
    except:
        return redirect(url_for('views.experiments'))

    if not experimentDB.experimentExistsById(experiment_id):
        return redirect(url_for('views.experiments'))

    experiment = experimentDB.getExperimentById(experiment_id)
    if experiment.usr_id != current_user.id and not experimentDB.followsExperiment(current_user, experiment_id):
        return redirect(url_for('views.experiments'))
    
    scenario_id = modelDB.getScenarioIDFromModel(experiment.model_id)
    dataset_id = scenarioDB.getDatasetID(scenario_id)
    clientsFromScenario = scenarioDB.getAllClients(scenario_id)
    itemsFromScenario = scenarioDB.getAllItems(scenario_id)
    scenarioName = scenarioDB.getScenarioName(scenario_id)

    if request.method == 'POST':
        if request.form.get('which-form') == 'addClient':
            algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
            maxItemId = scenarioDB.getMaxItem(scenario_id)
            parameters = modelDB.getParameters(experiment.model_id)
            if scenarioDB.has_cross_validation(scenarioName, current_user.id):
                parameters = modelDB.getParameters(experiment.model_id)
                algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
               

                maxItemId = scenarioDB.getMaxItem(scenario_id)
                parameters = modelDB.getParameters(experiment.model_id)
                algorithmName = modelDB.getAlgorithmName(experiment.model_id)
                addExperimentClient(request, experiment, scenario_id, algorithmName, maxItemId, parameters, len(itemsFromScenario),True)
            
            else:
                addExperimentClient(request, experiment, scenario_id, algorithmName, maxItemId, parameters, len(itemsFromScenario))

        elif request.form.get('which-form') == 'deleteClient':
            deleteExperimentClient(request, experiment.id)

        elif request.form.get('which-form') == 'deleteItem':
            parameters = modelDB.getParameters(experiment.model_id)
            algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id), parameters)
            maxItemId = scenarioDB.getMaxItem(scenario_id)
            deleteItem(request, experiment.id, alg, maxItemId, algorithmName, len(itemsFromScenario), experiment.retargeting)

        elif request.form.get('which-form') == 'addItem':
            parameters = modelDB.getParameters(experiment.model_id)
            algorithmName = modelDB.getAlgorithmName(experiment.model_id) 
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id), parameters)
            maxItemId = scenarioDB.getMaxItem(scenario_id)
            addItem(request, experiment.id, alg, maxItemId, algorithmName, len(itemsFromScenario), experiment.retargeting)
        
        elif request.form.get('which-form') == 'showItemMetadata':
            return itemMetadata(request,dataset_id)

    clients = experimentDB.getExperimentClients(experiment.id)
    return render_template("experimentdata.html", clients=clients, clientsFromScenario = clientsFromScenario, itemsFromScenario=itemsFromScenario, scenario_id=scenario_id)

@views.route('/experiments/metadata/<scenario_id>/<item_id>', methods=['GET', 'POST'])
@login_required
def itemMetadata(scenario_id,item_id):
    dataset_id = scenarioDB.getDatasetID(scenario_id)
    metadataPD = metadataElementDB.getItemMetadata(item_id, dataset_id)
    return render_template("metadata_experiment.html", metadata=metadataPD, item_id=item_id)
    
def makeExperiment(request):
    experimentName = request.form.get('experimentName')
    modelName = request.form.get('modelName')
    experimentExists = experimentDB.experimentExists(experimentName, current_user.id)
    modelExists = modelDB.modelExists(modelName, current_user.id)
    retargeting = False
    if request.form.get('retargetingCheck') == 'on':
        retargeting = True

    if modelExists and not experimentExists and experimentName:
        modelId = int(modelDB.getModelId(modelName, current_user.id))
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        #add experiment
        newExperiment = Experiment(current_user.id, experimentName, modelId, dt_string, retargeting, True)
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
    experiment_id = int(request.form.get("experiment_id"))
    usr_id = int(request.form.get("experiment_id"))

    if usr_id != current_user.id:
        experimentDB.unfollowExperiment(current_user, experiment_id)
        flash('Experiment succesfully unfollowed.')
        return

    if experimentDB.experimentExistsById(experiment_id):
        experimentDB.deleteExperimentById(experiment_id)
        flash('Experiment succesfully deleted.')

def addExperimentClient(request, experiment, scenario_id, algorithmName, maxItemId, parameters, itemCount, cv = False):
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
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id), parameters)

            #predict call
            predictions = alg.predict(historyMatrix)
            recommendations, scores = util.predictions_to_recommendations(predictions, top_k=itemCount)
            recommendations = recommendations[0].tolist()
            if algorithmName == 'ease':
                recommendations = recommendations[0]

            recommendations = retargetingFilter(recommendations, history, experiment.retargeting)

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
            alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id), parameters)

            for index, client in enumerate(listOfClients):
                historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
                history = scenarioDB.getClientHistory(scenario_id,client)
                for item in history:
                    historyMatrix[0, item] = 1

                #predict call
                predictions = alg.predict(historyMatrix)
                recommendations, scores = util.predictions_to_recommendations(predictions, top_k=itemCount)
                recommendations = recommendations[0].tolist()
                if algorithmName == 'ease':
                    recommendations = recommendations[0]
                
                recommendations = retargetingFilter(recommendations, history, experiment.retargeting)

                #add client
                newClientName = clientName + '#' + str(index+1)
                newClient = Experiment_Client(newClientName, experiment.id, recommendations, history)
                experimentDB.addExperimentClient(newClient)

        elif type == 'validation-in':
            if cv:
                alg = createAlgorithm(algorithmName, modelDB.getMatrix(experiment.model_id), parameters)
                val_in = scenarioDB.getValIn(scenario_id)
                val_out = scenarioDB.getValOut(scenario_id)
                clients = list(range(val_in.shape[0])) #list of numbers from 0 to #clients
                histories = val_in[clients, :]
                expectations = val_out[clients, :]
                predictions = alg.predict(histories)
                predictions2 = alg.predict(val_in)
                recommendations, scores = util.predictions_to_recommendations(predictions, top_k=top_k)
                """
                for index, u in enumerate(clients):
                    clientName = "Client" + str(u)
                    History = list(np.where(histories[index].toarray().flatten())[0].tolist())
                    recommendation = recommendations[index].tolist()
                    expectation = list(np.where(expectations[index].toarray().flatten())[0].tolist())
                    score = scores[index].tolist()
                """
                rand = randint(0,len(clients)-1)
                history = list(np.where(histories[rand].toarray().flatten())[0].tolist())
                recommendation = recommendations[rand].tolist()
                expectation = list(np.where(expectations[rand].toarray().flatten())[0].tolist())
                score = scores[rand].tolist()
                if algorithmName == 'ease':
                        recommendation = recommendation[0]

                recommendation = retargetingFilter(recommendation, history, experiment.retargeting)

                if experimentDB.counter < len(clients):
                    experimentDB.counter += 1
                else:
                    experimentDB.counter = 0
                maxItemId = scenarioDB.getMaxItem(scenario_id)
                newClient = Experiment_Client(clientName, experiment.id, recommendation, history, expectation)
                experimentDB.addExperimentClient(newClient)
            else:
                flash('Cross-validation is not enabeled')
                return

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
    
def createAlgorithm(name, matrix, parameters):
    alg = None
    if name == 'ease':
        from Algorithms.src.algorithm.ease import EASE
        l2 = float(parameters[0][1])
        alg = EASE(l2 = l2)
        alg.similarity_matrix_ = matrix

    elif name == 'iknn':
        from Algorithms.src.algorithm.item_knn import ItemKNN
        k = int(parameters[0][1])
        normalize = False
        if parameters[1][1] == 'true':
            normalize = True
        alg = ItemKNN(k = k, normalize=normalize)

        alg.similarity_matrix_ = matrix
        
    elif name == 'pop':
        from Algorithms.src.algorithm.popularity import Popularity
        alg = Popularity()
        alg.item_counts = matrix
        
    elif name == 'wmf':
        from Algorithms.src.algorithm.wmf import WMF
        alpha = float(parameters[0][1])
        factors = int(parameters[1][1])
        regularization = float(parameters[2][1])
        iterations = int(parameters[3][1])
        alg = WMF(alpha=alpha, num_factors=factors, regularization=regularization, iterations=iterations)
        alg.model = alg.create_model()
        alg.model.item_factors = matrix
    
    return alg

def deleteItem(request, experiment_id, alg, maxItemId, algorithmName, itemCount, retargeting):
    clientName = request.form.get('clientName')
    if experimentDB.experimentClientExists(clientName, experiment_id):
        itemId = int(request.form.get('itemId'))
        client = experimentDB.getExperimentClient(clientName, experiment_id)

        if itemId in client.history:
            client.history.remove(itemId)
        
        historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
        for item in client.history:
            historyMatrix[0, item] = 1
        
        #predictCall
        predictions = alg.predict(historyMatrix)
        recommendations, scores = util.predictions_to_recommendations(predictions, top_k=itemCount)
        recommendations = recommendations[0].tolist()
        if algorithmName == 'ease':
            recommendations = recommendations[0]
        
        recommendations = retargetingFilter(recommendations, client.history, retargeting)
        experimentDB.updateExperimentClient(clientName, experiment_id, client.history, recommendations)
        flash('Item removed.')

def addItem(request, experiment_id, alg, maxItemId, algorithmName, itemCount, retargeting):
    clientName = request.form.get('clientName')
    if experimentDB.experimentClientExists(clientName, experiment_id):
        if not request.form.get('itemId'):
            flash('Please select an item to be added.')
            return

        itemId = int(request.form.get('itemId'))
        client = experimentDB.getExperimentClient(clientName, experiment_id)

        if itemId in client.history:
            flash('Item is already in the history.')
            return

        client.history.append(itemId)        
        historyMatrix = scipy.sparse.csr_matrix((1, maxItemId+1), dtype=np.int8)
        for item in client.history:
            historyMatrix[0, item] = 1
        
        #predictCall
        predictions = alg.predict(historyMatrix)
        recommendations, scores = util.predictions_to_recommendations(predictions, top_k=itemCount)
        recommendations = recommendations[0].tolist()
        if algorithmName == 'ease':
            recommendations = recommendations[0]

        recommendations = retargetingFilter(recommendations, client.history, retargeting)
        experimentDB.updateExperimentClient(clientName, experiment_id, client.history, recommendations)
        flash('Item added.')

def retargetingFilter(recommendations, history, retargeting):

    items = []
    duplicates = []
    if not retargeting:
        for item in recommendations:
            if item in history:
                duplicates.append(item)
    
    for item in duplicates:
        recommendations.remove(item)
    
    if len(recommendations) > top_k:
        return recommendations[:top_k]

    return recommendations

def changeExperimentPublic(request):
    experiment_id = request.form.get('experiment_id')
    if experimentDB.experimentExistsById(experiment_id):
        if experimentDB.isPrivate(experiment_id):
            experimentDB.changePrivacy(experiment_id, False)

def changeExperimentPrivate(request):
    experiment_id = request.form.get('experiment_id')
    if experimentDB.experimentExistsById(experiment_id):
        if not experimentDB.isPrivate(experiment_id):
            experimentDB.changePrivacy(experiment_id, True)