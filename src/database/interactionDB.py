import io

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


    