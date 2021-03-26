from entitiesDB.dataset import Metadata

class MetadataDB:
    def __init__(self, connection):
        self.connection = connection

    def add_metadata(self, metadataOBJ):
        cursor = self.connection.get_cursor()
        try:
            cursor.execute('INSERT INTO metadata (dataset_id) VALUES (%s)', (metadataOBJ.dataset_id,))
            self.connection.commit()
            cursor.execute('SELECT LASTVAL()')
            metadataOBJ.id = cursor.fetchone()[0]
            return metadataOBJ
        except:
            self.connection.rollback()
            raise Exception('Unable to save metadata: ')