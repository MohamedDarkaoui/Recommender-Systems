from views import *

@views.route('/experiments', methods=['GET', 'POST'])
@login_required
def experiments():

    #ADD EXPERIMENT
    if request.method == 'POST' and request.form.get('which-form') == "createExperiment":
        experimentName = request.form.get('experimentName')
        model_id = request.form.get('modelId')
        if len(experimentName) > 0  and model_id:
            model_id = int(model_id)
            dt_string = str(datetime.now().strftime("%Y/%m/%d %H:%M"))
            #add experiment
            newExperiment = Experiment(current_user.id, experimentName, model_id, dt_string)
            newExperiment = experimentDB.add_experiment(newExperiment)
    

    models = modelDB.getModelsFromUser(current_user)
    experiments = experimentDB.getExperimentsFromUser(current_user)
    for i in range(len(experiments)):
        experiments[i].model_id = modelDB.getModelName(experiments[i].model_id)
        experiments[i] = (i+1, experiments[i])

    return render_template("experiments.html", models = models, experiments = experiments)

@views.route('/experiments/experimentdata')
@login_required
def experimentdata():
    return render_template("experimentdata.html")