"""
Created on: 12 Dec 2023
Script to populate the User database table to start writing data to it
"""
from portfolio_tracker import db, create_app
from portfolio_tracker.models.models import User

app = create_app()


def populate_db():
    # example users
    user_one = User(username='user1', email='user1@example.com')
    user_two = User(username='user2', email='user2@example.com')

    # add the users to the session
    db.session.add(user_one)
    db.session.add(user_two)

    # commit the session to the database
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        # populate the database
        populate_db()

        print("The database has been populated with the sample data for users")
