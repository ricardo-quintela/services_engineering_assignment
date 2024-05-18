# pylint: disable=no-member
"""Contains the API endpoints used for authentication and related
"""

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view

from clinic.settings import MAX_FILE_SIZE, S3_IMAGE_BUCKET_NAME
from aws_middleware.s3 import s3_upload
from .serializers import UserSerializer
from .jwt import generate_token, perm_required, requires_jwt, validate_token, verify_format



@perm_required("admin")
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


@perm_required("admin")
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
def register_view(request: HttpRequest) -> JsonResponse:
    """Registers a user on the website

    Args:
        request (HttpRequest): the request data

    Returns:
        JsonResponse: a message with detailed information about the status details
    """

    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError:
        return JsonResponse({"error": "User already exists."})
    user.save()

    return JsonResponse({"message": "Successfully registered."})

@api_view(["POST"])
def login_view(request: HttpRequest) -> JsonResponse:
    """Logs a user in and returns a valid JWT the response's headers

    Args:
        request (HttpRequest): the request data

    Returns:
        JsonResponse: a message with login details with a JWT embeded in the headers
    """

    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid username."})

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid password."})

    response = JsonResponse({"message": "Successfully logged in."})
    response.headers["jwt"] = generate_token(user)

    return response


@requires_jwt
@api_view(["POST"])
def upload_image_view(request: HttpRequest) -> JsonResponse:

    jwt_payload = verify_format(validate_token(request.headers["jwt"]))
    username = jwt_payload.username

    try:
        image = request.FILES["file"]
    except KeyError:
        return JsonResponse({"error": "No image was uploaded."})

    if image.size > MAX_FILE_SIZE:
        return JsonResponse({"error": "Uploaded file excedes max size limit."})

    if not s3_upload(image_key=username, bucket_name=S3_IMAGE_BUCKET_NAME, image_file=image):
        return JsonResponse({"message": "An error occured while uploading the image."})

    return JsonResponse({"message": "Image successfully uploaded."})
