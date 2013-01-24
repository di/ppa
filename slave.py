#!/usr/bin/python

import fetch
import requests

master = "http://129.25.163.19"

def new() :
    resp = requests.get(master + "/new").json() 
    print resp
    lmn = resp['lmn']
    if lmn is None :
        return resp['_id'], None 
    else :
        return resp['_id'], int(resp['lmn'])

def insert(data):
    requests.put(master + "/insert", data)

while True :
    _id,lmn = new()
    print "%s %d" % ("Trying", _id)
    data = fetch.fetch_range(_id, lmn)
    print data
    insert(data)
