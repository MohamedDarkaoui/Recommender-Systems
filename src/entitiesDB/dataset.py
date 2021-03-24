class Dataset:
    def __init__(self, id, name, usr_id, private):
        self.id = id
        self.name = name
        self.usr_id = usr_id
        self.private = private


class Item:
    def __init_(self,id,dataset_id):
        self.id = id
        self.dataset_id = dataset_id