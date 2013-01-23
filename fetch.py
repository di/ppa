#!/usr/bin/python

import requests
import time
import sys
from bs4 import BeautifulSoup

url = "https://wmq.etimspayments.com/pbw/onlineDisputeAction.doh"
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"92",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"JSESSIONID=0000eLBlvGlUd2LxI7trTeg8ale:-1;Path=/",
    "Host":"wmq.etimspayments.com",
    "Origin":"https://wmq.etimspayments.com",
    "Referer":"https://wmq.etimspayments.com/pbw/confirmAgreementAction.doh",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17",
}

# Fetching a specific ticket when we know the magic-number
def fetch(_id, magic_num) :
    full_id = int(_id*10 + magic_num)
    payload = {'clientcode' : '02',
               'requestType' : 'submit',
               'clientAccount' : '5',
               'actionType' : 'I',
               'ticket' : full_id,
               'submit' : 'Submit'}
    r = requests.post(url, data=payload, headers=headers)
    time.sleep(1) # sleep for a bit
    soup = BeautifulSoup(r.content)
    tr = soup.find_all("form", attrs={'name':'onlineDisputeForm'})[0]
    if str(tr.table.contents[1].contents[3].text.strip()) == str(full_id) :
        return True, {
            "_id" : int(_id),
            "magic-num" : magic_num,
            "plate" : tr.find("input", attrs={'name':'plate'})['value'],
            "violationCode" : tr.find("input", attrs={'name':'violationCode'})['value'],
            "location" : tr.table.contents[1].contents[9].text.strip(),
            "violation" : tr.table.contents[5].contents[3].text.strip(),
            "meterNumber" : tr.table.contents[7].contents[3].text.strip(),
            "time" : tr.table.contents[3].contents[9].text.strip(),
            "issueDate" : tr.table.contents[3].contents[3].text.strip(),
            "resolved" : False
        }
    elif "$0.00" in soup.find_all("li", attrs={'class':'error'})[0].text.strip() :
        return True, {
            "_id" : int(_id),
            "magic-num" : magic_num,
            "resolved" : True
        }
    elif "unavailable" in soup.find_all("li", attrs={'class':'error'})[0].text.strip() :
        sys.exit(1)
    else :
        return False, None

# Fetching a ticket when we don't know the magic-number
def fetch_range(_id) :
    for magic_num in range(0,10) :
        valid, r = fetch(_id, magic_num)
        if valid :
            return r
    else :
        return {
            "_id" : int(_id),
            "missing" : True
        }
