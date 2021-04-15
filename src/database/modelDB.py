from database.entitiesDB import Model

class ModelDB:
    def __init__(self, connection):
        self.connection = connection

    def add_model(self, ModelOBJ):
        cursor = self.connection.get_cursor()

        #'{{"helo","hello"},{"woter","water"}}'
        params = '{'
        for i in ModelOBJ.parameters:
            params += '{' + '"' + i[0] + ',' + i[1] + '"' + '},'
        params = params [:-1]
        params += '}'


        cursor.execute(
            'INSERT INTO Model (usr_id,name,algorithm,scenario_id,date_time,parameters) VALUES (%s,%s,%s,%s,%s,%s)', 
            (ModelOBJ.usr_id,ModelOBJ.name,ModelOBJ.algorithm,ModelOBJ.scenario_id,ModelOBJ.date_time,params,))
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
        cursor.execute('SELECT * FROM model WHERE usr_id = %s ORDER BY date_time', (id,))

        for row in cursor:
            scenario = Model(id=row[0],usr_id=row[1],name=row[2],algorithm=row[3],scenario_id=row[4],date_time=row[5],parameters=row[6])
            models.append(scenario)

        return models