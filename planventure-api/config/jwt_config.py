import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

class JWTConfig:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_DAYS = 1
    
    @classmethod
    def get_config(cls):
        return {
            'SECRET_KEY': cls.SECRET_KEY,
            'ALGORITHM': cls.ALGORITHM,
            'ACCESS_TOKEN_EXPIRE_DELTA': timedelta(days=cls.ACCESS_TOKEN_EXPIRE_DAYS)
        }
