import boto3
from botocore.exceptions import ClientError
from clinic.settings import S3_BUCKET_URL

client = boto3.client("s3", endpoint_url=S3_BUCKET_URL)

def s3_upload(image_key: str, image_file: bytes, bucket_name: str) -> bool | str:
    """Uploads an image to an s3 bucket

    Args:
        image_key (str): the key to give to the image on the bucket
        image_file (bytes): the image file to upload
        bucket_name (str): the name of the bucked to upload the image to

    Returns:
        bool: True if the upload is successful, False otherwise
    """
    try:
        client.upload_fileobj(image_file, bucket_name, image_key)
    except ClientError as e:
        return str(e)

    return True
