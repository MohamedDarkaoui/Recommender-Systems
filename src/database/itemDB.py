
class ItemDB:
    def __init__(self, connection):
        self.connection = connection

    def add_item(self,id, dataset_id):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute('INSERT INTO item VALUES (%s,%s)', (id,dataset_id))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save item: ' + id)