from django.db import models
from django.contrib.auth.models import User

class Consultas(models.Model):
    """Stores info on an appointment
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    data_appointment = models.CharField(max_length=100)
    hora = models.IntegerField()
    especialidade = models.IntegerField()
    medico = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)

    class Meta:
        db_table = 'consultas'

class Medicos(models.Model):
    medico = models.CharField(max_length=100)
    hora = models.IntegerField()
    data_appointment = models.CharField(max_length=100)

    class Meta:
        db_table = 'medicos'
