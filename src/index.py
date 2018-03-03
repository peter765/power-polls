from flask import Flask
import pymongo
import boto3
import requests
import json
from bson.json_util import dumps
import time
from flask import Response, stream_with_context
from flask import render_template, redirect, render_template_string

uri = "mongodb://hackgt:IHUrK9eC7zt1X3AofIIgWmeByxSAg4kkZV8QNd8JKk1jTS5rSvOgNrcUPQKEx4rUYxrZM2mxRSYXywIBg9lWlw==@hackgt.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)

db = client['targets']
coll = db['sankey_graph']
cursor = coll.find({})


AWS_ACCESS_KEY=''
AWS_SECRET_KEY=''
REGION="us-east-1"



abbrev_to_full = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}


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
    return {abbrev_to_full[abv]: count for abv, count in states.items()}


app = Flask(__name__)
@app.route("/")
def index():
  #title, latest_major_action_date, $id, total_votes
  #fakeData = {'one': ['BillOne','2017-05-13','123',456],'two':['BillTwo','2017-03-13','589',654], 'three':['BillThree','2017-02-18','48',13]}
  #url="https://congress-app.azurewebsites.net/api/trending?code=YnQeg28fJHri0iFVl25OF8ggle9Wfc4d1fyAZl22NONQ7E6GtZZADw=="
  #heatMapData = get_state_to_bills()
  heatMapData = [];
  sankeyData = dumps(cursor)
  url="https://p49g8wr8d3.execute-api.us-east-1.amazonaws.com/dev/bill?trend=True&limit=9"
  topTenTrending = requests.request(method='get', url=url)
  topTenTrending = topTenTrending.json()

  return render_template("index.html", topTenTrending=json.dumps(topTenTrending), sankeyData=sankeyData, heatMapData=heatMapData)#data=json.dumps(response))

@app.route("/billview/<string:bill_id>", methods=['GET'])
def view_bill_details(bill_id):
  #summary
  fakeData = {'summary':'summary of infomration will go here','components':['componentid', 'information for compoenent component']}
  return render_template("summary.html", data=fakeData)


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8010)
