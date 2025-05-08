from flask_cors import CORS


class CORSConfig:
    @staticmethod
    def initialize_cors(app):
        CORS(app, resources={
            r"/*": {
                "origins": ["http://localhost:3000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "expose_headers": ["Authorization"],
                "supports_credentials": True
            }
        })
