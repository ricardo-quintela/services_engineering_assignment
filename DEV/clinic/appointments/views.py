# pylint: disable=no-member
import json
import time

from django.http import HttpRequest, JsonResponse
from django.core.exceptions import FieldDoesNotExist

from rest_framework.decorators import api_view
from authentication.jwt import perm_required, validate_token, requires_jwt
from aws_middleware.stepfunctions import client

from .models import Consultas
from .serializers import AppointmentSerializer


MAX_RETRIES = 3
TIMEOUT = 1


@perm_required("admin")
@api_view(["GET"])
def all_appointments_view(_: HttpRequest) -> JsonResponse:

    appointments = Consultas.objects.all()

    serializer = AppointmentSerializer(appointments, many=True)

    return JsonResponse(serializer.data, safe=False)


@perm_required("admin")
@api_view(["PUT"])
def update_appointments_view(request: HttpRequest, _id: int) -> JsonResponse:

    appointment = Consultas.objects.filter(id=_id)
    if appointment is None:
        return JsonResponse({"error": "Appointment does not exist."})

    json_payload: dict = request.data

    try:
        appointment.update(**{k: json_payload.get(k) for k in json_payload})
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

    try:
        data = request.data["data"]
        hora = int(request.data["hora"])
        especialidade = int(request.data["especialidade"])
        medico = request.data["medico"]
    except KeyError:
        return JsonResponse({"error": "Invalid payload."})
    except ValueError:
        return JsonResponse({"error": "Invalid payload."})

    token = request.headers["jwt"]
    username = validate_token(token)["username"]

    input_sf = json.dumps(
        {
            "cliente": username,
            "data": data,
            "hora": hora,
            "especialidade": especialidade,
            "medico": medico,
            "estado": "open",
        }
    )

    try:
        response = client.start_execution(
            stateMachineArn="arn:aws:states:us-east-1:123456789012:stateMachine:InsereMarcacao",
            input=input_sf,
        )
        execution_arn = response["executionArn"]

    except Exception as e:
        return JsonResponse({"error": str(e)})

    for _ in range(MAX_RETRIES):
        try:
            response = client.describe_execution(executionArn=execution_arn)
        except Exception as e:
            return JsonResponse({"error": str(e)})

        status = response["status"]

        if status in ["SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"]:
            if status == "FAILED":
                return JsonResponse({"message": response["error"], "statusCode": 500})
            return JsonResponse({"message": "Insertion succeded", "statusCode": 200})

        time.sleep(1)

    return JsonResponse({"error": "Step function execution timed out."})
