#!/usr/bin/python

import requests
import re
import sys
import time
import math
from pymongo import MongoClient

db = MongoClient().ppa

def geocode(location) :
    api_url = "http://maps.googleapis.com/maps/api/geocode/json"
    payload = {'address': location, 'sensor': 'false'}
    r = requests.get(api_url, params=payload)
    return r.json()

def distance(lat, lon) :
    c_lat = 39.952385
    c_lon = -75.163578
    c_lat_rad = math.radians(c_lat)
    dLat = math.radians(c_lat-lat)
    dLon = math.radians(c_lon-lon)
    lat_rad = math.radians(lat)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat_rad) * math.cos(c_lat_rad)
    return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

i = 0
for location in db.location.find({'checked':False}) :
    if i >= 2500 :
        print "Daily limit reached"
        sys.exit(1)
    text = location['text']
    r = geocode(location['text'])
    i += 1
    if r['status'] == "OK" :
        ll = r['results'][0]['geometry']['location']
        d = distance(ll['lat'], ll['lng'])
        db.location.update({'text':text},{'$set':{'location':ll, 'checked':True, 'distance':d}})
        print "%s\n =>\t%s" % (text, ll)
        time.sleep(0.2)
    elif r['status'] == 'ZERO_RESULTS' :
        print "ZERO RESULTS"
        print text
    else :
        print "Bad status code: " + r['status']
        print "%s = %d" % ("i", i)
        print r
        sys.exit(1)
