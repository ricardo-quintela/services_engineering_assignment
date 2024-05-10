from django.contrib.auth.models import User
from django.test import TestCase
from random import randint

from rest_framework.test import APIClient
from .jwt import generate_token, validate_token

NUM_USERS = 10

class BaseTestCase(TestCase):
    """Sets Up the database and test client for the tests
    """
    def setUp(self) -> None:
        self.client = APIClient()
        self.users = list()

        for i in range(1, NUM_USERS+1):
            self.users.append(User.objects.create(username=f"test_user{i}", password=f"test_password{i}"))


# Create your tests here.
class TestUserEndPoints(BaseTestCase):
    """Tests all the User model related endpoints
    """

    def test_get_user(self):
        """Tests if a random user in the database can be returned
        """
        user_id = randint(1, NUM_USERS)
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content,
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
        self.assertJSONEqual(
            response.content,
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
        self.assertJSONEqual(
            response.content,
            {"error": "User does not exist."}
        )



class TestJWT(BaseTestCase):

    def test_create_jwt(self):
        """Test if a valid JWT can be generated with user data
        """
        user = self.users[0] # user 1
        generated_token = generate_token(user)
        self.assertRegex(
            generated_token,
            r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)"
        )

    def test_verify_token(self):
        """Tests if a token can be validated
        """
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQxIn0.pgFzfEvsUFi9yYhSUfW0psegUlF4zYWitKo4Yf71HrA"

        self.assertDictEqual(
            validate_token(token),
            {
                "username": self.users[0].username,
                "password": self.users[0].password
            }
        )

    def test_verify_invalid_token(self):
        """Tests if an invalid token returns None
        """
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQxIn0.hOU0Bz8QRxlEcxkHOLrWU7pDpJ6oEmBxEYj2hXQacaE"

        self.assertIsNone(
            validate_token(token)
        )
