import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    item_id = event['pathParameters']['id']
    data = json.loads(event['body'])

    update_expression = "SET "
    expression_values = {}
    for key, value in data.items():
        update_expression += f"{key} = :{key}, "
        expression_values[f":{key}"] = value
    update_expression = update_expression.rstrip(', ')

    table.update_item(
        Key={'id': item_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item updated'})
    }
