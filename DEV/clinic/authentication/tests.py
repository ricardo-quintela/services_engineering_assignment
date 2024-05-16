from datetime import datetime
from random import randint

from clinic.tests import BaseTestCase

from .jwt import (
    generate_token,
    validate_token,
    verify_expiry,
    verify_format,
    JwtPayload,
)

INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJ0aW1lc3RhbXAiOjE3MTUzNDA1NDAuMDAxMjIzLCJyb2xlIjpudWxsfQ.qrmwgNoyxCMRJ5QcmcWuH3DwyjMcqsPYMu438l2BvI0"


# Create your tests here.
class TestUserEndPoints(BaseTestCase):
    """Tests all the User model related endpoints"""

    def test_get_user(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(
            response.content, {"id": user_id, "username": f"test_user{user_id}"}
        )

    def test_get_user_not_authenticated(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(response.content, {"error": "User is not logged in."})

    def test_get_user_not_admin(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(response.content, {"error": "Forbidden."})

    def test_get_all_users(self):
        """Tests if all the users in the database are returned"""
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.get("/users/")
        self.assertJSONEqual(
            response.content,
            [
                {"id": i, "username": f"{(self.users+self.admins)[i-1].username}"}
                for i in range(1, len(self.users) + len(self.admins) + 1)
            ],
        )

    def test_get_all_users_not_authenticated(self):
        """Tests if a random user in the database can be returned"""
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get("/users/")
        self.assertJSONEqual(response.content, {"error": "User is not logged in."})

    def test_get_invalid_user(self):
        """Tests if getting an invalid user will return an error message"""
        user_id = len(self.users) + len(self.admins) + 1
        self.client.cookies.load({"jwt": generate_token(self.admins[0])})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(response.content, {"error": "User does not exist."})

    def test_get_invalid_user_not_authenticated(self):
        """Tests if getting an invalid user will return an error message"""
        user_id = len(self.users) + len(self.admins) + 1
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        response = self.client.get(f"/users/{user_id}/")
        self.assertJSONEqual(response.content, {"error": "User is not logged in."})

    def test_login_valid_credentials(self):
        """Tests if a user can successfully login"""
        response = self.client.post(
            "/login/", data={"username": "test_user1", "password": "test_password1"}
        )
        self.assertRegex(
            response.headers["jwt"],
            r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)",
        )

    def test_login_invalid_username(self):
        """Tests if a user cannot login with an invalid username"""
        response = self.client.post(
            "/login/", data={"username": "unexistent_username", "password": "password"}
        )
        self.assertJSONEqual(response.content, {"error": "Invalid username."})

    def test_login_invalid_password(self):
        """Tests if a user cannot login with an invalid password"""
        response = self.client.post(
            "/login/",
            data={"username": "test_user1", "password": "unexistent_password"},
        )
        self.assertJSONEqual(response.content, {"error": "Invalid password."})

    def test_register(self):
        """Tests if a new user can register on the website"""
        response = self.client.post(
            "/register/",
            data={
                "username": f"test_user{len(self.users)+len(self.admins)+2}",
                "password": f"test_password{len(self.users)+len(self.admins)+2}",
            },
        )
        self.assertJSONEqual(response.content, {"message": "Successfully registered."})

    def test_register_username_exists(self):
        """Tests if a new user can register on the website"""
        response = self.client.post(
            "/register/",
            data={
                "username": "test_user1",
                "password": "test_password1",
            },
        )
        self.assertJSONEqual(response.content, {"error": "User already exists."})


class TestJWT(BaseTestCase):
    """Tests token generation and validation"""

    def test_create_jwt(self):
        """Test if a valid JWT can be generated with user data"""
        user = self.users[0]  # user 1
        generated_token = generate_token(user)
        self.assertRegex(
            generated_token, r"(^[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$)"
        )

    def test_verify_token(self):
        """Tests if a token can be validated"""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJ0aW1lc3RhbXAiOjE3MTUzNDA1NDAuMDAxMjIzLCJyb2xlIjpudWxsfQ.it9lIbICZMTXOfvvZxNw6XiYTcTFjhpL9IQ6j1zNEe4"

        self.assertDictEqual(
            validate_token(token),
            {"username": "test_user1", "timestamp": 1715340540.001223, "role": None},
        )

    def test_verify_invalid_token(self):
        """Tests if an invalid token returns None"""
        self.assertIsNone(validate_token(INVALID_TOKEN))

    def test_valid_token_expiry(self):
        """Tests if a payload from a token with a valid timestamp is accepted"""
        self.assertTrue(
            verify_expiry(
                JwtPayload(
                    username="test_user1",
                    timestamp=datetime.now().timestamp(),
                    role=None,
                )
            )
        )

    def test_invalid_token_expiry(self):
        """Tests if a payload from a token with an expired timestamp is rejected"""
        self.assertFalse(
            verify_expiry(
                JwtPayload(
                    username="test_user1",
                    timestamp=datetime(1999, 1, 1).timestamp(),
                    role=None,
                )
            )
        )

    def test_token_valid_format(self):
        """Tests if a token in a valid format is accepted"""
        self.assertEqual(
            verify_format(
                {
                    "username": "test_user1",
                    "timestamp": datetime(1999, 1, 1).timestamp(),
                    "role": None,
                }
            ),
            JwtPayload(
                username="test_user1",
                timestamp=datetime(1999, 1, 1).timestamp(),
                role=None,
            ),
        )

    def test_token_invalid_format(self):
        """Tests if a token in an invalid format is rejected"""
        self.assertIsNone(
            verify_format(
                {
                    "username": "test_user1",
                }
            )
        )
