#!/usr/bin/python

import fetch
import requests

master = "http://129.25.163.19:8080"

def new() :
    resp = requests.get(master + "/missing").json() 
    print resp
    return resp['_id'], resp['lmn'], resp['pmn']

def insert(data):
    requests.put(master + "/insert_missing", data)

while True :
    _id,lmn,pmn = new()
    print "%s %d" % ("Trying", _id)
    data = fetch.fetch_range(_id, lmn, pmn)
    print data
    insert(data)
