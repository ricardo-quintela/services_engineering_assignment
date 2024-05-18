"""Tests appointment related endpoints
"""
# pylint: disable=no-member
import json
from datetime import datetime

from authentication.serializers import UserSerializer
from authentication.jwt import generate_token
from clinic.tests import BaseTestCase, INVALID_TOKEN

from .models import Consultas

NUM_APPOINTMENTS = 3


class TestAppointments(BaseTestCase):
    """Tests appointment related endpoints"""

    def setUp(self):
        super().setUp()

        self.appointments = list()
        now = datetime.now()

        for i in range(NUM_APPOINTMENTS):
            appointment = Consultas.objects.create(
                user=self.users[i],
                data_appointment=f"{now.date()}",
                hora=10,
                especialidade=2,
                medico="doctor",
                estado="open",
            )
            self.appointments.append(appointment)

    def test_get_appointments(self):
        """Tests if an admin can get all the appointments"""
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.get("/appointments/")

        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": appointment.id,
                    "user": UserSerializer(appointment.user).data,
                    "data_appointment": appointment.data_appointment,
                    "hora": appointment.hora,
                    "especialidade": appointment.especialidade,
                    "medico": appointment.medico,
                    "estado": appointment.estado,
                }
                for appointment in self.appointments
            ],
        )

    def test_get_appointments_not_admin(self):
        """Tests if a regular user is blocked from accessing the appointments data"""
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get("/appointments/")

        self.assertJSONEqual(response.content, {"error": "Forbidden."})

    def test_close_appointment(self):
        """Tests if an admin can alter an appointment's field"""
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.put("/appointments/1/", data={"estado": "closed"})

        self.assertJSONEqual(
            response.content,
            {
                "id": self.appointments[0].id,
                "user": UserSerializer(self.appointments[0].user).data,
                "data_appointment": self.appointments[0].data_appointment,
                "hora": self.appointments[0].hora,
                "especialidade": self.appointments[0].especialidade,
                "medico": self.appointments[0].medico,
                "estado": "closed",
            },
        )

    def test_close_appointment_wrong_attribute(self):
        """Tests if the attribute's name is not changed if the name is incorrect"""
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.put(
            "/appointments/1/",
            data={"unexistent_attribute": "value"},
        )

        self.assertJSONEqual(
            response.content,
            {"error": "Appointment has no field named 'unexistent_attribute'"},
        )

    def test_close_appointment_not_admin(self):
        """Tests if a regular user is blocked from accessing the appointments data"""
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.put(
            "/appointments/1/",
            data={"estado": "closed"},
        )

        self.assertJSONEqual(response.content, {"error": "Forbidden."})


    def test_scheduling(self):
        """Tests if a regular user can schedule an appointment"""
        self.client.cookies.load({"jwt": generate_token(self.users[0])})

        response = self.client.post(
            "/scheduling/",
            data={
                "cliente": "rafa",
                "data": "123",
                "horario": 12,
                "especialidade": 2,
                "medico": "doctor",
                "estado": "open"
            }
        )
        print(response.content)
        self.assertTrue("message" in json.loads(response.content))

    def test_scheduling_not_authenticated(self):
        """Tests if a regular user that is not logged in cannot schedule an appointment"""
        self.client.cookies.load({"jwt": INVALID_TOKEN})

        response = self.client.post(
            "/scheduling/",
            data={
                "data": "123",
                "hora": 12,
                "especialidade": 2,
                "medico": "doctor"
            }
        )
        self.assertJSONEqual(
            response.content,
            {"error": "User is not logged in."}
        )

    def test_scheduling_invalid_payload(self):
        """Tests if an invalid payload is blocked"""
        self.client.cookies.load({"jwt": generate_token(self.users[0])})

        response = self.client.post(
            "/scheduling/",
            data={
                "hora": 12,
                "especialidade": 2,
                "medico": "doctor"
            }
        )
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid payload."}
        )
