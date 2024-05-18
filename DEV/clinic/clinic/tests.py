from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

NUM_USERS = 10
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJ0aW1lc3RhbXAiOjE3MTUzNDA1NDAuMDAxMjIzLCJyb2xlIjpudWxsfQ.qrmwgNoyxCMRJ5QcmcWuH3DwyjMcqsPYMu438l2BvI0"

class BaseTestCase(TestCase):
    """Sets Up the database and test client for the tests
    """

    @override_settings(EBS_HOST="localhost")
    @override_settings(S3_BUCKET_URL="http://127.0.0.1:9090")
    @override_settings(S3_BUCKET_NAME="frontend")
    def setUp(self) -> None:
        call_command('flush', '--noinput')
        self.client = APIClient()
        self.users: list[User] = list()
        self.admins: list[User] = list()
        self.groups: dict[str, Group] = dict()

        for i in range(1, NUM_USERS+1):
            user = User.objects.create_user(username=f"test_user{i}", password=f"test_password{i}")
            self.users.append(user)

        self.groups["admin"] = Group.objects.create(name="admin")
        self.admins.append(
            User.objects.create_user(username="admin", password="admin")
        )
        for admin in self.admins:
            admin.groups.add(self.groups["admin"])
