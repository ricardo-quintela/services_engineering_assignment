# pylint: disable=no-member
"""Contains the API endpoints used for authentication and related
"""
from django.contrib.auth.models import User
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@api_view(["GET"])
def users_view(_: HttpRequest, user_id: int) -> Response:
    """Returns the user with the given id

    If the user doesn't exist an error message will be returned instead

    Args:
        _ (HttpRequest): the request data
        user_id (int): the id of the user

    Returns:
        Response: the serialized user data
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User does not exist."})

    serializer = UserSerializer(user)

    return Response(serializer.data)

@api_view(["GET"])
def all_users_view(_: HttpRequest) -> Response:
    """Returns a serialized list of all users

    Args:
        _ (HttpRequest): the request data

    Returns:
        Response: the serialized users data
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)
