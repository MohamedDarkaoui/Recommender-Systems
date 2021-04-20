from database.entitiesDB import Model
import pickle

class ModelDB:
    def __init__(self, connection):
        self.connection = connection

    def add_model(self, ModelOBJ, matrix):
        cursor = self.connection.get_cursor()
        #params = '{'
        #for i in ModelOBJ.parameters:
            #params += '{' + '"' + i[0] + ',' + i[1] + '"' + '},'
        #params = params [:-1]
        #params += '}'

        cursor.execute(
            'INSERT INTO Model (usr_id,name,algorithm,scenario_id,date_time,parameters,matrix) VALUES (%s,%s,%s,%s,%s,%s,%s)', 
            (ModelOBJ.usr_id,ModelOBJ.name,ModelOBJ.algorithm,ModelOBJ.scenario_id,ModelOBJ.date_time,ModelOBJ.parameters,matrix,))
        cursor.execute('SELECT LASTVAL()')
        ModelOBJ.id = cursor.fetchone()[0]
        self.connection.commit()
        return ModelOBJ

    def getModelsFromUser(self, usr):
        """
        returns a list of models that are created by usr
        """
        models = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT id,usr_id,name,algorithm,scenario_id,date_time,parameters FROM model WHERE usr_id = %s ORDER BY date_time', (id,))

        for row in cursor:
            model = Model(id=row[0],usr_id=row[1],name=row[2],algorithm=row[3],scenario_id=row[4],date_time=row[5],parameters=row[6])
            models.append(model)

        return models

    def getModelName(self, id):
        """
        returns the name of the model with id = id
        """
        cursor = self.connection.get_cursor()
        id = str(id)
        cursor.execute('SELECT name FROM model WHERE id = %s', (id,))
        result = cursor.fetchall()
        return result[0][0]
    
    def getScenarioIDFromModel(self, id):
        """
        returns an model object
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.scenario_id FROM model I
                                WHERE I.id = %s""",(id,))
            result = cursor.fetchall()
            return result[0][0]

        except:
            raise Exception('Unable to select the experiment')
    
    def getAlgorithmName(self, id):
        """
        returns an the name of the algorithm of the model with id = id
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.algorithm FROM model I
                                WHERE I.id = %s""",(id,))
            result = cursor.fetchall()
            return result[0][0]

        except:
            raise Exception('Unable to select the algorithm')

    def getMatrix(self, id):
        """
        returns the matrix of the model with id = id
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.matrix FROM model I
                                WHERE I.id = %s""",(id,))
            
            result = pickle.loads(cursor.fetchone()[0])
            return result

        except:
            raise Exception('Unable to select the algorithm')
    
    def deleteModel(self,name, user_id):
        """
        deletes model with the given name an user 
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM model 
                                WHERE name = %s
                                AND usr_id = %s;""", (name,user_id,))
            self.connection.commit()
        except:
            self.connection.rollback()
            print("fout")
    
    def modelExists(self, name, usr_id):
        """
            returns true if there exists a model with name = name and usr_id = usr_id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM model
                                WHERE name = %s
                                AND usr_id = %s;""", (name,usr_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()

    def getModelId(self, name, usr_id):
        """
            returns the id of a model with name = name and usr_id = usr_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM model
                                WHERE name = %s
                                AND usr_id = %s;""", (name,usr_id,))

            result = cursor.fetchone()
            return result[0]
        except:
            self.connection.rollback()