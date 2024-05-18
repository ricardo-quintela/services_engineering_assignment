from clinic.tests import BaseTestCase, INVALID_TOKEN

from .jwt import generate_token

class TestLoginEndpoints(BaseTestCase):
    """Tests the login and registration endpoints"""

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
