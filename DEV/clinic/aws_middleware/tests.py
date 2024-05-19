from unittest.mock import patch

import boto3
from django.core.files.uploadedfile import SimpleUploadedFile

from clinic.tests import BaseTestCase
from clinic.settings import S3_IMAGE_BUCKET_NAME

from .s3 import s3_upload
from .stepfunctions import execute_workflow


class TestS3Uploads(BaseTestCase):
    """Tests uploading of s3 objects"""

    @patch("aws_middleware.s3.client")
    def test_upload_image(self, mock_boto_client):
        """Tests if an image can be uploaded to a given s3 bucket"""
        mock_boto_client.return_value = boto3.client("s3")

        image_key = "image_key"
        image_file = SimpleUploadedFile(
            "image", b"image data", content_type="image/jpeg"
        )
        self.assertTrue(s3_upload(image_key, image_file, S3_IMAGE_BUCKET_NAME))

    @patch("aws_middleware.stepfunctions.client")
    @patch("aws_middleware.stepfunctions.client.describe_execution")
    def test_execute_workflow(self, mock_boto_client, mock_describer):
        """Tests if a workflow can be executed"""
        mock_boto_client.return_value = boto3.client("stepfunctions", region_name="us-east-1")
        mock_describer.return_value = {"status": "SUCCEEDED", "output": "workflow output"}

        self.assertTrue(
            execute_workflow(
                {"payload": "data"},
                "arn:aws:states:us-east-1:123456789012:stateMachine:InsereMarcacao",
            )
        )
