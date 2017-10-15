
import requests
import time
import random
ENDPOINT = 'https://p49g8wr8d3.execute-api.us-east-1.amazonaws.com/dev/vote'

bills = [
    ('hconres', 84),
    ('hjres', 117),
    ('hr', 4066),
    ('hres', 572),
    ('s', 1956),
    ('sconres', 23),
    ('sres', 288),
    ('sjres', 47)
]

def generate_vote():
    bill = random.choice(bills)
    return {
        'voterId': '{0:09}'.format(random.randint(0, 3149)),
        'billId': bill[0] + str(random.randint(1, bill[1])) + str('-115'),
        'vote': random.choice(['yes', 'no']),
        'component': random.randint(1, 4),
        'congress': '115'
    }

while True:
    params = generate_vote()
    print(params)
    requests.get(ENDPOINT, params=params)
    time.sleep(1)