from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'messicristianoneymarmbappehaaland'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:database123!@localhost/team3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    
    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import Users

    login_manager = LoginManager()
    login_manager.login_view = 'auth.registration'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(email):
        return Users.query.get(email)

    return app

app = create_app()