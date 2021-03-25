
class DatasetDB:
    def __init__(self, connection):
        self.connection = connection

    def add_dataset(self, dtsetOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute('INSERT INTO dataset VALUES (%s,%s,%s,%s)', (dtsetOBJ.id, dtsetOBJ.name,dtsetOBJ.usr_id,dtsetOBJ.private))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save dataset: ' + dtsetOBJ.name)
    
    def delete_dataset(self):
        pass

    def get_dataset(self):
        pass
    
    def getDatasetsFromUser(self, user_id):


        #return [list of dataset objecten]
        pass
