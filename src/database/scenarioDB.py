from database.entitiesDB import Scenario
from pandas import DataFrame

class ScenarioDB:
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

    def get_interactionsPD(self, dataset_id, time1, time2, imin, imax, umin,umax):   

        print('-------------------LMAO----------------------------------')
        cursor = self.connection.get_cursor()
        cursor.execute(
        """ select id from subset_for_scenario (%s, %s, %s) 
        natural join subset_for_scenario_client (%s, %s, %s,%s,%s)
        natural join subset_for_scenario_item (%s, %s, %s,%s,%s)""",
        (time1,time2,dataset_id,time1,time2,dataset_id,umin,umax,time1,time2,dataset_id,imin,imax))

        print('--------------LMAO---------------------------')
        ids = cursor.fetchall()
        interaction_ids = DataFrame (ids, columns=['interaction_id'])
        return interaction_ids