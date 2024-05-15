from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for the Appointment model
    """
    user = UserSerializer()

    class Meta:
        model = Appointment
        fields = ["id", "user", "horario", "especialidade", "medico", "estado"]
