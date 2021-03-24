class interactionDB:
    def __init__(self, connection):
        self.connection = connection

    def add_interaction(self,dataset_id,client_id,item_id,timestamp):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO interaction VALUES (%s,%s,%s,%s)', 
                (dataset_id, client_id, item_id, timestamp)
                )

            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save interaction')