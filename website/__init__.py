'''
Author: Dietrich Sinkevitch
Program: Tech Product Search Tool
Date: 08/08/2023
Github Link: https://github.com/dytryk/techproductsearchtool
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    '''This function initializes the application, and is called by main.'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wsfgsjrthvtesargjyzmertszDfvsrsd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # import and register the blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Admin, Product
    
    with app.app_context():
        db.create_all()

    # define the login view
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # load either an admin or a regular user
    @login_manager.user_loader
    def load_user(id):
        if Admin.query.get(int(id)) is not None:
            return Admin.query.get(int(id))
        else: 
            return User.query.get(int(id))
    
    return app