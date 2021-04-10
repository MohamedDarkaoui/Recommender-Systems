import io
from pandas import DataFrame

class interactionDB:
    def __init__(self, connection):
        self.connection = connection
    def add_interaction(self, pdOBJ):
        cursor = self.connection.get_cursor()
        try:
            output = io.StringIO()
            pdOBJ.to_csv(output,sep='\t', header=False, index=False)
            output.seek(0)
            contents = output.getvalue()
            cursor.copy_from(file=output, table='interaction(dataset_id,client_id,item_id,tmstamp)', null='') 
            self.connection.commit()

        except:
            self.connection.rollback()
            raise Exception('Unable to save interaction')

    def getInteractionSample(self, dataset_id):
        """
        returns a pandas object with 50 interactions that belong to a certain dataset given the dataset_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.client_id, I.item_id, I.tmstamp FROM interaction I
                                WHERE I.dataset_id = %s
                                ORDER BY  I.tmstamp
                                LIMIT 50;""",(dataset_id,))
            result = cursor.fetchall()
            returnResult = DataFrame (result, columns=['client_id','item_id','tmstamp'])
            return returnResult
        except:
            raise Exception('Unable to select 50 interactions')

    def getCountInteractions(self, dataset_id):
        """
        given a dataset id, returns the number of interactions
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT COUNT (I.dataset_id) FROM interaction I
                                WHERE I.dataset_id = %s
                                GROUP BY I.dataset_id;""",(dataset_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the count of intercations')
