from random import randint
from unittest.mock import patch

import boto3
from django.core.files.uploadedfile import SimpleUploadedFile

from clinic.tests import BaseTestCase, INVALID_TOKEN
from clinic.settings import MAX_FILE_SIZE

from .jwt import generate_token


# Create your tests here.
class TestUserEndPoints(BaseTestCase):
    """Tests all the User model related endpoints"""

    def test_get_user(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        response = self.client.get(
            f"/users/{user_id}/", headers={"jwt": generate_token(self.admins[0])}
        )
        self.assertJSONEqual(
            response.content, {"id": user_id, "username": f"test_user{user_id}"}
        )

    def test_get_user_not_authenticated(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        response = self.client.get(f"/users/{user_id}/", headers={"jwt": INVALID_TOKEN})
        self.assertJSONEqual(response.content, {"error": "User is not logged in."})

    def test_get_user_not_admin(self):
        """Tests if a random user in the database can be returned"""
        user_id = randint(1, len(self.users))
        response = self.client.get(
            f"/users/{user_id}/", headers={"jwt": generate_token(self.users[0])}
        )
        self.assertJSONEqual(response.content, {"error": "Forbidden."})

    def test_get_all_users(self):
        """Tests if all the users in the database are returned"""
        response = self.client.get(
            "/users/", headers={"jwt": generate_token(self.admins[0])}
        )
        self.assertJSONEqual(
            response.content,
            [
                {"id": i, "username": f"{(self.users+self.admins)[i-1].username}"}
                for i in range(1, len(self.users) + len(self.admins) + 1)
            ],
        )

    @patch("aws_middleware.stepfunctions.client.describe_execution")
    def test_upload_file(self, mock_describer):
        """Tests if an authenticated user can upload a profile picture"""
        mock_describer.return_value = {
            "status": "SUCCEEDED",
            "output": "stepfunction output",
        }

        image = SimpleUploadedFile(
            "profile.jpg", b"image_content", content_type="image/jpeg"
        )
        response = self.client.post(
            "/image/", {"file": image}, headers={"jwt": generate_token(self.users[0])}
        )

        self.assertJSONEqual(
            response.content, {"message": "Imagem enviada com sucesso."}
        )

    def test_upload_file_not_authenticated(self):
        """Tests if a non authenticated user is stopped from uploading a file"""
        image = SimpleUploadedFile(
            "profile.jpg", b"image_content", content_type="image/jpeg"
        )
        response = self.client.post(
            "/image/", {"file": image}, headers={"jwt": INVALID_TOKEN}
        )

        self.assertJSONEqual(response.content, {"error": "User is not logged in."})

    def test_upload_file_not_supplied(self):
        """Stops a request that doesn't contain a file"""
        response = self.client.post(
            "/image/", headers={"jwt": generate_token(self.users[0])}
        )

        self.assertJSONEqual(response.content, {"error": "Nenhuma imagem selecionada."})

    def test_upload_file_too_big(self):
        """Stops a request that doesn't contain a file"""
        image = SimpleUploadedFile(
            "profile.jpg", b"a" * (MAX_FILE_SIZE + 1), content_type="image/jpeg"
        )
        response = self.client.post(
            "/image/",
            data={"file": image},
            headers={"jwt": generate_token(self.users[0])},
        )

        self.assertJSONEqual(
            response.content, {"error": "Tamanho máximo excedido."}
        )
