# pylint: disable=no-member
from django.http import HttpRequest, JsonResponse
from django.core.exceptions import FieldDoesNotExist

from rest_framework.decorators import api_view
from authentication.jwt import perm_required

from .models import Appointment
from .serializers import AppointmentSerializer

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
