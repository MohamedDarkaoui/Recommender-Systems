from entities import Scenario

class scenarioDB:
    def __init__(self, connection):
        self.connection = connection
    


    def add_scenario(self, scenarioOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO scenario (name,usr_id,date_time,dataset_id) VALUES (%s,%s,%s,%s)', 
                (scenarioOBJ.name,scenarioOBJ.usr_id,scenarioOBJ.date_time, scenarioOBJ.dataset_id),)
            cursor.execute('SELECT LASTVAL()')
            scenarioOBJ.id = cursor.fetchone()[0]
            self.connection.commit()
            return scenarioOBJ

        except:
            self.connection.rollback()
            raise Exception('Unable to save scenario: ' + scenarioOBJ.name)

    def get_interactionsPD(self,date1,date2,imin,imax,umin,umax):
        pass
    '''
        cursor = self.connection.get_cursor()
        cursor.execute(
            'SELECT * FROM interaction WHERE  = %s', 
            (id,))
    '''        