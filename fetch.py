#!/usr/bin/python

import requests
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

def fetch(t_id) :
    payload = {'clientcode' : '02',
               'requestType' : 'submit',
               'clientAccount' : '5',
               'actionType' : 'I',
               'ticket' : t_id,
               'submit' : 'Submit'}
    r = requests.post(url, data=payload, headers=headers)
    return r

#r = fetch("585362916")
ticket = "585362916"
#headers["Cookie"] = r.headers["set-cookie"]
for i in range(585362916, 585363016):
    r = fetch(str(i))
    soup = BeautifulSoup(r.content)
    odf = soup.find_all("form", attrs={'name':'onlineDisputeForm'})[0]
    tr = odf.table.findChildren()
    if tr[0].findChildren()[1].text.strip() == str(i):
        print "%d,%s" % (i,"true")
    else :
        print "%d,%s" % (i,"false")

