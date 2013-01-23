#!/usr/bin/python

from pymongo import MongoClient
col = MongoClient().ppa.ticket

import fetch

def insert(data) :
    print data
    col.insert(data)


#insert(fetch.fetch_range(58536292)) #6
#insert(fetch.fetch_range(58536293)) #resolved

