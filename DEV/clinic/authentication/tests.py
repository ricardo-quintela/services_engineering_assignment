from django.contrib.auth.models import User
from django.test import TestCase
from random import randint

from rest_framework.test import APIClient
from .jwt import generate_token, validate_token, verify_expiry, verify_format, JwtPayload
from datetime import datetime

NUM_USERS = 10

INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQxIiwidGltZXN0YW1wIjoxNzE1MzQwNTQwLjAwMTIyM30.xktKTj9uy3wFoD4OL58u2V39DIi9d92RSG7jWopyfw0"

class BaseTestCase(TestCase):
    """Sets Up the database and test client for the tests
    """
    def setUp(self) -> None:
        self.client = APIClient()
        self.users = list()

        for i in range(1, NUM_USERS+1):
            user = User.objects.create_user(username=f"test_user{i}", password=f"test_password{i}")
            self.users.append(user)


# Create your tests here.
class TestUserEndPoints(BaseTestCase):
    """Tests all the User model related endpoints
    """

    def test_get_user(self):
        """Tests if a random user in the database can be returned
        """
        user_id = randint(1, NUM_USERS)
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content,
            {
                "id": user_id,
                "username": f"test_user{user_id}"
            }
        )

    def test_get_user_not_authenticated(self):
        """Tests if a random user in the database can be returned
        """
        user_id = randint(1, NUM_USERS)
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content,
            {
                "error": "User is not logged in."
            }
        )

    def test_get_all_users(self):
        """Tests if all the users in the database are returned
        """
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get("/users/")
        self.assertJSONEqual(
            response.content,
            [
                {"id": i, "username": f"test_user{i}"}
                for i in range(1, NUM_USERS+1)
            ]
        )

    def test_get_all_users_not_authenticated(self):
        """Tests if a random user in the database can be returned
        """
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get("/users/")
        self.assertJSONEqual(
            response.content,
            {
                "error": "User is not logged in."
            }
        )


    def test_get_invalid_user(self):
        """Tests if getting an invalid user will return an error message
        """
        user_id = NUM_USERS+1
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content,
            {"error": "User does not exist."}
        )

    def test_get_invalid_user_not_authenticated(self):
        """Tests if getting an invalid user will return an error message
        """
        user_id = NUM_USERS+1
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content,
            {
                "error": "User is not logged in."
            }
        )


    def test_login_valid_credentials(self):
        """Tests if a user can successfully login
        """
        response = self.client.post(
            "/login/",
            data={
                "username": "test_user1",
                "password": "test_password1"
            }
        )
        self.assertRegex(
            response.cookies["jwt"].value,
            r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)"
        )

    def test_login_invalid_username(self):
        """Tests if a user cannot login with an invalid username
        """
        response = self.client.post(
            "/login/",
            data={
                "username": "unexistent_username",
                "password": "password"
            }
        )
        self.assertJSONEqual(
            response.content,
            {
                "error": "Invalid username."
            }
        )

    def test_login_invalid_password(self):
        """Tests if a user cannot login with an invalid password
        """
        response = self.client.post(
            "/login/",
            data={
                "username": "test_user1",
                "password": "unexistent_password"
            }
        )
        self.assertJSONEqual(
            response.content,
            {
                "error": "Invalid password."
            }
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
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQxIiwidGltZXN0YW1wIjoxNzE1MzQwNTQwLjAwMTIyM30.xktKTj9uy3wFoD4OL58u2V39DIi9d92RSG7jWopyfw0"

        self.assertDictEqual(
            validate_token(token),
            {
                "username": "test_user1",
                "password": "test_password1",
                "timestamp": 1715340540.001223
            }
        )

    def test_verify_invalid_token(self):
        """Tests if an invalid token returns None
        """
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJwYXNzd29yZCI6InRlc3RfcGFzc3dvcmQxIiwidGltZXN0YW1wIjoxNzE1MzQwNTQwLjAwMTIyM30.J5FvcrY52ySpWvKLHAwCI70mSuZVkaoeKaEWZoEH360"

        self.assertIsNone(
            validate_token(token)
        )

    def test_valid_token_expiry(self):
        """Tests if a payload from a token with a valid timestamp is accepted
        """
        self.assertTrue(
            verify_expiry(
                JwtPayload(
                    username="test_user1",
                    password="test_password1",
                    timestamp=datetime.now().timestamp()
                )
            )
        )

    def test_invalid_token_expiry(self):
        """Tests if a payload from a token with an expired timestamp is rejected
        """
        self.assertFalse(
            verify_expiry(
                JwtPayload(
                    username="test_user1",
                    password="test_password1",
                    timestamp=datetime(1999,1,1).timestamp()
                )
            )
        )

    def test_token_valid_format(self):
        """Tests if a token in a valid format is accepted
        """
        self.assertEqual(
            verify_format(
                {
                    "username": "test_user1",
                    "password": "test_password1",
                    "timestamp": datetime(1999,1,1).timestamp()
                }
            ),
            JwtPayload(
                username="test_user1",
                password="test_password1",
                timestamp=datetime(1999,1,1).timestamp()
            )
        )

    def test_token_invalid_format(self):
        """Tests if a token in an invalid format is rejected
        """
        self.assertIsNone(
            verify_format(
                {
                    "username": "test_user1",
                    "password": "test_password1",
                }
            )
        )
