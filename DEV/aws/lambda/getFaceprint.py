import json
import boto3

clientRekognition = boto3.client("rekognition")


def lambda_handler(event, context):

    bucket_image = event["imageKey"]
    bucket_name = event["bucketName"]

    try:
        response = clientRekognition.compare_faces(
            SourceImage={"S3Object": {"Bucket": bucket_name, "Name": bucket_image}},
            TargetImage={"S3Object": {"Bucket": bucket_name, "Name": bucket_image}},
            SimilarityThreshold=90,
        )
    except clientRekognition.exceptions.InvalidS3ObjectException:
        return json.dumps(
            {
                "error": f"Object with key '{bucket_image}' doesn't exist on bucket '{bucket_name}'."
            },
            indent=2,
        )

    if response["FaceMatches"]:
        return json.dumps(
            {"comparison_result": response["FaceMatches"][0]["Similarity"]}, indent=2
        )
    return json.dumps({"comparison_result": 0}, indent=2)
