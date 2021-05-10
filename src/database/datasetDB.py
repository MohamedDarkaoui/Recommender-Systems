from database.entitiesDB import Dataset

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

    def getDatasetID(self,usr_id,name):
        """
        returns the ID of the dataset with the given name that belongs to the given user
        """

        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT D.id FROM dataset D
                                WHERE D.usr_id = %s
                                AND D.name = %s """,(usr_id, name))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the ID of the dataset')

    def getDatasetName(self,id):
        """
        returns the name of the dataset with the given ID that belongs to the current user
        """

        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT D.name FROM dataset D
                                WHERE D.id =  %s """,(id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the name of the dataset')

    def deleteDataset(self,name,user_id):
        """
        deletes a dataset with the given name and user id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM dataset
                                WHERE name = %s
                                AND usr_id = %s;""", (name,user_id,))
            self.connection.commit()
        except:
            self.connection.rollback()
            print("fout")

    def datasetExists(self, name, usr_id):
        """
            returns true if there exists a dataset with name = name and usr_id = usr_id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM dataset
                                WHERE name = %s
                                AND usr_id = %s;""", (name,usr_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()
    
    def datasetExistsById(self, id):
        """
            returns true if there exists a dataset with id=id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM dataset
                                WHERE id = %s;""", (id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()