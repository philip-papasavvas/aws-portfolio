"""
Created on: 2 Jan 2024
Script to populate User database table with user information
"""
from sqlalchemy.exc import IntegrityError

from portfolio_tracker import create_app
from portfolio_tracker.models.models import User, db

app = create_app()


def populate_user_db_table():
    """
    Created abd adds example user instances to the user database table.
    This function creates two example users with predefined usernames and
    email addresses, adds them to the database session and commits the session.
    If an Integrity error is encountered during the commit (e.g. duplicate entry)
    then the transaction is rolled back to ensure database integrity.
    """
    # define example users

    users = [
     User(username='user1', email='user1@example.com'),
     User(username='user2', email='user2@example.com')
    ]
    # add the users to the session
    for user in users:
        db.session.add(user)

    try:
        db.session.commit()  # commit the session to the database
    except IntegrityError:
        db.session.rollback()  # rollback the transaction if an error occurs


if __name__ == '__main__':
    with app.app_context():
        populate_user_db_table()
