import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

DB_FILE = Path.home() / "planventure.db"
DB_URI = f"sqlite:///{DB_FILE.as_posix()}"

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

def init_db(app):
    """Initialize the database with the app context"""
    db.init_app(app)
    BaseModel.metadata.bind = db.engine
    
    with app.app_context():
        db.create_all()

try:
    testfile = INSTANCE_PATH / "testwrite.txt"
    with open(testfile, "w") as f:
        f.write("test")
    os.remove(testfile)
    print("Write test: SUCCESS")
except Exception as e:
    print(f"Write test: FAIL - {e}")
