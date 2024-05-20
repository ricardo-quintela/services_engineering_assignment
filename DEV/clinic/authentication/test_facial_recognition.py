from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

from authentication.jwt import generate_token
from clinic.tests import BaseTestCase


class TestFacialRecognition(BaseTestCase):

    @patch("aws_middleware.stepfunctions.client.describe_execution")
    def test_facial_recognition(self, mock_describer):
        """Tests if an admin can run a facial recognition workflow"""
        mock_describer.return_value = {
            "status": "SUCCEEDED",
            "output": '"{\\"comparison_result\\": 100}"',
        }

        image = SimpleUploadedFile(
            "test_image.jpg", b"file content", content_type="image/jpeg"
        )
        response = self.client.post(
            "/recognition/",
            data={"file": image, "username": self.users[0].username},
            headers={"jwt": generate_token(self.admins[0])},
        )
        self.assertJSONEqual(
            response.content, {"message": {"comparison_result": 100}, "statusCode": 200}
        )
