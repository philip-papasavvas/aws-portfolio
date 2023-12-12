"""
Created on: 7 Dec 2023
App file to initialise the Flask application and link it to a SQL Alchemy db
"""

from flask import Flask
from portfolio_tracker.models.models import db


def create_app():
    # Initiate a Flask app within the function
    app = Flask(__name__)

    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Create tables
    with app.app_context():
        # this creates the database file using SQLAlchemy
        db.create_all()

    return app
