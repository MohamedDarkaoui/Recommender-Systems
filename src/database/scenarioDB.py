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
                'INSERT INTO scenario (name,usr_id,date_time,dataset_id,sDate,eDate,max_items,min_items,max_clients,min_clients) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', 
                (scenarioOBJ.name,scenarioOBJ.usr_id,scenarioOBJ.date_time, scenarioOBJ.dataset_id, scenarioOBJ.time_min,scenarioOBJ.time_max,scenarioOBJ.item_max,
                scenarioOBJ.item_min,scenarioOBJ.client_max,scenarioOBJ.client_min))
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
                    cursor.execute(""" select client_id, item_id, tmstamp from subset_for_scenario(%s)
                    NATURAL JOIN subset_for_scenario_client (%s,%s,%s)""",
                    (dataset_id,dataset_id,umin,umax))
                elif umin == '0' and umax == 'infinity':
                    cursor.execute(""" select client_id, item_id, tmstamp from subset_for_scenario(%s)
                    NATURAL JOIN  subset_for_scenario_item (%s,%s,%s)""",
                    (dataset_id,dataset_id,imin,imax))
                else:
                    cursor.execute(""" select client_id, item_id, tmstamp from subset_for_scenario(%s)
                    NATURAL JOIN subset_for_scenario_client (%s,%s,%s)
                    NATURAL JOIN subset_for_scenario_item (%s,%s,%s)""",
                    (dataset_id,dataset_id,umin,umax,dataset_id,imin,imax))

            elif imin == '0' and imax == 'infinity':
                cursor.execute(
                """ select client_id, item_id, tmstamp from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
                natural join subset_for_scenario_client (%s::timestamp, %s::timestamp, %s,%s,%s)""",
                (time1,time2,dataset_id,time1,time2,dataset_id,umin,umax))
            elif umin == '0' and umax == 'infinity':
                cursor.execute(
                """ select client_id, item_id, tmstamp from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
                natural join subset_for_scenario_item (%s::timestamp, %s::timestamp, %s,%s,%s)""",
                (time1,time2,dataset_id,time1,time2,dataset_id,imin,imax))
            else:
                cursor.execute(
                """ select client_id, item_id, tmstamp from subset_for_scenario (%s::timestamp, %s::timestamp, %s) 
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
            cursor.copy_from(file=output, table='scenario_element(scenario_id, client_id, item_id, tmstamp)', null='') 
            self.connection.commit()

        except:
            self.connection.rollback()
            raise Exception('Unable to save scenario elements')
    
    
    def getScenariosFromUser(self, usr):
        """
        returns a list of scenarios that are created by usr
        """
        scenarios = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT * FROM scenario WHERE usr_id = %s', (id,))

        for row in cursor:
            scenario = Scenario(id=row[0],name=row[1],usr_id=row[2],date_time=row[3],dataset_id=row[4],time_min=row[5],time_max=row[6],item_max=row[7],item_min=row[8],client_max=row[9],client_min=row[10])
            scenarios.append(scenario)

        return scenarios

    def getScenarioID(self, name, user_id):
        """
        returns the id of the scenario given the name of the scenario and the dataset id
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.id FROM scenario I
                                WHERE I.name = %s
                                AND I.usr_id = %s""",(name,user_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the scenario id')

    def getScenarioItemCount(self, scenario_id):
        """
        counts the number of items
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT COUNT(distinct S.item_id) FROM scenario_element S
                                WHERE s.scenario_id = %s; """,(scenario_id,))
                                
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the count of items in scenario')    
    
    def getScenarioClientCount(self, scenario_id):
        """
        counts the number of clients
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT COUNT(distinct S.client_id) FROM scenario_element S
                                WHERE s.scenario_id = %s; """,(scenario_id,))
                                
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the count of items in scenario')    

    def getScenarioInteractionsCount(self,scenario_id):
        """
        given a scenario id, returns the number of interactions inside a scenario
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT COUNT (I.scenario_id) FROM scenario_element I
                                WHERE I.scenario_id = %s;""",(scenario_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the count of intercations')

    def getScenarioSample(self, scenario_id):
        """
        returns a pandas object with 50 scenario elements that belong to a certain dataset given the dataset_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.client_id, I.item_id, I.tmstamp FROM scenario_element I
                                WHERE I.scenario_id = %s
                                ORDER BY  I.tmstamp
                                LIMIT 50;""",(scenario_id,))
            result = cursor.fetchall()
            returnResult = DataFrame (result, columns=['client_id','item_id','tmstamp'])
            return returnResult
        except:
            raise Exception('Unable to select 50 scenario elements')

    def getPreProcessingSteps(self,scenario_id):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  select sdate::date,edate::date,min_items,max_items,min_clients,max_clients from scenario
                                WHERE id = %s""",(scenario_id,))
            result = cursor.fetchall()
            return result[0]
        except:
            raise Exception('Unable to select the preprocessing steps')
    
    def getScenarioName(self,id):
        """
        returns the name of the scenario with the given ID that belongs to the current user
        """

        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT D.name FROM scenario D
                                WHERE D.id =  %s """,(id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the name of the scenario')

    def getScenarioDataframe(self, scenarioID):
        """
        returns a pandas object with a scenario that has the given id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.client_id, I.item_id FROM scenario_element I
                                WHERE I.scenario_id = %s;""",(scenarioID,))
            result = cursor.fetchall()
            returnResult = DataFrame (result, columns=['client_id','item_id'])
            return returnResult
        except:
            raise Exception('Unable to get df for scenario')

    def getRandomClient(self,scenario_id):
        """
            get one client from the given scenario
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.client_id FROM scenario_element I
                                WHERE I.scenario_id = %s
                                ORDER BY RANDOM()
                                LIMIT 1;""",(scenario_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select random client')

    def getRandomItems(self,scenario_id,amount):
        """
            get a list of rndom items with size=amount
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT * FROM (SELECT  DISTINCT (I.item_id)  FROM scenario_element I
                                WHERE I.scenario_id = %s
                                LIMIT %s) SS
								ORDER BY RANDOM()""",(scenario_id,amount,))
                                
            result = [r[0] for r in cursor.fetchall()]
            return result
        except:
            raise Exception('Unable to select random client')

    def getClientHistory(self,scenario_id,client_id):
        """
            get a list of items that belong to th ehistoy of the given client
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.item_id FROM scenario_element I
                                WHERE I.scenario_id = %s
								AND I.client_id = %s;""",(scenario_id,client_id,))
            result = [r[0] for r in cursor.fetchall()]
            return result
        except:
            raise Exception('Unable to select items from scenario for the given client')

    def getMaxItem(self, scenario_id):
        """
            get the biggest item_id from a scenario
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT MAX (item_id) FROM scenario_element
                                WHERE scenario_id = %s;""",(scenario_id,))

            result = cursor.fetchall()
            return result[0][0]
            
        except:
            raise Exception('Unable to select the maximum item_id')

    

    def getAllClients(self,scenario_id):
        """
            get a list of all the clients from a scenario
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT DISTINCT (client_id) from scenario_element
                                    WHERE scenario_id = %s ORDER BY client_id;""",(scenario_id,))
                                
            result = [r[0] for r in cursor.fetchall()]
            return result
        except:
            raise Exception('Unable to select all the clients')

    def getAllItems(self,scenario_id):
        """
            get a list of all the items from a scenario
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT DISTINCT (item_id) from scenario_element
                                    WHERE scenario_id = %s ORDER BY item_id;""",(scenario_id,))
                                
            result = [r[0] for r in cursor.fetchall()]
            return result
        except:
            raise Exception('Unable to select all the items')

    def getAllClientsWithItem(self, scenario_id, item_id):
        """
        returns a list of clients that have an interaction with the given item inside the given scenario
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT DISTINCT (client_id) from scenario_element
                                WHERE scenario_id = %s
                                AND item_id = %s;""",(scenario_id,item_id))
                                
            result = [r[0] for r in cursor.fetchall()]
            return result
        except:
            raise Exception('Unable to select the clients for that item')

        
    def deleteScenario(self,scenario_id):
        """
        deletes a scenario with the given scenario id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM scenario
                                WHERE id = %s;""", (scenario_id,))
            self.connection.commit()
        except:
            self.connection.rollback()
            print("fout")


    