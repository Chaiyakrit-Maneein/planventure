import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple

import jwt
from dotenv import load_dotenv
from flask import current_app

load_dotenv()
logger = logging.getLogger(__name__)

class TokenService:
    _secret_key = None
    
    @classmethod
    def _get_secret_key(cls) -> str:
        if not cls._secret_key:
            cls._secret_key = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
            logger.debug(f"Initialized JWT secret key: {cls._secret_key[:5]}...")
        return cls._secret_key

    @classmethod
    def generate_auth_token(cls, user_id: int, email: str) -> str:
        """Generate JWT authentication token"""
        now = datetime.utcnow()
        expiration = now + timedelta(days=1)
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': expiration,
            'iat': now,
            'type': 'access'
        }
        secret_key = cls._get_secret_key()
        logger.debug(f"Generating token for user_id: {user_id} using key: {secret_key[:5]}...")
        return jwt.encode(payload, secret_key, algorithm='HS256')

    @classmethod
    def verify_token(cls, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            secret_key = cls._get_secret_key()
            logger.debug(f"Verifying token: {token[:10]}... using key: {secret_key[:5]}...")
            
            unverified = jwt.decode(token, options={"verify_signature": False})
            logger.debug(f"Token payload structure: {unverified}")
            
            return jwt.decode(token, secret_key, algorithms=['HS256'])
            
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Token expired: {str(e)}")
            raise
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise

    @classmethod
    def generate_email_verification_token(cls, user_id: int, email: str) -> str:
        """Generate email verification token"""
        now = datetime.utcnow()
        expiration = now + timedelta(hours=current_app.config['JWT_EMAIL_TOKEN_EXPIRES'])
        payload = {
            'user_id': user_id,
            'email': email,
            'exp': expiration,
            'iat': now,
            'nbf': now,
            'type': 'email_verification'
        }
        secret_key = cls._get_secret_key()
        return jwt.encode(payload, secret_key, algorithm='HS256')
