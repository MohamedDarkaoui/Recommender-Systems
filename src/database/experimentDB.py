from database.entitiesDB import Experiment

class ExperimentDB:
    def __init__(self, connection):
        self.connection = connection

    def add_experiment(self, ExpOBJ):
        cursor = self.connection.get_cursor()

        cursor.execute(
            'INSERT INTO Experiment (usr_id,name,model_id,date_time) VALUES (%s,%s,%s,%s)', 
            (ExpOBJ.usr_id,ExpOBJ.name, ExpOBJ.model_id, ExpOBJ.date_time,))

        cursor.execute('SELECT LASTVAL()')
        ExpOBJ.id = cursor.fetchone()[0]
        self.connection.commit()
        return ExpOBJ

    def getExperimentsFromUser(self,usr):
        """
        returns a list of experiments that are created by usr
        """
        experiments = []
        cursor = self.connection.get_cursor()
        id = str(usr.id)
        cursor.execute('SELECT * FROM experiment WHERE usr_id = %s ORDER BY date_time', (id,))

        for row in cursor:
            experiment = Experiment(id=row[0],usr_id=row[1],name=row[2],model_id=row[3],date_time=row[4])
            experiments.append(experiment)

        return experiments