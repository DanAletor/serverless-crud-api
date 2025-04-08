import json
import os
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def lambda_handler(event, context):
    method = event['httpMethod']
    if method == 'POST':
        return create_item(event)
    elif method == 'GET':
        return get_item(event)
    elif method == 'PUT':
        return update_item(event)
    elif method == 'DELETE':
        return delete_item(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps('Method Not Allowed')
        }


def create_item(event):
    body = json.loads(event['body'])
    item_id = body.get('id')
    if not item_id:
        return {'statusCode': 400, 'body': json.dumps('ID is required')}

    try:
        table.put_item(Item=body)
        return {'statusCode': 201, 'body': json.dumps('Item created')}
    except ClientError as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}


def get_item(event):
    item_id = event['pathParameters']['id']
    try:
        response = table.get_item(Key={'id': item_id})
        if 'Item' not in response:
            return {'statusCode': 404, 'body': json.dumps('Item not found')}
        return {'statusCode': 200, 'body': json.dumps(response['Item'])}
    except ClientError as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}


def update_item(event):
    item_id = event['pathParameters']['id']
    body = json.loads(event['body'])
    try:
        table.update_item(
            Key={'id': item_id},
            UpdateExpression="set #name = :value",
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':value': body['name']}
        )
        return {'statusCode': 200, 'body': json.dumps('Item updated')}
    except ClientError as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}


def delete_item(event):
    item_id = event['pathParameters']['id']
    try:
        table.delete_item(Key={'id': item_id})
        return {'statusCode': 200, 'body': json.dumps('Item deleted')}
    except ClientError as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}
