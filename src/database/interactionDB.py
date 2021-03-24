class interactionDB:
    def __init__(self, connection):
        self.connection = connection

    def add_interaction(self,interactionOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute(
                'INSERT INTO interaction VALUES (%s,%s,%s,%s)', 
                (interactionOBJ.id, interactionOBJ.dataset_id,interactionOBJ.client_id,interactionOBJ.item_id, interactionOBJ.timestamp)
                )

            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save interaction')