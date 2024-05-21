import json
import boto3

clientRekognition = boto3.client("rekognition")


def lambda_handler(event, context):

    image_key = event["imageUUID"]
    bucket_name = event["bucketName"]
    collection_id = event["collectionId"]

    try:
        response = clientRekognition.search_faces_by_image(
            CollectionId=collection_id,
            Image={
                "S3Object": {
                    "Bucket": bucket_name,
                    "Name": image_key
                }
            },
            MaxFaces=1
        )
    except clientRekognition.exceptions.InvalidS3ObjectException:
        return {
                "error": f"Object with key '{image_key}' doesn't exist on bucket '{bucket_name}'."
            }

    if response["FaceMatches"]:
        return {"faceId": response["FaceMatches"][0]["Face"]["FaceId"]}
    return {"error": "No faces were detected."}
