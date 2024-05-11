# pylint: disable=no-member
"""Contains the API endpoints used for authentication and related
"""
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view
from .serializers import UserSerializer
from .jwt import generate_token, requires_jwt

@requires_jwt
@api_view(["GET"])
def users_view(_: HttpRequest, user_id: int) -> JsonResponse:
    """Returns the user with the given id

    If the user doesn't exist an error message will be returned instead

    Args:
        _ (HttpRequest): the request data
        user_id (int): the id of the user

    Returns:
        JsonResponse: the serialized user data
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."})

    serializer = UserSerializer(user)

    return JsonResponse(serializer.data, safe=False)

@requires_jwt
@api_view(["GET"])
def all_users_view(_: HttpRequest) -> JsonResponse:
    """Returns a serialized list of all users

    Args:
        _ (HttpRequest): the request data

    Returns:
        JsonResponse: the serialized users data
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(["POST"])
def login_view(request: HttpRequest) -> JsonResponse:
    """Logs a user in and returns a valid JWT the response's cookies

    Args:
        request (HttpRequest): the request data

    Returns:
        JsonResponse: a message with login details with a JWT embeded in the cookies
    """

    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid username."})

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid password."})

    response = JsonResponse(
        {
            "message": "Successfully logged in."
        }
    )
    response.set_cookie("jwt", generate_token(user))

    return response
