from datetime import datetime, timedelta
from typing import Optional, Protocol

import bcrypt
import jwt
from database import BaseModel, db
from email_validator import EmailNotValidError, validate_email
from services.token_service import TokenService

# JWT configuration (in practice, should be in config file and loaded from env variables)
JWT_SECRET_KEY = 'your-secret-key'  # Change this to a secure key
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(days=1)

# Change from ABC to Protocol
class TokenAuthenticator(Protocol):
    def generate_token(self) -> str: ...
    def verify_token(self, token: str) -> bool: ...

class EmailVerifier(Protocol):
    def generate_verification_token(self) -> str: ...
    def verify_email(self, token: str) -> bool: ...

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

    def validate(self) -> bool:
        """Validate user data"""
        if not self.email or not self.validate_email(self.email):
            raise ValueError("Invalid email address")
        if not self.first_name or len(self.first_name) < 2:
            raise ValueError("First name must be at least 2 characters long")
        if not self.last_name or len(self.last_name) < 2:
            raise ValueError("Last name must be at least 2 characters long")
        return True

    def set_password(self, password: str) -> None:
        """Set user password with validation"""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one number")
        
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

    def generate_token(self) -> str:
        """Generate JWT token using TokenService"""
        return TokenService.generate_auth_token(self.id, self.email)

    @staticmethod
    def verify_token(token: str) -> Optional['User']:
        """Verify JWT token and return User instance"""
        try:
            payload = TokenService.verify_token(token)
            if not payload or 'user_id' not in payload:
                return None
            return User.query.get(payload['user_id'])
        except ValueError:
            return None

    def generate_verification_token(self) -> str:
        """Generate email verification token using TokenService"""
        self.email_verification_token = TokenService.generate_email_verification_token(self.id, self.email)
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
