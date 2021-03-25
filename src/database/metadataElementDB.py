class MetadataElementDB:
    def __init__(self, connection):
        self.connection = connection

    def add_metadataElement(self, item_id, dataset_id, metadata_id, description, data):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute('INSERT INTO metadata_element VALUES (%s,%s,%s,%s,%s)', (item_id, dataset_id, metadata_id, description, data))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise Exception('Unable to save metadata: ')