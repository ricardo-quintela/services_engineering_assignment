"""Tests appointment related endpoints
"""

# pylint: disable=no-member
from datetime import datetime

from authentication.serializers import UserSerializer
from authentication.jwt import generate_token
from clinic.tests import BaseTestCase

from .models import Appointment

NUM_APPOINTMENTS = 3


class TestAppointments(BaseTestCase):
    """Tests appointment related endpoints"""

    def setUp(self):
        super().setUp()

        self.appointments = list()
        now = datetime.now()

        for i in range(NUM_APPOINTMENTS):
            appointment = Appointment.objects.create(
                user=self.users[i],
                horario=f"{now.date()}|{now.time()}",
                especialidade="specialty",
                medico="doctor",
                estado="open",
            )
            self.appointments.append(appointment)

    def test_get_appointments(self):
        """Tests if an admin can get all the appointments"""
        response = self.client.get(
            "/appointments/", headers={"jwt": generate_token(self.admins[0])}
        )

        self.assertJSONEqual(
            response.content,
            [
                {
                    "id": appointment.id,
                    "user": UserSerializer(appointment.user).data,
                    "horario": appointment.horario,
                    "especialidade": appointment.especialidade,
                    "medico": appointment.medico,
                    "estado": appointment.estado,
                }
                for appointment in self.appointments
            ],
        )

    def test_get_appointments_not_admin(self):
        """Tests if a regular user is blocked from accessing the appointments data"""
        response = self.client.get(
            "/appointments/", headers={"jwt": generate_token(self.users[0])}
        )

        self.assertJSONEqual(response.content, {"error": "Forbidden."})

    def test_close_appointment(self):
        """Tests if an admin can alter an appointment's field"""
        response = self.client.put(
            "/appointments/1/",
            data={"estado": "closed"},
            headers={"jwt": generate_token(self.admins[0])},
        )

        self.assertJSONEqual(
            response.content,
            {
                "id": self.appointments[0].id,
                "user": UserSerializer(self.appointments[0].user).data,
                "horario": self.appointments[0].horario,
                "especialidade": self.appointments[0].especialidade,
                "medico": self.appointments[0].medico,
                "estado": "closed",
            },
        )

    def test_close_appointment_wrong_attribute(self):
        """Tests if the attribute's name is not changed if the name is incorrect"""
        response = self.client.put(
            "/appointments/1/",
            data={"unexistent_attribute": "value"},
            headers={"jwt": generate_token(self.admins[0])},
        )

        self.assertJSONEqual(
            response.content,
            {"error": "Appointment has no field named 'unexistent_attribute'"},
        )

    def test_close_appointment_not_admin(self):
        """Tests if a regular user is blocked from accessing the appointments data"""
        response = self.client.put(
            "/appointments/1/",
            data={"estado": "closed"},
            headers={"jwt": generate_token(self.users[0])},
        )

        self.assertJSONEqual(response.content, {"error": "Forbidden."})
