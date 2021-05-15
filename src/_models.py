from views import *
import pickle

@views.route('/models',methods=['GET', 'POST'])
@login_required
def models():
    if request.method == 'POST':
        if request.form.get('which-form') == 'makeModel':
            makeModel(request)

        elif request.form.get('which-form') == 'deleteModel':
            deleteModel(request)

    models = modelDB.getModelsFromUser(current_user)
    for i in range(len(models)):
        scenarioName = scenarioDB.getScenarioName(models[i].scenario_id)
        models[i] = (i+1, models[i].name, scenarioName,models[i].algorithm, models[i].date_time)

    scenarios = scenarioDB.getScenariosFromUser(current_user)
    for i in range(len(scenarios)):
        scenarios[i] = (i+1, scenarios[i].name)

    return render_template("models.html", scenarios = scenarios,models=models)

def deleteModel(request):
    modelName = request.form.get('modelName')
    existsModel = modelDB.modelExists(modelName, current_user.id)
    if existsModel:
        modelDB.deleteModel(modelName, current_user.id)

    flash("Model succesfully deleted.")
    

def makeModel(request):
    modelName = request.form.get('modelName')
    scenarioName = request.form.get('scenarioSelect')
    algorithmName = request.form.get('algorithmName')
    dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
    param = {}

    existsScenario = scenarioDB.scenarioExists(scenarioName, current_user.id)
    existsModel = modelDB.modelExists(modelName, current_user.id)

    if existsScenario and modelName and not existsModel and algorithmName:
        scenario_id = scenarioDB.getScenarioID(scenarioName, current_user.id)
        interactionCount = int(scenarioDB.getScenarioInteractionsCount(scenario_id))
        if interactionCount == 0:
            flash('It is not possible to make a model with an empty scenario.')
            return
            
        if algorithmName == 'ease':
            param['l2'] = request.form.get('L2')
            if not param['l2']:
                param['l2'] = '200.0'

        elif algorithmName == 'wmf':
            param['alpha'] = request.form.get('alpha')
            param['factors'] = request.form.get('factors')
            param['regularization'] = request.form.get('regularization')
            param['iterations'] = request.form.get('iterations')

            if not param['alpha']:
                param['alpha'] = '40.0'
            if not param['factors']:
                param['factors'] = '20'
            if not param['regularization']:
                param['regularization'] = '20'
            if not param['iterations']:
                param['iterations'] = '0.01'

        elif algorithmName == 'iknn':
            param['k'] = request.form.get('k')
            param['normalize'] = request.form.get('normalize')
            if not param['k']:
                param['k'] = '40.0'
            if not param['normalize']:
                param['normalize'] = 'false'
        
        elif algorithmName == 'pop':
            pass

        parameters = []
        for dict_elem in param:
            parameters.append([dict_elem,param[dict_elem]])
        
        #generate df from scenario
        dfScenario = scenarioDB.getScenarioDataframe(scenario_id)

        #train algorithm 
        alg = None
        if scenarioDB.has_cross_validation(scenarioName,current_user.id):
            train = scenarioDB.getTrain(scenario_id)
            alg = trainAlgorithm(algorithmName,param, dfScenario,train)
        else:
            alg = trainAlgorithm(algorithmName,param, dfScenario) 

        #save model
        model = Model(usr_id=current_user.id,name=modelName,algorithm=algorithmName,scenario_id=scenario_id,parameters=parameters,date_time=dt_string)
        if algorithmName in ['ease', 'iknn']:
            modelDB.add_model(model, pickle.dumps(alg.similarity_matrix_))
        elif algorithmName == 'wmf':
            modelDB.add_model(model, pickle.dumps(alg.model.item_factors))
        elif algorithmName == 'pop':
            modelDB.add_model(model, pickle.dumps(alg.item_counts))
        
        flash('Model succesfully made')
        return
    
    if not modelName:
        flash('Please enter a name for the model.')
    if existsModel:
        flash('There already exists a model with the given name.')
        
    if not scenarioName:
        flash('Please select a scenario.')

    elif not existsScenario:
        flash('The selected scenario doesnt exist anymore')
        
    if not algorithmName:
        flash('Please select an algorithm.')

