import boto3
from moto import mock_aws
from django.core.files.uploadedfile import SimpleUploadedFile

from clinic.tests import BaseTestCase
from clinic.settings import S3_IMAGE_BUCKET_NAME

from .s3 import s3_upload

class TestS3Uploads(BaseTestCase):
    """Tests uploading of s3 objects
    """

    def setUp(self):
        super().setUp()

        self.mock_aws = mock_aws()
        self.mock_aws.start()

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(S3_IMAGE_BUCKET_NAME)
        bucket.create()

    def tearDown(self) -> None:
        self.mock_aws.stop()
        super().tearDown()

    def test_upload_image(self):
        """Tests if an image can be uploaded to a given s3 bucket
        """
        image_key = "image_key"
        image_file = SimpleUploadedFile("image", b"image data", content_type="image/jpeg")
        self.assertTrue(s3_upload(image_key, image_file, S3_IMAGE_BUCKET_NAME))
