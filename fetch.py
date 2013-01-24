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
def fetch(_id, magic_num, secs=5) :
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
        print "%s %d %s" % ("Oops, we brought it down, backing off for", secs, "seconds...")
        time.sleep(secs)
        return fetch(_id, magic_num, secs*2) 
    else :
        return False, None

# Fetching a ticket when we don't know the magic-number
def fetch_range(_id, lmn=None, pmn=None) :
    range = []
    if pmn is not None :
        pmn = int(pmn)
        _range = [(pmn+8)%10, (pmn+7)%10, (pmn+6)%10]
    elif lmn is not None :
        lmn = int(lmn)
        _range = [(lmn-8)%10, (lmn-7)%10, (lmn-6)%10]
    else :
        _range = [9, 1, 0, 8, 4, 6, 7, 3, 2, 5]
    for magic_num in _range :
        valid, r = fetch(_id, magic_num)
        if valid :
            return r
    else :
        return {
            "_id" : int(_id),
            "missing" : True
        }

