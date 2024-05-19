from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient
from moto import mock_aws
import boto3

from clinic.settings import S3_IMAGE_BUCKET_NAME

NUM_USERS = 10
INVALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3RfdXNlcjEiLCJ0aW1lc3RhbXAiOjE3MTUzNDA1NDAuMDAxMjIzLCJyb2xlIjpudWxsfQ.qrmwgNoyxCMRJ5QcmcWuH3DwyjMcqsPYMu438l2BvI0"


class BaseTestCase(TestCase):
    """Sets Up the database and test client for the tests"""

    def setUp(self) -> None:
        call_command("flush", "--noinput")
        self.client = APIClient()
        self.users: list[User] = list()
        self.admins: list[User] = list()
        self.groups: dict[str, Group] = dict()

        for i in range(1, NUM_USERS + 1):
            user = User.objects.create_user(
                username=f"test_user{i}", password=f"test_password{i}"
            )
            self.users.append(user)

        self.groups["admin"] = Group.objects.create(name="admin")
        self.admins.append(User.objects.create_user(username="admin", password="admin"))
        for admin in self.admins:
            admin.groups.add(self.groups["admin"])

        self.mock_aws = mock_aws()
        self.mock_aws.start()

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(S3_IMAGE_BUCKET_NAME)
        bucket.create()

        step_function = boto3.client("stepfunctions", region_name="us-east-1")
        with open(
            "../aws/state_machines/stepFunction_insereMarcacao.json",
            "r",
            encoding="utf-8",
        ) as f:
            definition = f.read()
        step_function.create_state_machine(
            name="InsereMarcacao",
            roleArn="arn:aws:iam::123456789012:role/unknown_sf_role",
            definition=definition,
        )

        with open(
            "../aws/state_machines/clinicStateMachine.json",
            "r",
            encoding="utf-8",
        ) as f:
            definition = f.read()
        step_function.create_state_machine(
            name="clinicStateMachine",
            roleArn="arn:aws:iam::123456789012:role/unknown_sf_role",
            definition=definition,
        )

    def tearDown(self) -> None:
        self.mock_aws.stop()
        super().tearDown()
