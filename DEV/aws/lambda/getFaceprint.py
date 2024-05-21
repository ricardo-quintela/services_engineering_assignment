import boto3

clientRekognition = boto3.client("rekognition")


def lambda_handler(event, context):

    username = event["username"]
    bucket_name = event["bucketName"]
    collection_id = event["collectionId"]

    try:
        response = clientRekognition.index_faces(
            CollectionId=collection_id,
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": username
                }
            },
            MaxFaces=1
        )
    except clientRekognition.exceptions.InvalidS3ObjectException:
        return {
                "error": f"Object with key '{username}' doesn't exist on bucket '{bucket_name}'."
            }

    if response["FaceRecords"]:
        return {"faceId": response["FaceRecords"][0]["Face"]["FaceId"], "username": username}
    return {"error": "No faces were detected."}
