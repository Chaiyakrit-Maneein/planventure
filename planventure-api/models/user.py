from datetime import datetime, timedelta

import bcrypt
import jwt
from database import BaseModel, db
from email_validator import EmailNotValidError, validate_email

# JWT configuration (in practice, should be in config file and loaded from env variables)
JWT_SECRET_KEY = 'your-secret-key'  # Change this to a secure key
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(days=1)


class User(BaseModel):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(128))
    email_verification_sent_at = db.Column(db.DateTime)

    # Relationship
    trips = db.relationship('Trip', back_populates='user', lazy='dynamic')

    @staticmethod
    def generate_salt():
        return bcrypt.gensalt()
    
    @property
    def password(self):
        return self.password_hash

    @staticmethod
    def hash_password(password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt())


    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        password_hash = self.hash_password(password)
        self.password_hash = password_hash.decode('utf-8')
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except ValueError:
            return False
    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    def generate_token(self):
        """Generate JWT token for the user"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + JWT_EXPIRATION_DELTA
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user_id if valid"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def generate_verification_token(self):
        """Generate email verification token"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        self.email_verification_token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        self.email_verification_sent_at = datetime.utcnow()
        db.session.commit()
        return self.email_verification_token

    @staticmethod
    def verify_email(token):
        """Verify email verification token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user = User.query.get(payload['user_id'])
            if user and user.email_verification_token == token:
                user.email_verified = True
                user.is_active = True
                user.email_verification_token = None
                db.session.commit()
                return user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None
    
    def __repr__(self):
        return f'<User {self.email}>'
