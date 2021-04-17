from views import *
import pickle

@views.route('/models',methods=['GET', 'POST'])
@login_required
def models():
    if request.method == 'POST' and request.form.get('which-form') == 'makeModel':
        modelName = request.form.get('modelName')
        scenarioName = request.form.get('scenarioSelect')
        algorithmName = request.form.get('algorithmName')

        scenario_id = scenarioDB.getScenarioID(scenarioName,current_user.id)
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        param = {}
        
        if algorithmName == 'ease':
            top_k_ease= request.form.get('top_k_ease')
            param['top_k_ease'] = top_k_ease
            if len(top_k_ease) == 0:
                    param['top_k_ease'] = '5'
            l2 = request.form.get('l2')
            param['l2'] = l2
            if len(l2) == 0:
                param['l2'] = '200.0'

        elif algorithmName == 'wmf':
            top_k_wmf= request.form.get('top_k_wmf')
            param['top_k_wmf'] = top_k_wmf
            if len(top_k_wmf) == 0:
                    param['top_k_wmf'] = '5'
            alpha = request.form.get('alpha')
            factors = request.form.get('factors')
            regularization = request.form.get('regularization')
            iterations = request.form.get('iterations')
            param['alpha'] = alpha
            param['factors'] = factors
            param['regularization'] = regularization
            param['iterations'] = iterations
            if len(alpha) == 0:
                param['alpha'] = '40.0'
            if len(factors) == 0:
                param['factors'] = '20'
            if len(regularization) == 0:
                param['regularization'] = '0.01'
            if len(iterations) == 0:
                param['iterations'] = '20'

        elif algorithmName == 'iknn':
            top_k_iknn= request.form.get('top_k_iknn')
            param['top_k_iknn'] = top_k_iknn
            if len(top_k_iknn) == 0:
                    param['top_k_iknn'] = '5'
            k = request.form.get('k')
            normalize = request.form.get('normalize')
            param['k'] = k
            param['normalize'] = normalize
            if len(k) == 0:
                param['k'] = '200'
        
        elif algorithmName == 'pop':
            top_k_pop = request.form.get('top_k_pop')
            param['top_k_pop'] = top_k_pop
            if len(top_k_pop) == 0:
                    param['top_k_pop'] = '5'

        parameters = []
        for dict_elem in param:
            parameters.append([dict_elem,param[dict_elem]])
        
        #generate df from scenario
        dfScenario = scenarioDB.getScenarioDataframe(scenario_id)
        #train algorithm 
        alg = trainAlgorithm(algorithmName,param, dfScenario) 
        #save model
        # for ease and iknn = similarity_matrix_ (matrix)
        # for wmf = model.item_factors (matrix)
        # for pop = item_counts (array)
        model = Model(usr_id=current_user.id,name=modelName,algorithm=algorithmName,scenario_id=scenario_id,parameters=parameters,date_time=dt_string)
        if algorithmName in ['ease', 'iknn']:
            modelDB.add_model(model, pickle.dumps(alg.similarity_matrix_))
        elif algorithmName == 'wmf':
            modelDB.add_model(model, pickle.dumps(alg.model.item_factors))
        elif algorithmName == 'pop':
            modelDB.add_model(model, pickle.dumps(alg.item_counts))

    models = modelDB.getModelsFromUser(current_user)
    for i in range(len(models)):
        scenarioName = scenarioDB.getScenarioName(models[i].scenario_id)
        models[i] = (i+1, models[i].name, scenarioName,models[i].algorithm, models[i].date_time)

    scenarios = scenarioDB.getScenariosFromUser(current_user)
    for i in range(len(scenarios)):
        scenarios[i] = (i+1, scenarios[i].name)

    return render_template("models.html", scenarios = scenarios,models=models)