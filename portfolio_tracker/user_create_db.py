"""
Created on: 7 Dec 2023

"""
from models import User, db
from app import app

# Create a new user
new_user = User(username='testuser', email='testuser@example.com')

# Add the new user to the session
with app.app_context():
    db.session.add(new_user)

    # Commit the session to write changes to the database
    db.session.commit()