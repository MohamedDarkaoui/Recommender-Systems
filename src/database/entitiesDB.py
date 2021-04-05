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
    def __init__(self, name, usr_id, date_time, dataset_id, id=None):
        self.name = name
        self.usr_id = usr_id
        self.date_time = date_time
        self.dataset_id = dataset_id
        self.id = id


