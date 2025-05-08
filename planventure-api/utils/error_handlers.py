from abc import ABC, abstractmethod


class AuthErrorCode:
    TOKEN_EXPIRED = "AUTH_001"
    TOKEN_INVALID = "AUTH_002"
    TOKEN_MISSING = "AUTH_003"

def create_error_response(error_code, message, status_code):
    return {
        "error": {
            "code": error_code,
            "message": message,
            "status": status_code
        }
    }

class ErrorStrategy(ABC):
    @abstractmethod
    def handle_error(self, code: str, message: str) -> dict:
        pass

class AuthErrorStrategy(ErrorStrategy):
    def handle_error(self, code: str, message: str) -> dict:
        return {
            "error": {
                "code": code,
                "message": message,
                "type": "auth"
            }
        }
