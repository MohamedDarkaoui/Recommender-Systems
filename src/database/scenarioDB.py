import io
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
                (scenarioOBJ.name,scenarioOBJ.usr_id,scenarioOBJ.date_time, scenarioOBJ.dataset_id))
            cursor.execute('SELECT LASTVAL()')
            scenarioOBJ.id = cursor.fetchone()[0]
            self.connection.commit()
            return scenarioOBJ

        except:
            self.connection.rollback()
            raise Exception('Unable to save scenario: ' + scenarioOBJ.name)

    def get_interactionsPD(self, dataset_id, time1, time2, imin, imax, umin,umax):   

        cursor = self.connection.get_cursor()
        try:
            if time1 == '-infinity' and time2 == 'infinity':
                if imin == '0' and imax == 'infinity':
                    cursor.execute(""" select * from subset_for_scenario(%s)
                    NATURAL JOIN subset_for_scenario_client (%s,%s,%s)""",
                    (dataset_id,dataset_id,umin,umax))
                elif umin == '0' and umax == 'infinity':
                    cursor.execute(""" select * from subset_for_scenario(%s)
                    NATURAL JOIN  subset_for_scenario_item (%s,%s,%s)""",
                    (dataset_id,dataset_id,imin,imax))
                else:
                    cursor.execute(""" select * from subset_for_scenario(%s)
                    NATURAL JOIN subset_for_scenario_client (%s,%s,%s)
                    NATURAL JOIN subset_for_scenario_item (%s,%s,%s)""",
                    (dataset_id,dataset_id,umin,umax,dataset_id,imin,imax))

            elif imin == '0' and imax == 'infinity':
                cursor.execute(
                """ select * from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
                natural join subset_for_scenario_client (%s::timestamp, %s::timestamp, %s,%s,%s)""",
                (time1,time2,dataset_id,time1,time2,dataset_id,umin,umax))
            elif umin == '0' and umax == 'infinity':
                cursor.execute(
                """ select * from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
                natural join subset_for_scenario_item (%s::timestamp, %s::timestamp, %s,%s,%s)""",
                (time1,time2,dataset_id,time1,time2,dataset_id,imin,imax))
            else:
                cursor.execute(
                """ select * from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
                natural join subset_for_scenario_client (%s::timestamp, %s::timestamp, %s,%s,%s)
                natural join subset_for_scenario_item (%s::timestamp, %s::timestamp, %s,%s,%s)""",
                (time1,time2,dataset_id,time1,time2,dataset_id,umin,umax,time1,time2,dataset_id,imin,imax))

            result = cursor.fetchall()
            returnResult = DataFrame (result, columns=['client_id','item_id','tmstamp'])
            return returnResult
        except:
            self.connection.rollback()
            raise Exception('unable to select from interaction')

    def add_scenario_elements(self,pdOBJ):
        cursor = self.connection.get_cursor()
        try:
            output = io.StringIO()
            pdOBJ.to_csv(output,sep='\t', header=False, index=False)
            output.seek(0)
            contents = output.getvalue()
            cursor.copy_from(file=output, table='scenario_element', null='') 
            self.connection.commit()

        except:
            self.connection.rollback()
            raise Exception('Unable to save scenario elements')
    
    
    def getScenariosFromUser(self, usr):
        """
        returns a list of datasets that are created by usr
        """
        scenarios = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT * FROM scenario WHERE usr_id = %s', (id,))

        for row in cursor:
            scenario = Scenario(id=row[0],name=row[1],usr_id=row[2],date_time=row[3],dataset_id=row[4])
            scenarios.append(scenario)

        return scenarios