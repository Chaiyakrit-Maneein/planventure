from database import db, init_db
from flask import Flask
from models.user import User

app = Flask(__name__)
init_db(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
