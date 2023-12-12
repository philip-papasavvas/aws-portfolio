"""
Created on: 12 Dec 2023
Script to populate the User database table to start writing data to it
"""
import os
import json
from sqlalchemy.exc import IntegrityError

from portfolio_tracker import db, create_app
from portfolio_tracker.models.models import User, Stock

app = create_app()


def populate_db():
    # # example users
    # user_one = User(username='user1', email='user1@example.com')
    # user_two = User(username='user2', email='user2@example.com')
    #
    # # add the users to the session
    # db.session.add(user_one)
    # db.session.add(user_two)

    from flask import current_app
    json_path = os.path.join(current_app.root_path, 'config', 'stocks.json')
    with open(json_path, 'r') as file:
        stock_list = json.load(file)

    for stock_info in stock_list:
        stock = Stock(ticker=stock_info['ticker'],
                      name=stock_info['name']
                      )
        db.session.add(stock)

    try:
        # commit the session to the database
        db.session.commit()
    except IntegrityError:
        # rollback the transaction if an error occurs
        db.session.rollback()


if __name__ == '__main__':
    with app.app_context():
        # populate the database
        populate_db()

        print("The database has been populated with the required data")
