import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    item_id = event['pathParameters']['id']
    table.delete_item(Key={'id': item_id})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item deleted'})
    }
