# pylint: disable=no-member
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import FieldDoesNotExist

from rest_framework.decorators import api_view
from authentication.jwt import perm_required, validate_token, requires_jwt
from django.contrib.auth.models import User
from aws_middleware.stepfunctions import execute_workflow

from .models import Consultas
from .serializers import AppointmentSerializer

from clinic.settings import STATE_MACHINE_ARN


@perm_required("admin")
@api_view(["GET"])
def all_appointments_view(_: HttpRequest) -> JsonResponse:

    appointments = Consultas.objects.all()

    serializer = AppointmentSerializer(appointments, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
def all_appointments_view_id(request: HttpRequest) -> JsonResponse:
    
    token = request.headers["jwt"]
    username = validate_token(token)["username"]
    user_id = User.objects.filter(username=username).values()[0]["id"]
    
    appointments = Consultas.objects.filter(user=user_id)

    serializer = AppointmentSerializer(appointments, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["PUT"])
def update_appointments_view(request: HttpRequest, _id: int) -> JsonResponse:

    appointment = Consultas.objects.filter(id=_id)
    if appointment is None:
        return JsonResponse({"error": "Consulta não encontrada."})

    json_payload: dict = request.data

    try:
        appointment.update(**{k: json_payload.get(k) for k in json_payload})
    except FieldDoesNotExist as e:
        return JsonResponse({"error": "Erro ao atualizar o estado da consulta."})

    serializer = AppointmentSerializer(appointment.first())

    return JsonResponse(serializer.data, safe=False)


@requires_jwt
@api_view(["POST"])
def schedule_appointment(request: HttpRequest) -> JsonResponse:
    """Build the request to schedulle the medical appointment

    Args:
        request (HttpRequest): the requested data

    Returns:
        JsonResponse: a message with success or errors
    """

    try:
        data = request.data["data"]
        hora = int(request.data["hora"])
        especialidade = int(request.data["especialidade"])
        medico = request.data["medico"]
    except KeyError:
        return JsonResponse({"error": "Parâmetros inválidos."})
    except ValueError:
        return JsonResponse({"error": "Parâmetros inválidos."})

    token = request.headers["jwt"]
    username = validate_token(token)["username"]

    return execute_workflow(
        {
            "cliente": username,
            "data": data,
            "hora": hora,
            "especialidade": especialidade, 
            "medico": medico,
            "estado": "open",
        },
        STATE_MACHINE_ARN
    )
