#!/usr/bin/python

import fetch
import requests
import sys

master = "http://129.25.163.19"

_id = sys.argv[1]
num = int(_id[:8])
mnum = int(_id[-1])
print "%s %d-%d" % ("Trying", num, mnum)
valid, data = fetch.fetch(num, mnum)
print data
requests.put(master + "/insert", data)
