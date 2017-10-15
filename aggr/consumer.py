import json
import re
import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from random import randint
import time
import datetime
import datetime
import boto3
import time
import pprint
#AWS
AWS_ACCESS_KEY='AKIAJCYCZPH7F53LXXHQ'
AWS_SECRET_KEY='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'

ES_ENDPOINT="search-hackgt-t4clvnkl4gw4wkhiv6fkwd6ebi.us-east-1.es.amazonaws.com"
ES_INDEX="sensordata"
# AWS KEYS
REGION="us-east-1"

# Get proper credentials for ES auth
awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION, 'es')

# Connect to ES
es = Elasticsearch(
    [ES_ENDPOINT],
    http_auth=awsauth,
    use_ssl=True,
    port=443,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

sqs = boto3.resource('sqs', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=REGION)

        


# Get the queue
queue = sqs.get_queue_by_name(QueueName='voting_queue')


def insert_document(es, record):
    #record['ts'] = '{}'.format(record['ts'])
    record = json.loads(record)
    del record['voterId']
    pprint.pprint(es)
    pprint.pprint(record)
    doc = json.dumps(record)

    es.index(index=ES_INDEX,
             body=doc,
             doc_type=ES_INDEX,
             id=record['timestamp'],
             refresh=True)

while True:
    for message in queue.receive_messages(MaxNumberOfMessages=1):
        print(message.body)
        data = message.body
        message.delete()
        insert_document(es, data)	
    time.sleep(1)


