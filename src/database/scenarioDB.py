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

    def get_interactionsPD(self,usr_id, dataset_id, time1, time2, imin, imax, umin,umax):   
        cursor = self.connection.get_cursor()
        code = """ CREATE OR REPLACE VIEW choose_timestamp AS (
                    SELECT I1.id FROM interaction I1
                    WHERE I1.timestamp > %s
                    AND I1.timestamp < %s
                     );

                    CREATE OR REPLACE VIEW choose_dataset_and_user AS (
                        SELECT I1.id FROM interaction I1, dataset D, users U
                        WHERE I1.dataset_id = D.id
                        AND D.usr_id = U.id
                        AND I1.dataset_id = %s
                        AND U.id = %s
                        );

                    SELECT I.id FROM interaction I
                    WHERE I.id IN ( SELECT * FROM  choose_timestamp )
                    AND I.id IN ( SELECT * FROM  choose_dataset_and_user )
                    AND I.client_id IN (	SELECT DISTINCT I1.client_id FROM interaction I1
                    WHERE I1.id IN ( SELECT * FROM  choose_timestamp )
                    AND I1.id IN ( SELECT * FROM  choose_dataset_and_user )
                    GROUP BY I1.client_id
                    HAVING COUNT(I1.client_id) > %s
                    AND COUNT(I1.client_id) < %s)
                    AND I.item_id IN (	SELECT DISTINCT I1.item_id FROM interaction I1
                    WHERE I1.id IN ( SELECT * FROM  choose_timestamp )
                    AND I1.id IN ( SELECT * FROM  choose_dataset_and_user )
                    GROUP BY I1.item_id
                    HAVING COUNT(I1.item_id) > %s
                    AND COUNT(I1.item_id) < %s);"""

        cursor.execute(code, (time1,time2,dataset_id,usr_id,umin,umax,imin,imax,))
        ids = cursor.fetchall()
        interaction_ids = DataFrame (ids, columns=['interaction_id'])
        return interaction_ids