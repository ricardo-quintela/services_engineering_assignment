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

    @patch("aws_middleware.s3.client")
    def test_upload_file(self, mock_boto_client):
        """Tests if an authenticated user can upload a profile picture
        """
        mock_boto_client.return_value = boto3.client("s3")

        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        image = SimpleUploadedFile("profile.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post("/image/", {"file": image})

        self.assertJSONEqual(
            response.content,
            {"message": "Image successfully uploaded."}
        )

    def test_upload_file_not_authenticated(self):
        """Tests if a non authenticated user is stopped from uploading a file
        """
        self.client.cookies.load({"jwt": INVALID_TOKEN})
        image = SimpleUploadedFile("profile.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post("/image/", {"file": image})

        self.assertJSONEqual(
            response.content,
            {"error": "User is not logged in."}
        )

    def test_upload_file_not_supplied(self):
        """Stops a request that doesn't contain a file
        """
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        response = self.client.post("/image/")

        self.assertJSONEqual(
            response.content,
            {"error": "No image was uploaded."}
        )

    def test_upload_file_too_big(self):
        """Stops a request that doesn't contain a file
        """
        self.client.cookies.load({"jwt": generate_token(self.users[0])})
        image = SimpleUploadedFile("profile.jpg", b"a"*(MAX_FILE_SIZE+1), content_type="image/jpeg")
        response = self.client.post("/image/", data={"file": image})

        self.assertJSONEqual(
            response.content,
            {"error": "Uploaded file excedes max size limit."}
        )
