import os
from typing import Dict


class EnvValidator:
    @staticmethod
    def validate_required_vars() -> Dict[str, str]:
        required_vars = {
            'JWT_SECRET_KEY': 'dev-jwt-secret-key',
            'SECRET_KEY': 'dev-secret-key',
            'DATABASE_URL': 'sqlite:///instance/planventure.db'
        }
        
        config = {}
        for var, default in required_vars.items():
            value = os.getenv(var)
            if not value:
                if var.endswith('SECRET_KEY'):
                    print(f"Warning: Using default {var} in development")
                value = default
            config[var] = value
        return config