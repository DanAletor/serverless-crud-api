import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    item_id = str(uuid.uuid4())
    item = {
        'id': item_id,
        'name': data['name'],
        'description': data.get('description', '')
    }
    table.put_item(Item=item)
    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'Item created', 'id': item_id})
    }
