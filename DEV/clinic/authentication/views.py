# pylint: disable=no-member
"""Contains the API endpoints used for authentication and related
"""
import json
import uuid

from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.db.utils import IntegrityError

from rest_framework.decorators import api_view

from aws_middleware.s3 import s3_upload
from aws_middleware.stepfunctions import execute_workflow
from clinic.settings import (
    MAX_FILE_SIZE,
    REKOGNITION_COLLECTION_ID,
    S3_IMAGE_BUCKET_NAME,
    STATE_MACHINE_ARN,
)

from .serializers import UserSerializer
from .jwt import (
    generate_token,
    perm_required,
    requires_jwt,
    validate_token,
    verify_format,
)


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
        return JsonResponse({"error": "Username inválido."})

    if not user.check_password(password):
        return JsonResponse({"error": "Password inválida."})

    response = JsonResponse({"message": "Logado com sucesso."})
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
        return JsonResponse({"error": "Nenhuma imagem selecionada."})

    if image.size > MAX_FILE_SIZE:
        return JsonResponse({"error": "Tamanho máximo excedido."})

    if (
        status := s3_upload(
            image_key=username, bucket_name=S3_IMAGE_BUCKET_NAME, image_file=image
        )
    ) != True:
        return JsonResponse({"error": f"Erro ao dar upload da imagem: {status}"})

    response = execute_workflow(
        {
            "type": "getFaceprint",
            "arguments": {
                "username": username,
                "bucketName": S3_IMAGE_BUCKET_NAME,
                "collectionId": REKOGNITION_COLLECTION_ID,
            },
        },
        STATE_MACHINE_ARN,
    )

    if json.loads(response.content)["statusCode"] == 200:
        return JsonResponse({"message": "Imagem enviada com sucesso."})

    return JsonResponse(
        {
            "error": f"Erro ao dar upload da imagem: {json.loads(response.content)['error']}"
        }
    )


@perm_required("admin")
@api_view(["POST"])
def facial_recognition_view(request: HttpRequest) -> JsonResponse:
    """Launches a facial recognition workflow with the given image

    Args:
        request (HttpRequest): the request data

    Returns:
        JsonResponse: the response data with the possible output of the workflow
    """
    try:
        image = request.FILES["file"]
    except KeyError:
        return JsonResponse({"error": "Nenhuma imagem selecionada."})

    if image.size > MAX_FILE_SIZE:
        return JsonResponse({"error": "Tamanho máximo excedido."})

    image_uuid = str(uuid.uuid4())

    if (
        status := s3_upload(
            image_key=image_uuid, bucket_name=S3_IMAGE_BUCKET_NAME, image_file=image
        )
    ) != True:
        return JsonResponse({"error": f"Erro ao dar upload da imagem: {status}"})

    response = execute_workflow(
        {
            "type": "facialRecognition",
            "arguments": {
                "imageUUID": image_uuid,
                "bucketName": S3_IMAGE_BUCKET_NAME,
                "collectionId": REKOGNITION_COLLECTION_ID,
            },
        },
        STATE_MACHINE_ARN,
    )

    if json.loads(response.content)["statusCode"] == 200:
        return JsonResponse(
            {
                "message": json.loads(json.loads(response.content)["message"])["Item"][
                    "username"
                ]["S"]
            }
        )

    return JsonResponse(
        {
            "error": f"Erro ao dar upload da imagem: {json.loads(response.content)['error']}"
        }
    )
