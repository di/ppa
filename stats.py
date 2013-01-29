#!/usr/bin/python

import fetch
import sys
from pymongo import MongoClient

db = MongoClient().ppa.ticket
min_id = db.find().sort([('_id', 1)]).limit(1)[0]['_id'] - 1
max_id = db.find().sort([('_id', -1)]).limit(1)[0]['_id'] + 1
i = (min_id % 1000) % 200
block_start = min_id - i + 1

_total = 0
_resolved = 0
_unresolved = 0
_missing = 0

while block_start < max_id :
    block_end = block_start + 199
    total = db.find({'_id':{'$gte':block_start, '$lte':block_end}}).count()
    try :
        start_date = db.find({'_id':{'$gte':block_start,'$lte':block_end},'issueTime':{'$exists':True}}).sort([('_id', 1)]).limit(1)[0]['issueTime']
    except :
        start_date = "???"
    try :
        end_date = db.find({'_id':{'$gte':block_start,'$lte':block_end},'issueTime':{'$exists':True}}).sort([('_id', -1)]).limit(1)[0]['issueTime']
    except :
        end_date = "???"
    resolved = db.find({'_id':{'$gte':block_start,'$lte':block_end},'resolved':True}).count()
    unresolved = db.find({'_id':{'$gte':block_start,'$lte':block_end},'resolved':False}).count()
    missing = db.find({'_id':{'$gte':block_start,'$lte':block_end},'missing':True}).count()
    if True:
        print "%s: %d-%d" % ("Range", block_start, block_end)
        print "\t%s:\t\t%s" % ("Start", start_date)
        print "\t%s:\t\t%s" % ("End", end_date)
        print "\t%s:\t%d" % ("Resolved", resolved)
        print "\t%s:\t%d" % ("Unresolved", unresolved)
        print "\t%s:\t%d" % ("Missing", missing)
        print "\t%s:\t\t%d" % ("Total", total)
    block_start += 200
    _total += total
    _resolved += resolved
    _unresolved += unresolved
    _missing += missing
print "*************"
print "%s:\t%d" % ("Resolved", _resolved)
print "%s:\t%d" % ("Unresolved", _unresolved)
print "%s:\t%d" % ("Missing", _missing)
print "%s:\t\t%d" % ("Total", _total)


