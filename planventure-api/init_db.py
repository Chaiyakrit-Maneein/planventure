import os

from database import db, init_db
from flask import Flask
from models.trip import Trip
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
db.init_db(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

def reset_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all existing tables")
        
        # Create all tables
        db.create_all()
        print("Created new tables successfully!")

if __name__ == '__main__':
    reset_db()
