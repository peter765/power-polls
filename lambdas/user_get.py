import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
def handler(event, context):
    
    # DynamoDB access
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    
    # If bill_id given, query it
    if 'voterId' in event and event['voterId']:
        items = table.get_item(Key={'voterId': event['voterId']})
        if items:
            return items['Item']
        else:
            raise ValueError(event['voterId'] + ' is not valid.')
    
    return table.scan()