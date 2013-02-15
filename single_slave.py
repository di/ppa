#!/usr/bin/python

import fetch
import requests
import sys

master = "http://129.25.163.19:8080"

data = fetch.fetch_range(int(sys.argv[1]))
print data
requests.put(master + "/insert", data)
