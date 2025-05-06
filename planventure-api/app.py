import os

from database import init_db
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
init_db(app)

# Initialize extensions
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API"})

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "database": "connected" if db.engine.connect() else "disconnected"
    })

if __name__ == '__main__':
    app.run(debug=True)
