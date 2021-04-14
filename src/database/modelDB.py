from database.entitiesDB import Model

class ModelDB:
    def __init__(self, connection):
        self.connection = connection

    def add_Model(self, ModelOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO Model (usr_id,name,algorithm,scenario_id,date_time) VALUES (%s,%s,%s,%s,%s)', 
                (ModelOBJ.usr_id,ModelOBJ.name,ModelOBJ.algorithm,ModelOBJ.scenario_id,ModelOBJ.date_time),)
            cursor.execute('SELECT LASTVAL()')
            ModelOBJ.id = cursor.fetchone()[0]
            self.connection.commit()
            return ModelOBJ

        except:
            self.connection.rollback()
            raise Exception('Unable to save Model: ' + ModelOBJ.name)