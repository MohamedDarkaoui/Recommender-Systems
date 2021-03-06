from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    email = db.Column(db.String(150), primary_key=True)
    password = db.Column(db.String(150))

    def get_id(self):
        return (self.email)