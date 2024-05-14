from typing import Callable, Any
from django.http import HttpRequest, JsonResponse, HttpResponse

from authentication.jwt import validate_token, verify_expiry, verify_format


def perm_required(perm: str | None) -> Callable[[HttpRequest, Any], JsonResponse | HttpResponse]:
    def decorator(endpoint: Callable[[HttpRequest, Any], HttpResponse]) -> Callable[[HttpRequest, Any], JsonResponse | HttpResponse]:

        error_message = {"error": "User is not logged in."}
        permission_error_message = {"error": "Forbidden."}

        def wrapper(*args, **kwargs):
            try:
                token = args[0].COOKIES["jwt"]
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

            if perm != jwt_payload.role:
                return JsonResponse(permission_error_message)

            return endpoint(*args, **kwargs)

        return wrapper

    return decorator
        