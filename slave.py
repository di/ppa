#!/usr/bin/python

import fetch
import requests

master = "http://129.25.163.19"

def new() :
    return requests.get(master + "/new").json()['_id']

def insert(data):
    requests.put(master + "/insert", data)

while True :
    _id = new()
    print "%s %d" % ("Trying", _id)
    data = fetch.fetch_range(_id)
    print data
    insert(data)
