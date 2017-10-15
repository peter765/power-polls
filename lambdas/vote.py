import boto3
import os
import copy
import time
import json
import datetime

from boto3.dynamodb.conditions import Key, Attr
def handler(event, context):
    # DynamoDB access
    dynamodb = boto3.resource('dynamodb')
    bill_table = dynamodb.Table(os.environ['DB_BILL_TABLE'])
    voter_table = dynamodb.Table(os.environ['DB_VOTER_TABLE'])
    
    # Attempt to vote
    if 'voterId' in event and event['voterId'] and 'billId' in event and event['billId'] and 'congress' in event and event['congress']:
        voter = voter_table.get_item(Key={'voterId': event['voterId']})["Item"]
        bill = bill_table.get_item(Key={'bill_id': event['billId'], 'congress': event['congress']})
        billId = event['billId']
        if 'vote' in event and event['vote'] and billId not in voter['votes']:
            
            # User has not voted, cast vote
            dct = voter['votes']
            if type(voter['votes']) == str:
                dct = dict()
            dct[billId] = event['vote'][0]
            
            
            voter_table.update_item(
                Key={
                    'voterId': event['voterId']
                },
                UpdateExpression="SET votes = :r",
                ExpressionAttributeValues={
                    ':r': dct,
                }
            )
            
            
            ts=time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            data = {
                "voterId": event['voterId'],
                "billId": event['billId'],
                "component": event['component'],
                "vote": event['vote'],
                'state': voter['state'],
                "timestamp": timestamp,
                "ts": ts
            }
            
            
            # SQS resource
            sqs = boto3.resource('sqs')
            # Get the queue
            queue = sqs.get_queue_by_name(QueueName='voting_queue')
            queue.send_message(MessageBody=json.dumps(data))
            
            return "Success"
        return "Already Voted"