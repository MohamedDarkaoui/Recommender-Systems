import io

class ClientDB:
    def __init__(self, connection):
        self.connection = connection

    def add_client(self,pdOBJ):
        cursor = self.connection.get_cursor()
        try:
            output = io.StringIO()
            pdOBJ.to_csv(output,sep='\t', header=False, index=False)
            output.seek(0)
            contents = output.getvalue()
            cursor.copy_from(file=output, table='client', null='') 
            self.connection.commit()
            
        except:
            self.connection.rollback()
            raise Exception('Unable to save client: ' + id)
    
    def getCountClients(self, dataset_id):
        """
        given a dataset id, returns the number of clients
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT COUNT (I.dataset_id) FROM client I
                                WHERE I.dataset_id = %s
                                GROUP BY I.dataset_id;""",(dataset_id,))
            result = cursor.fetchall()
            return result[0][0]
        except:
            raise Exception('Unable to select the count of client')