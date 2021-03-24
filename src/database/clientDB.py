class ClientDB:
    def __init__(self, connection):
        self.connection = connection

    def add_client(self,id,dataset_id):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute('INSERT INTO client VALUES (%s,%s)', (id,dataset_id))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save client: ' + id)