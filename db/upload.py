import boto3
import random
import time
import datetime
import glob
import json
import requests

AWS_ACCESS_KEY='AKIAJCYCZPH7F53LXXHQ'
AWS_SECRET_KEY='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'
REGION="us-east-1"

BILL_API = 'https://api.propublica.org/congress/v1/{congress}/bills/{bill_id}.json'

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_KEY,
                            aws_secret_access_key=AWS_SECRET,
                            region_name=REGION)

table = dynamodb.Table('bills')

def publish(data):
    table.put_item(
       Item=data
        )
    
def generate_votes():
    BIAS = random.randint(0, 300)
    STATES = {
        'AL': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'AK': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'AZ': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'AR': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'CA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'CO': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'CT': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'DE': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'FL': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'GA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'HI': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'ID': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'IL': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'IN': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'IA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'KS': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'KY': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'LA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'ME': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MD': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MI': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MN': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MS': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MO': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'MT': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NE': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NV': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NH': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NJ': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NM': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NY': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'NC': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'ND': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'OH': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'OK': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'OR': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'PA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'RI': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'SC': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'SD': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'TN': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'TX': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'UT': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'VT': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'VA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'WA': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'WV': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'WI': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
        'WY': {'yes': random.randint(0, 100), 'no': random.randint(0, 100)},
    }
    return STATES

import re
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
from sumy.summarizers.text_rank import TextRankSummarizer #We're choosing Lexrank, other algorithms are also built in
from sumy.summarizers.lsa import LsaSummarizer

HEADERS = {
    "X-API-Key":"Ol1yD7w4Ek75uBGo3tw1GJDBZExZXErw7WG15HDz",
    "user-agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    }
MEMBER_API = "https://api.propublica.org/congress/v1/members/{}.json" #{member_id}.json
MEMBER_BILL_API = "https://api.propublica.org/congress/v1/members/{}/bills/cosponsored.json"

def get_components(bill):
    return extract_components(bill['bill_id'], bill['govtrack_url'])
        
'''
extract_components(bill_id, url):
bill_id: bill_id for database storage
url: url to access congress.gov
'''
def extract_components(bill_id, url):
    url = url + "/text"
    print(url)

    browser = RoboBrowser(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', history=True)
    browser.open(url)
    #print(browser.parsed)
    
    content = browser.find("section", class_="legis-body")
    if content is None:
        print("NONE")
        return []
    
    sections = content.find_all("section", class_="little-level")
    section_data = content.text
    parser = PlaintextParser.from_string(section_data, Tokenizer("english"))
    summarizer = LsaSummarizer()
    num_sentences = 10 if len(sections) > 10 else len(sections)
    summary = summarizer(parser.document, num_sentences)

    return list(set(summary))




for name in glob.glob('bills/**/data.json', recursive=True):
    f = open(name, 'r')
    bill_dict = json.loads(f.read())
    #bill_dict['state_votes'] = generate_votes()
    #bill_dict['total_votes'] = sum([s['yes'] + s['no'] for s in bill_dict['state_votes'].values()])
    api_url = BILL_API.format(congress=bill_dict['congress'], bill_id=bill_dict['bill_id'][:-4])
    bill_dict_new = requests.get(api_url, headers=HEADERS).json().get('results')[0]
    comp = get_components(bill_dict_new)
    print(comp)
    bill_dict['components'] = comp
    bill_dict['num_components'] = len(comp)
    for key in bill_dict:
        if key == '':
            del bill_dict[key]
    try:
        pass
        #print(bill_dict)
        #publish(bill_dict)
    except:
        pass

