import logging
import os
from pathlib import Path

from config.cors_config import CORSConfig
from config.env_validator import EnvValidator
from database import db
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from models.trip import Trip
from models.user import User
from routes.auth import auth_bp
from routes.trip import trip_bp
from sqlalchemy.exc import SQLAlchemyError
from utils.error_handlers import AuthErrorCode, create_error_response

# Load environment variables first
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set up paths
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_PATH = BASE_DIR / 'instance'
DB_FILE = Path.home() / "planventure.db"
DB_URI = f"sqlite:///{DB_FILE.as_posix()}"
file_path = os.path.abspath(os.getcwd())+"\instance\planventure.db"


# Ensure instance directory exists and is writable
INSTANCE_PATH.mkdir(parents=True, exist_ok=True)
assert INSTANCE_PATH.exists() and INSTANCE_PATH.is_dir(), "Instance dir missing"
assert os.access(INSTANCE_PATH, os.W_OK), "Instance dir not writable"

def create_app():
    print(f"INSTANCE_PATH: {INSTANCE_PATH}")
    print(f"DB_FILE: {DB_FILE}")
    print(f"DB_URI: {DB_URI}")
    print(f"INSTANCE_PATH exists: {INSTANCE_PATH.exists()}")
    print(f"INSTANCE_PATH is dir: {INSTANCE_PATH.is_dir()}")
    print(f"DB_FILE exists: {DB_FILE.exists()}")

    env_config = EnvValidator.validate_required_vars()
    app = Flask(__name__, instance_path=str(INSTANCE_PATH))
    #app.config['SQLALCHEMY_DATABASE_URI'] = env_config.get('DATABASE_URL', DB_URI)
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/planventure.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = env_config.get('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = env_config.get('JWT_SECRET_KEY')
    import os

    app.config['JWT_EMAIL_TOKEN_EXPIRES'] = int(os.getenv('JWT_EMAIL_TOKEN_EXPIRES', 24))

    db.init_app(app)
    Migrate(app, db)
    CORSConfig.initialize_cors(app)

    # Do NOT touch or create DB_FILE manually here!

    with app.app_context():
        db.create_all()

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(error):
        return jsonify(create_error_response(
            AuthErrorCode.TOKEN_EXPIRED,
            "Your session has expired. Please log in again.",
            401
        )), 401

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token(error):
        return jsonify(create_error_response(
            AuthErrorCode.TOKEN_INVALID,
            "Invalid authentication token. Please log in again.",
            401
        )), 401

    @app.errorhandler(401)
    def handle_missing_token(error):
        return jsonify(create_error_response(
            AuthErrorCode.TOKEN_MISSING,
            "Authentication token is missing. Please log in.",
            401
        )), 401

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(trip_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to PlanVenture API"})

    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
