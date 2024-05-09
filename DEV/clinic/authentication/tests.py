from django.contrib.auth.models import User
from django.test import TestCase
from random import randint

from rest_framework.test import APIClient

NUM_USERS = 10


# Create your tests here.
class TestUserEndPoints(TestCase):
    """Tests all the User model related endpoints
    """

    def setUp(self) -> None:
        self.client = APIClient()

        for i in range(1, NUM_USERS+1):
            User.objects.create(username=f"test_user{i}", password=f"test_password{i}")

    def test_get_user(self):
        """Tests if a random user in the database can be returned
        """
        user_id = randint(1, NUM_USERS)
        response = self.client.get(f"/users/{user_id}/")
        self.assertDictEqual(
            response.data,
            {
                "id": user_id,
                "username": f"test_user{user_id}",
                "password": f"test_password{user_id}",
            }
        )

    def test_get_all_users(self):
        """Tests if all the users in the database are returned
        """
        response = self.client.get("/users/")
        self.assertListEqual(
            response.data,
            [
                {"id": i, "username": f"test_user{i}", "password": f"test_password{i}"}
                for i in range(1, NUM_USERS+1)
            ]
        )

    def test_get_invalid_user(self):
        """Tests if getting an invalid user will return an error message
        """
        user_id = NUM_USERS+1
        response = self.client.get(f"/users/{user_id}/")
        self.assertDictEqual(
            response.data,
            {"error": "User does not exist."}
        )
