import base64
import json
import boto3

client = boto3.client("rekognition")


def lambda_handler(event, context):

    bucket_image = event["imageKey"]
    source_image = base64.b85decode(event["imageBytes"])
    bucket_name = event["bucketName"]

    try:
        response = client.compare_faces(
            SourceImage={"Bytes": source_image},
            TargetImage={"S3Object": {"Bucket": bucket_name, "Name": bucket_image}},
            SimilarityThreshold=90,
        )
    except client.exceptions.InvalidS3ObjectException:
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
