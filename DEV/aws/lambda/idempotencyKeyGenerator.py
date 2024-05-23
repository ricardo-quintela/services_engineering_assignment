import json
import hashlib
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("idempotencyCache")

def lambda_handler(event, context):
    
    request_id = hashlib.sha256(json.dumps(event).encode("utf-8")).hexdigest()
    
    try:
        response = table.get_item(Key={"requestId": request_id})
        if "Item" in response:
            return {
                'statusCode': 403,
                'error': "Consulta já tinha sido paga."
            }
    except ClientError:
        return {
            'statusCode': 500,
            'error': "Ocorreu um erro ao ligar à cache."
        }
        
    table.put_item(Item={"requestId": request_id})

    return {
        'statusCode': 200,
        'message': "Chave inserida." 
    }