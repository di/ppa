#!/usr/bin/python

import fetch
import requests
import sys

master = "http://129.25.163.19"

_id = int(sys.argv[1])
print "%s %d" % ("Trying", _id)
data = fetch.fetch_range(_id)
print data
requests.put(master + "/insert", data)
