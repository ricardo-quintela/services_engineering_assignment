from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import Consultas

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for the Appointment model
    """
    user = UserSerializer()

    class Meta:
        model = Consultas
        fields = ["id", "user", "data_appointment", "hora", "especialidade", "medico", "estado"]
