from entitiesDB.dataset import Dataset

class DatasetDB:
    def __init__(self, connection):
        self.connection = connection

    def add_dataset(self, dtsetOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO dataset (name,usr_id,date_time,private) VALUES (%s,%s,%s,%s)', 
                (dtsetOBJ.name,dtsetOBJ.usr_id,dtsetOBJ.date_time,dtsetOBJ.private),)
            cursor.execute('SELECT LASTVAL()')
            dtsetOBJ.id = cursor.fetchone()[0]
            self.connection.commit()
            return dtsetOBJ

        except:
            self.connection.rollback()
            raise Exception('Unable to save dataset: ' + dtsetOBJ.name)
    
    def delete_dataset(self):
        pass

    def get_dataset(self):
        pass
    
    def getDatasetsFromUser(self, usr):
        """
        returns a list of datasets that are created by usr
        """
        datasets = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT * FROM dataset WHERE usr_id = %s', (id,))

        for row in cursor:
            dataset = Dataset(id=row[0],name=row[1],usr_id=row[2],date_time=row[3],private=row[4])
            datasets.append(dataset)

        return datasets