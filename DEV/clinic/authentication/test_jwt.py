from datetime import datetime
from clinic.tests import BaseTestCase, INVALID_TOKEN

from .jwt import (
    generate_token,
    validate_token,
    verify_expiry,
    verify_format,
    JwtPayload,
)

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
