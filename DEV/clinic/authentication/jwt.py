from django.contrib.auth.models import User
from clinic.settings import SECRET_KEY, JWT_ALGORITHM
import jwt

def generate_token(user: User) -> str:
    """Generates a JWT based on the user's credentials

    Args:
        user (User): the user object to create the credentials from

    Returns:
        str: the JWT
    """
    payload = {
        "username": user.username,
        "password": user.password
    }

    return jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)

def validate_token(token: str) -> dict | None:
    """Validates a given token

    Args:
        token (str): the token to validate

    Returns:
        dict | None: returns the decoded payload if validated, None otherwise
    """
    try:
        decoded_payload = jwt.decode(token, SECRET_KEY, JWT_ALGORITHM)
    except jwt.InvalidSignatureError:
        return None

    return decoded_payload
