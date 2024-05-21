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
            "output": '{"Item":{"faceId":{"S":"d484e16f-b3f3-47e3-ae1d-d986bfba3412"},"username":{"S":"test_user1"}},"SdkHttpMetadata":{"AllHttpHeaders":{"Server":["Server"],"Connection":["keep-alive"],"x-amzn-RequestId":["3578OK12RVJV22GL2JN8I0CN2RVV4KQNSO5AEMVJF66Q9ASUAAJG"],"x-amz-crc32":["1056373934"],"Content-Length":["89"],"Date":["Tue, 21 May 2024 15:29:14 GMT"],"Content-Type":["application/x-amz-json-1.0"]},"HttpHeaders":{"Connection":"keep-alive","Content-Length":"89","Content-Type":"application/x-amz-json-1.0","Date":"Tue, 21 May 2024 15:29:14 GMT","Server":"Server","x-amz-crc32":"1056373934","x-amzn-RequestId":"3578OK12RVJV22GL2JN8I0CN2RVV4KQNSO5AEMVJF66Q9ASUAAJG"},"HttpStatusCode":200},"SdkResponseMetadata":{"RequestId":"3578OK12RVJV22GL2JN8I0CN2RVV4KQNSO5AEMVJF66Q9ASUAAJG"}}',
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
            response.content, {"message": "test_user1"}
        )
