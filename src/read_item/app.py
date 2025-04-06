import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    item_id = event['pathParameters']['id']
    response = table.get_item(Key={'id': item_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'body': json.dumps({'message': 'Item not found'})}
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }
