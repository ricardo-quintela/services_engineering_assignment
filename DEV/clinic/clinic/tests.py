from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

NUM_USERS = 10

class BaseTestCase(TestCase):
    """Sets Up the database and test client for the tests
    """
    def setUp(self) -> None:
        self.client = APIClient()
        self.users = list()

        for i in range(1, NUM_USERS+1):
            user = User.objects.create_user(username=f"test_user{i}", password=f"test_password{i}")
            self.users.append(user)
