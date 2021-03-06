#!/usr/bin/python

import sys
import fetch
import requests

master = "http://localhost:8080"

while True :
    try :
        resp = requests.get(master + "/missing").json() 
        print resp
        print "%s %d" % ("Trying", resp['_id'])
        data = fetch.fetch_range(resp['_id'], resp['lmn'], resp['pmn'])
        print data
        requests.put(master + "/insert_missing", data)
    except requests.exceptions.ConnectionError :
        print "It seems like the master is not running. Exiting."
        sys.exit(1)
