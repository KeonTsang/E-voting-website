from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # Replace 'your_database_uri' with the actual URI of your database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    
    # Initialize the database extension with the app
    db.init_app(app)

    # Import views and register the blueprint
    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Import models and create database tables
    from .models import Vote, AuditTrail, Candidate, Voter

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')


