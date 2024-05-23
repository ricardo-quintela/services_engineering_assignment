from typing import Callable, Any
from datetime import datetime

import jwt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, JsonResponse
from pydantic import BaseModel, ValidationError

from clinic.settings import SECRET_KEY, JWT_ALGORITHM, JWT_TOKEN_EXPIRY


class JwtPayload(BaseModel):
    """A valid structure of a JWT"""

    username: str
    timestamp: float
    role: str | None


def generate_token(user: User) -> str:
    """Generates a JWT based on the user's credentials

    Args:
        user (User): the user object to create the credentials from

    Returns:
        str: the JWT
    """

    role = user.groups.first()

    jwt_payload = JwtPayload(
        username=user.username,
        timestamp=datetime.now().timestamp(),
        role=role.name if role is not None else None,
    )

    return jwt.encode(jwt_payload.model_dump(), SECRET_KEY, JWT_ALGORITHM)


def validate_token(token: str) -> dict[str, str | float] | None:
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


def verify_expiry(jwt_payload: JwtPayload) -> bool:
    """Verifies the expiry of the given token

    Args:
        payload (JwtPayload): the payload of a JWT

    Returns:
        bool: True if it hasn't expired, False otherwise
    """
    timestamp = jwt_payload.timestamp
    date_time_instance = datetime.fromtimestamp(timestamp)

    return (datetime.now() - date_time_instance).total_seconds() < JWT_TOKEN_EXPIRY


def verify_format(jwt_payload: dict[str, str | float]) -> JwtPayload | None:
    """Verifies the format of a JWT payload

    Args:
        payload (dict[str, str  |  float]): the payload of the JWT

    Returns:
        JwtPayload | None: A JwtPayload instance with the payload contents if it can
        be validated, None otherwise
    """
    try:
        jwt_payload = JwtPayload(**jwt_payload)

    except ValidationError:
        return None

    return jwt_payload


def requires_jwt(
    endpoint: Callable[[HttpRequest, Any], HttpResponse]
) -> Callable[[HttpRequest, Any], JsonResponse | HttpResponse]:
    """Makes an endpoint require a valid JWT sent in the cookies

    Args:
        endpoint (Callable[[HttpRequest, Any], HttpResponse]): the endpoint

    Returns:
        Callable[[HttpRequest, Any], JsonResponse | HttpResponse]: the same endpoint
        with JWT authentication
    """
    error_message = {"error": "User is not logged in."}

    def wrapper(*args, **kwargs):
        try:
            token = args[0].headers["jwt"]
        except KeyError:
            return JsonResponse(error_message)

        payload = validate_token(token)
        if payload is None:
            return JsonResponse(error_message)

        jwt_payload = verify_format(payload)
        if jwt_payload is None:
            return JsonResponse(error_message)

        if not verify_expiry(jwt_payload):
            return JsonResponse(error_message)

        return endpoint(*args, **kwargs)

    return wrapper


def perm_required(
    *perms: str | None,
) -> Callable[[HttpRequest, Any], JsonResponse | HttpResponse]:
    """Ensures only a User with the given permissions can access the endpoint

    Returns:
        Callable[[HttpRequest, Any], JsonResponse | HttpResponse]: _description_
    """

    def decorator(
        endpoint: Callable[[HttpRequest, Any], HttpResponse]
    ) -> Callable[[HttpRequest, Any], JsonResponse | HttpResponse]:

        error_message = {"error": "User is not logged in."}
        permission_error_message = {"error": "Forbidden."}

        def wrapper(*args, **kwargs):
            try:
                token = args[0].headers["jwt"]
            except KeyError:
                return JsonResponse(error_message)

            payload = validate_token(token)
            if payload is None:
                return JsonResponse(error_message)

            jwt_payload = verify_format(payload)
            if jwt_payload is None:
                return JsonResponse(error_message)

            if not verify_expiry(jwt_payload):
                return JsonResponse(error_message)

            if jwt_payload.role not in perms:
                return JsonResponse(permission_error_message)

            return endpoint(*args, **kwargs)

        return wrapper

    return decorator
