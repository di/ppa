#!/usr/bin/python

import fetch
import requests

master = "http://localhost:8080"

while True :
    resp = requests.get(master + "/missing").json() 
    print resp
    print "%s %d" % ("Trying", _id)
    data = fetch.fetch_range(resp['_id'], resp['lmn'], resp['pmn'])
    print data
    requests.put(master + "/insert_missing", data)
