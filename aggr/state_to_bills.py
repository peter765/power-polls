"""
States to number of bills.
"""
import boto3
AWS_ACCESS_KEY='AKIAJCYCZPH7F53LXXHQ'
AWS_SECRET_KEY='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'
REGION="us-east-1"

def get_state_to_bills():

    dynamodb = boto3.resource('dynamodb',
                                aws_access_key_id=AWS_ACCESS_KEY,
                                aws_secret_access_key=AWS_SECRET_KEY,
                                region_name=REGION)

    table = dynamodb.Table('bills')
    response = table.scan()
    bills = response['Items']

    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        bills.extend(response['Items'])

    states = {}
    for bill in bills:
        states[bill['sponsor']['state']] = states.get(bill['sponsor']['state'], 0) + 1
    print(states)
    return states

get_state_to_bills()