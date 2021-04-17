from views import *

@views.route('/scenarios',methods=['GET', 'POST'])
@login_required
def scenarios():
    if request.method == 'POST' and request.form.get('which-form') == 'makeScenario':
        scenarioName = request.form.get('scenarioName')
        datasetName = request.form.get('datasetSelect')
        time1 = request.form.get('startDate')
        time2 = request.form.get('endDate')
        umin = request.form.get('user_min')
        umax = request.form.get('user_max')
        imin = request.form.get('item_min')
        imax = request.form.get('item_max')

        datasetID = datasetDB.getDatasetID(current_user.id,datasetName)

        if len(time1) == 0:
            time1 = '-infinity' 
        if len(time2) == 0:
            time2 = 'infinity'
        if len(umin) == 0:
            umin = '0'
        if len(umax) == 0:
            umax =  str(interactionDB.getCountInteractions(datasetID))
        if len(imin) == 0:
            imin = '0'
        if len(imax) == 0:
            imax = str(interactionDB.getCountInteractions(datasetID))

        if len(scenarioName) > 0 and len(datasetName) > 0:
            dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
            scenario = Scenario(name=scenarioName,usr_id=str(current_user.id),date_time=dt_string,dataset_id=datasetID,time_min=time1,time_max=time2,
            item_min=imin,item_max=imax,client_min=umin,client_max=umax)
            scenario = scenarioDB.add_scenario(scenario)
            scen_elem = scenarioDB.get_interactionsPD(datasetID, time1=time1, time2=time2, imin=imin, imax=imax, umin=umin, umax=umax)
            scen_elem.insert(0, 'scenario_id', scenario.id)
            print(scen_elem)
            scenarioDB.add_scenario_elements(scen_elem)
            
    
    scenarios = scenarioDB.getScenariosFromUser(current_user)
    for i in range(len(scenarios)):
        datasetName = datasetDB.getDatasetName(scenarios[i].dataset_id)
        scenarios[i] = (i+1, scenarios[i].name, datasetName, scenarios[i].date_time)

    
    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name)
    return render_template("scenarios.html", datasets = datasets,scenarios=scenarios)

@views.route('/scenarios/<scenario_name>')
@login_required
def scen_samples(scenario_name):

    scen_id = scenarioDB.getScenarioID(name=scenario_name,user_id=current_user.id)
    item_count = scenarioDB.getScenarioItemCount(scen_id)
    client_count = scenarioDB.getScenarioClientCount(scen_id)
    scenario_interactions_count = scenarioDB.getScenarioInteractionsCount(scen_id)
    scenario_sample = scenarioDB.getScenarioSample(scen_id)
    preprocessing = scenarioDB.getPreProcessingSteps(scen_id) 
    

    df = pd.DataFrame({})
    return render_template("scenario_sample.html",dataset_name=scenario_name,client_count=client_count,
    item_count=item_count,interaction_count=scenario_interactions_count,interaction_sample=scenario_sample,metadata_sample=df,preprocessing=preprocessing)