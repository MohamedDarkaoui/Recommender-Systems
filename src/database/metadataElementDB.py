import io
from pandas import DataFrame

class MetadataElementDB:
    def __init__(self, connection):
        self.connection = connection

    def add_metadataElements(self, pdOBJ):
        cursor = self.connection.get_cursor()
        
        output = io.StringIO()
        pdOBJ.to_csv(output,sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cursor.copy_from(file=output, table='metadata_element', null='') 
        self.connection.commit()

    def getMetadataSample(self, dataset_id):
        """
        returns a pandas object with 50 metadata elements (random order) that belong to a certain dataset given the dataset_id
        """
        cursor = self.connection.get_cursor()
        try:
            cursor.execute("""  SELECT I.item_id, I.description, I.data FROM metadata_element I
                                WHERE I.dataset_id = %s
                                ORDER BY RANDOM()
                                LIMIT 50;""",(dataset_id,))
            result = cursor.fetchall()
            returnResult = DataFrame (result, columns=['item_id','description','data'])
            return returnResult
        except:
            raise Exception('Unable to select 50 metadata elements')
