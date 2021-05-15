class Dataset:
    def __init__(self, name, usr_id, date_time, private, id=None):
        self.id = id
        self.name = name
        self.usr_id = usr_id
        self.date_time = date_time
        self.private = private

class Item:
    def __init_(self,id,dataset_id):
        self.id = id
        self.dataset_id = dataset_id

class Metadata:
    def __init__(self,dataset_id,id=None):
        self.id=id
        self.dataset_id=dataset_id

class Scenario:
    def __init__(self, name, usr_id, date_time, dataset_id,item_min,item_max,client_min,client_max,time_min,time_max,cross_validation=False, id=None):
        self.name = name
        self.usr_id = usr_id
        self.date_time = date_time
        self.dataset_id = dataset_id
        self.id = id
        self.item_min=item_min
        self.item_max=item_max
        self.client_min=client_min
        self.client_max=client_max
        self.time_min=time_min
        self.time_max=time_max
        self.cross_validation = cross_validation

class Model:
    def __init__(self,usr_id,name,algorithm,scenario_id,date_time,parameters,id=None):
        self.id = id
        self.name = name
        self.usr_id = usr_id
        self.algorithm = algorithm
        self.scenario_id = scenario_id
        self.date_time = date_time
        self.parameters = parameters

class Experiment:
    def __init__(self,usr_id,name,model_id,date_time,retargeting,private,id=None):
        self.id = id
        self.usr_id = usr_id
        self.name = name
        self.model_id = model_id
        self.date_time = date_time
        self.retargeting = retargeting
        self.private = private

class Experiment_Client:
    def __init__(self, name, experiment_id, recommendations, history, expectations=None, id = None,):
        self.id = id
        self.name = name
        self.experiment_id = experiment_id
        self.history = history
        self.recommendations = recommendations
        self.expectations = expectations
        
