import json
import time
import boto3
from django.http import JsonResponse


MAX_RETRIES = 3
TIMEOUT = 1


client = boto3.client("stepfunctions", region_name="us-east-1")


def execute_workflow(payload: dict, resource_arn: str) -> JsonResponse:
    """Executes a workflow on the stepfunction with the given arn

    Args:
        payload (dict): the json formated payload
        resource_arn (str): the arn identifier of the step function

    Returns:
        JsonResponse: a message containing the status of the request execution
    """
    try:
        json_input = json.dumps(payload)
    except TypeError:
        return JsonResponse({"error": "Invalid payload."})

    try:
        response = client.start_execution(
            stateMachineArn=resource_arn,
            input=json_input,
        )
        execution_arn = response["executionArn"]

    except Exception as e:
        return JsonResponse({"error": str(e)})

    for _ in range(MAX_RETRIES):
        try:
            response = client.describe_execution(executionArn=execution_arn)
        except Exception as e:
            return JsonResponse({"error": str(e)})

        status = response["status"]

        if status in ["SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED"]:
            if status == "FAILED":
                return JsonResponse({"error": response["error"], "statusCode": 500})
            return JsonResponse({"message": response["output"], "statusCode": 200})

        time.sleep(1)

    return JsonResponse({"error": "Step function execution timed out."})
