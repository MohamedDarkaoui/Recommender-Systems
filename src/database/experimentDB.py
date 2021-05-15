from database.entitiesDB import Experiment, Experiment_Client

class ExperimentDB:
    def __init__(self, connection):
        self.connection = connection
        self.counter = 0

    def add_experiment(self, ExpOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO Experiment (usr_id,name,model_id,date_time,retargeting,private) VALUES (%s,%s,%s,%s,%s,%s)', 
                (ExpOBJ.usr_id,ExpOBJ.name, ExpOBJ.model_id, ExpOBJ.date_time, ExpOBJ.retargeting,ExpOBJ.private,))

            cursor.execute('SELECT LASTVAL()')
            ExpOBJ.id = cursor.fetchone()[0]
            self.connection.commit()
            return ExpOBJ
        except:
            self.connection.rollback()
            raise Exception('Unable to add the experiment')

    def getExperimentsFromUser(self,usr):
        """
        returns a list of experiments that are created by usr
        """
        experiments = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT * FROM experiment WHERE usr_id = %s ORDER BY date_time', (id,))

        for row in cursor:
            experiment = Experiment(id=row[0],usr_id=row[1],name=row[2],model_id=row[3],date_time=row[4], retargeting=row[5], private=row[6])
            experiments.append(experiment)

        return experiments

    def getExperimentID(self, name, user_id):
        """
        returns the id of the experiment given the name of the experiment and the user id
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.id FROM experiment I
                                WHERE I.name = %s
                                AND I.usr_id = %s""",(name,user_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the experiment id')

    def getExperimentByName(self, name, user_id):
        """
        returns an experiment object
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.id, I.usr_id, I.name, I.model_id, I.date_time, I.retargeting, I.private FROM experiment I
                                WHERE I.name = %s
                                AND I.usr_id = %s""",(name,user_id,))
            result = cursor.fetchall()
            return Experiment(id=result[0][0], usr_id=result[0][1], name=result[0][2] ,model_id=result[0][3], date_time=result[0][4],
                retargeting=result[0][5], private=result[0][6])

        except:
            raise Exception('Unable to select the experiment')
        
    def getExperimentById(self, experiment_id):
        """
        returns an experiment object
        """
        
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.id, I.usr_id, I.name, I.model_id, I.date_time, I.retargeting, I.private FROM experiment I
                                WHERE I.id = %s""",(experiment_id,))
            result = cursor.fetchall()
            return Experiment(id=result[0][0], usr_id=result[0][1], name=result[0][2] ,model_id=result[0][3], date_time=result[0][4],
                retargeting=result[0][5], private=result[0][6])

        except:
            raise Exception('Unable to select the experiment')

    

    def addExperimentClient(self, client):
        """
            adds a new client to a experiment
        """
        cursor = self.connection.get_cursor()
        try:
            if client.expectations == None:
                cursor.execute("""INSERT INTO experiment_client (name, experiment_id,recommendations,history) 
                                        VALUES (%s,%s,%s,%s)""",(client.name, client.experiment_id, client.recommendations, client.history,))
            else:
                cursor.execute("""INSERT INTO experiment_client (name, experiment_id,recommendations,history,expectations) 
                                        VALUES (%s,%s,%s,%s,%s)""",(client.name, client.experiment_id, client.recommendations, client.history,client.expectations,))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to add the experiment client')

    def getExperimentClients(self, experiment_id):
        """
            get a list of experiment_client objects from a experiment with id = experiment_id
        """
        cursor = self.connection.get_cursor()
        cursor.execute('SELECT * FROM experiment_client WHERE experiment_id = %s ORDER BY id;', (experiment_id,))

        clients = []
        for row in cursor:
            history = row[4]
            history.sort()
            client = Experiment_Client(id=row[0], name=row[1], experiment_id=row[2], recommendations=row[3], history=history,expectations=row[5])
            clients.append(client)

        return clients

    def deleteExperiment(self,name, user_id):
        """
        deletes experiment with the given name an user 
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM experiment 
                                WHERE name = %s
                                AND usr_id = %s;""", (name,user_id,))
            self.connection.commit()
        except:
            self.connection.rollback()
    
    def deleteExperimentById(self, experiment_id):
        """
        deletes experiment with the given id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM experiment 
                                WHERE id = %s;""", (experiment_id,))
            self.connection.commit()
        except:
            self.connection.rollback()


    def deleteExperimentClient(self,name, experiment_id):
        """
        deletes experiment_client with the given name and experiment_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM experiment_client
                                WHERE name = %s
                                AND experiment_id = %s;""", (name,experiment_id,))
            self.connection.commit()
        except:
            self.connection.rollback()

    def getExperimentClient(self, name, experiment_id):
        """
            get a list of experiment_client objects from a experiment with id = experiment_id
        """
        cursor = self.connection.get_cursor()
        cursor.execute("""SELECT * FROM experiment_client WHERE name = %s
                            AND experiment_id = %s""", (name, experiment_id,))

        result = cursor.fetchone()
        client = Experiment_Client(id=result[0], name=result[1], experiment_id=result[2], recommendations=result[3], history=result[4], expectations=result[5])

        return client

    def updateExperimentClient(self, name, experiment_id, history, recommendations):
        """
        deletes experiment_client with the given name and experiment_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  UPDATE experiment_client
                                SET history = %s,
                                    recommendations = %s
                                WHERE experiment_id = %s
                                    AND name = %s;""", (history,recommendations,experiment_id,name,))

            self.connection.commit()
        except:
            self.connection.rollback()

    def experimentExists(self, name, usr_id):
        """
            returns true if there exists a experiment with name = name and usr_id = usr_id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM experiment
                                WHERE name = %s
                                AND usr_id = %s;""", (name,usr_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()
    
    def experimentExistsById(self, experiment_id):
        """
            returns true if there exists a experiment with id = experiment_id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT id FROM experiment
                                WHERE id = %s;""", (experiment_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()

    def experimentClientExists(self, name, experiment_id):
        """
            returns true if there exists a experiment client with name = name and experiment_id = experiment_id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT name FROM experiment_client
                                WHERE name = %s
                                AND experiment_id = %s;""", (name,experiment_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()

    def followsExperiment(self, usr, experiment_id):
        """
            returns true if the user follows the experiment with the given id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT * FROM experiment_follows
                                WHERE usr_id = %s
                                AND experiment_id = %s;""", (usr.id, experiment_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()

    
    def followsExperiment(self, usr, experiment_id):
        """
            returns true if the user follows the experiment with the given id else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT * FROM experiment_follows
                                WHERE usr_id = %s
                                AND experiment_id = %s;""", (usr.id, experiment_id,))

            result = cursor.fetchall()
            if len(result) == 0:
                return False
            return True
        except:
            self.connection.rollback()
    
    def followExperiment(self, usr, experiment_id, date_time):
        """
        adds a experiment follow
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO experiment_follows (usr_id, experiment_id, tmstamp) VALUES (%s,%s,%s)', 
                (usr.id, experiment_id, date_time),)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save the follow.')
    
    def unfollowExperiment(self, usr, experiment_id):
        """
        deletes a experiment follow
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  DELETE FROM experiment_follows
                                WHERE usr_id = %s
                                AND experiment_id = %s;""", (usr.id, experiment_id,))

            self.connection.commit()

        except:
            self.connection.rollback()
    
    def unfollowAllExperiment(self, experiment_id):
        """
        deletes al follows to the given experiment
        """
        cursor = self.connection.get_cursor()
        try:
            #REMOVE all FOLLOWS
            cursor.execute("""  DELETE FROM experiment_follows
                                WHERE experiment_id = %s;""", (experiment_id,))

            self.connection.commit()

        except:
            self.connection.rollback()

    def getFollowedExperiments(self, usr):
        """
            returns all experiments that the user follows
        """
        experiments = []
        cursor = self.connection.get_cursor()
        cursor.execute('SELECT experiment_id FROM experiment_follows WHERE usr_id = %s', (usr.id,))

        for row in cursor:
            experiment = self.getExperimentById(row[0])
            experiments.append(experiment)

        return experiments

    def isPrivate(self, experiment_id):
        """
            returns true if the experiment with the given id is private else false
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT private FROM experiment
                                WHERE id = %s;""", (experiment_id,))

            result = cursor.fetchall()
            return result[0][0]
        except:
            self.connection.rollback()
    
    def changePrivacy(self, experiment_id, private):
        """
            changes the privacy of the given experiment
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  UPDATE experiment 
                                SET private = %s 
                                WHERE id = %s;""", (private, experiment_id,))
            self.connection.commit()
            self.unfollowAllExperiment(experiment_id)
        except:
            
            self.connection.rollback()