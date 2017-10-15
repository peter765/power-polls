import json
import re
import requests
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
BILL_API = "https://api.propublica.org/congress/v1/bills/search.json/"
MEMBER_API = "https://api.propublica.org/congress/v1/members/{}.json" #{member_id}.json
MEMBER_BILL_API = "https://api.propublica.org/congress/v1/members/{}/bills/cosponsored.json"
'''
data_access()
gets bill data
'''
def data_access():
    req = requests.get(BILL_API, headers=HEADERS)
    data = req.json()
    bills = {}
    for bill in data['results'][0]['bills']:
        id = bill['bill_id']
        url = bill['govtrack_url']
        cur_bill = {}
        cur_bill['components'] = extract_components(id, url)
        cur_bill['num_components'] = len(cur_bill['components'])
        bills[id] = cur_bill
    return bills
        
'''
extract_components(bill_id, url):
bill_id: bill_id for database storage
url: url to access congress.gov
'''
def extract_components(bill_id, url):
    url = url + "/text"

    browser = RoboBrowser(user_agent='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', history=True)
    browser.open(url)
    
    content = browser.find("section", class_="legis-body")
    if content is None:
        return []
    
    sections = content.find_all("section", class_="little-level")
    section_data = content.text
    parser = PlaintextParser.from_string(section_data, Tokenizer("english"))
    summarizer = LsaSummarizer()
    num_sentences = 10 if len(sections) > 10 else len(sections)
    summary = summarizer(parser.document, num_sentences)

    return list(set(summary))

    '''
    text = content.find_all("section", class_="little-level")
    for item in text:
        
        section_data = item.text
        parser = PlaintextParser.from_string(section_data, Tokenizer("english"))
        summarizer = LexRankSummarizer()

        summary = summarizer(parser.document, 1)

        for sentence in summary:
            print(sentence)
        
        print(item.text)
        print("---------")

    
    '''

'''
collects memberinfo from propublica API based on member_ID
gets information for representative/senator
also includes lists of cosponsored bills
'''

def member_info(member_ID):
    #get member info 
    req_url = MEMBER_API.format(str(member_ID))
    member = requests.get(req_url, headers=HEADERS)
    member_bio = member.json()
    #import pdb; pdb.set_trace()
    
    #get member's cosponsored bills
    req_url = MEMBER_BILL_API.format(str(member_ID))
    bills = requests.get(req_url, headers=HEADERS)

    member_bills = bills.json()['results'][0]['bills']

    member_bio['bills'] = member_bills
    return member_bio
    
print(data_access())

#print(member_info("K000388"))