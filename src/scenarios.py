from views import *

@views.route('/scenarios',methods=['GET', 'POST'])
@login_required
def scenarios():
    if request.method == 'POST':     
        if request.form.get('which-form') == 'makeScenario':
            #try:
                df = makeScenario(request)
                df.drop('tmstamp', inplace=True, axis=1)
                df.drop('scenario_id', inplace=True, axis=1)
                clients = df['client_id']
                clients = clients.drop_duplicates()
                if request.form.get('cross_validation') == 'on':
                    X = util.df_to_csr(df)
                    if request.form.get('flexRadioDefault') == 's_generalization':
                        test_users = int(request.form.get('testUsers'))
                        perc_history = float(request.form.get('percHistory'))
                        train, val_in, val_out = strong_generalization(X,test_users,perc_history,clients)

                        print('train', train)
                        print('val_in', val_in)
                        print('val_out', val_out)
                    elif request.form.get('flexRadioDefault') == 'w_generalization':
                        pass
            
            #except:
             #   flash('Something went wrong, please fill in all the mandatory fields, deleteng scenario')
              #  deleteScenario(request)
        elif request.form.get('which-form') == 'deleteScenario':
            deleteScenario(request)
            flash('Scenario succesfully deleted.')
        
            

    scenarios = scenarioDB.getScenariosFromUser(current_user)
    for i in range(len(scenarios)):
        dataset = datasetDB.getDatasetById(scenarios[i].dataset_id)
        if dataset.usr_id != current_user.id:
            dataset.name += ' (' + Users.query.filter_by(id=dataset.usr_id).first().username + ')'

        scenarios[i] = (i+1, scenarios[i].name, dataset.name, scenarios[i].date_time)

    
    datasets = datasetDB.getDatasetsFromUser(current_user)
    for i in range(len(datasets)):
        datasets[i] = (i+1, datasets[i].name, datasets[i].id)


    followedDatasets = datasetDB.getFollowedDatasets(current_user)
    for i in range(len(followedDatasets)):
        owner = Users.query.filter_by(id=followedDatasets[i].usr_id).first()
        followedDatasets[i] = (i+len(datasets)+1, followedDatasets[i].name + ' (' + owner.username + ')', followedDatasets[i].id)


    return render_template("scenarios.html", datasets=datasets+followedDatasets, scenarios=scenarios)

@views.route('/scenarios/<scenario_name>')
@login_required
def scen_samples(scenario_name):
    if scenarioDB.scenarioExists(scenario_name, current_user.id):
        scen_id = scenarioDB.getScenarioID(name=scenario_name,user_id=current_user.id)
        item_count = scenarioDB.getScenarioItemCount(scen_id)
        client_count = scenarioDB.getScenarioClientCount(scen_id)
        scenario_interactions_count = scenarioDB.getScenarioInteractionsCount(scen_id)
        scenario_sample = scenarioDB.getScenarioSample(scen_id)
        preprocessing = scenarioDB.getPreProcessingSteps(scen_id) 
        return render_template("scenario_sample.html",dataset_name=scenario_name,client_count=client_count,
        item_count=item_count,interaction_count=scenario_interactions_count,interaction_sample=scenario_sample,preprocessing=preprocessing)
    else:
        return redirect(url_for('views.scenarios'))

    
def makeScenario(request):
    scenarioName = request.form.get('scenarioName')
    datasetID = int(request.form.get('datasetSelect'))
    time1 = request.form.get('startDate')
    time2 = request.form.get('endDate')
    umin = request.form.get('user_min')
    umax = request.form.get('user_max')
    imin = request.form.get('item_min')
    imax = request.form.get('item_max')

    existsDataset = datasetDB.datasetExistsById(datasetID)
    existsScenario = scenarioDB.scenarioExists(scenarioName, current_user.id)
    scen_elem = None
    if existsDataset and scenarioName and not existsScenario:
        #SET DEFAULT FILTERS IF NOT GIVEN
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
        
        dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
        scenario = Scenario(name=scenarioName,usr_id=str(current_user.id),date_time=dt_string,dataset_id=datasetID,time_min=time1,time_max=time2,
        item_min=imin,item_max=imax,client_min=umin,client_max=umax)
        scenario = scenarioDB.add_scenario(scenario)
        
        scen_elem = scenarioDB.get_interactionsPD(datasetID, time1=time1, time2=time2, imin=imin, imax=imax, umin=umin, umax=umax)
        scen_elem.insert(0, 'scenario_id', scenario.id)
        scenarioDB.add_scenario_elements(scen_elem)
        flash('Scenario succesfully made.')
    
    if not scenarioName:
        flash('Please enter a name for the scenario.')
    if existsScenario:
        flash('There already exists a scenario with the given name.')
    if not datasetID:
        flash('Please select a dataset.')
    elif not existsDataset:
        flash('The selected dataset doesnt exist anymore')

    return scen_elem

def deleteScenario(request):
    scenarioName = request.form.get('scenarioName')
    print(scenarioName)
    if scenarioDB.scenarioExists(scenarioName, current_user.id):
        scenario_id = scenarioDB.getScenarioID(scenarioName, current_user.id)
        scenarioDB.deleteScenario(scenario_id)
        
