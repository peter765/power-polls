import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
def handler(event, context):
    LIMIT = 100
    
    # DynamoDB access
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    
    # If bill_id given, query it
    if 'billId' in event and event['billId'] and 'congress' in event and event['congress']:
        items = table.get_item(Key={'bill_id': event['billId'], 'congress': event['congress']})
        if items:
            return items
        else:
            raise ValueError(event['billId'] + ' is not valid.')
    
    if 'trend' in event:
        items = table.query(
            IndexName='congress-total_votes-index-copy',
            KeyConditionExpression=Key('congress').eq('115'),
            ScanIndexForward=False,
            Limit=int(event.get('limit', 10)))
        return items
        
    if 'limit' in event:
        LIMIT = event['limit']
        items = table.scan(Limit=LIMIT)
        return items
    