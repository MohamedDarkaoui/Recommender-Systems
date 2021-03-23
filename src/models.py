from appCreator import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id =  db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    
    

    def get_id(self):
        return (self.id)
