# pylint: disable=no-member
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import FieldDoesNotExist

from rest_framework.decorators import api_view
from authentication.jwt import perm_required, validate_token, requires_jwt

from .models import Appointment
from .serializers import AppointmentSerializer

import json
import boto3

@perm_required("admin")
@api_view(["GET"])
def all_appointments_view(_: HttpRequest) -> JsonResponse:
    appointments = Appointment.objects.all()

    serializer = AppointmentSerializer(appointments, many=True)

    return JsonResponse(serializer.data, safe=False)


@perm_required("admin")
@api_view(["PUT"])
def update_appointments_view(request: HttpRequest, _id: int) -> JsonResponse:

    appointment = Appointment.objects.filter(id=_id)
    if appointment is None:
        return JsonResponse({"error": "Appointment does not exist."})

    json_payload: dict = request.data

    try:
        appointment.update(**{k:json_payload.get(k) for k in json_payload})
    except FieldDoesNotExist as e:
        return JsonResponse({"error": f"{e}"})

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

    data = request.data.get("data")
    hora = int(request.data.get("horario"))
    especialidade = int(request.data.get("especialidade"))
    medico = request.data.get("medico")
    
    token = request.headers["jwt"]
    username = validate_token(token)["username"]
    
    try:
        sf = boto3.client('stepfunctions', region_name = 'us-east-1')
        input_sf = json.dumps({"cliente": username, "data": data, "hora": hora, "especialidade": especialidade, "medico": medico, "estado": "Não Pago"})
        response = sf.start_execution(stateMachineArn = 'arn:aws:states:us-east-1:497624740126:stateMachine:InsereMarcacao', input = input_sf)
    except Exception as e:
        return JsonResponse({"message": e})  

    return JsonResponse(response)