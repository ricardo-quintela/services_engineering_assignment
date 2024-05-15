from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    """Stores info on an appointment
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    horario = models.CharField(max_length=30)
    especialidade = models.CharField(max_length=30)
    medico = models.CharField(max_length=30)
    estado = models.CharField(max_length=20)
