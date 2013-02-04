#!/usr/bin/python

import fetch
import json
import sys
from bottle import route, run, request#, response, abort, template, redirect
from daemon import Daemon
from pymongo import MongoClient
from datetime import datetime,timedelta

class Master :

    db = None
    min_id = None
    max_id = None
    mins = None

    def __init__(self) :
        self.db = MongoClient().ppa
        self.starter = None
        if len(sys.argv) == 2 :
            self.starter = int(sys.argv[1]) - 1
        else :
            try :
                self.starter = int(self.db.ticket.find({'placeholder':True}).sort([('_id',1)]).limit(1)[0]['_id']) - 1
                print "Using placeholder"
            except :
                print "No placeholder, no arg. Please provide a start number"
                sys.exit(1)
        #self.min_id = self.db.ticket.find().sort([('_id', 1)]).limit(1)[0]['_id'] - 1
        #self.max_id = self.db.ticket.find().sort([('_id', -1)]).limit(1)[0]['_id'] + 1
        self.min_id = 58536288
        self.max_id = 58536803 # max as of 1/23 6PM
        self.mins = True

        self.i = ((self.starter % 1000) % 200)
        self.start = self.starter - self.i
        print "%s: %d" % ("Next ID", self.start + self.i + 1)
        print "%s: %d" % ("Start", self.start)
        print "%s: %d" % ("i", self.i)
        self.miss_count = 0

        #self.db.ticket.remove({'placeholder':True})
#        print "%s: %d" % ("Next max", self.max_id)
#        print "%s: %d" % ("Next min", self.min_id)

    def insert(self, data) :
        print "%s %s" % ("Inserting", data['_id'])
        entity = dict()
        for field in data.keys() :
            entity[field] = data.get(field)
        entity['_id'] = int(entity['_id'])
        try :
            resolved = entity['resolved'] == 'True'
            entity['resolved'] = resolved
            if not resolved:
                entity['magic-num'] = int(entity['magic-num'])
                issueTime = entity['issueDate'] + " " + entity['time']
                entity['issueTime'] = datetime.strptime(issueTime, "%m/%d/%Y %I:%M%p")
        except KeyError :
            entity['missing'] = entity['missing'] == 'True'
        except ValueError :
            entity['issueTime'] = False
        self.db.ticket.save(entity)
        try :
            togeo = {'location':entity['location']}
            self.db.togeo.save(togeo)
        except KeyError :
            pass

    def set_placeholder(self, _id) :
        try :
            self.db.ticket.insert({'_id':int(_id),'placeholder':True})
        except :
            print "Already inserted this one..."

    def next_id(self):
        if self.i < 200 :
            self.i = self.i + 1
            return self.i + self.start
        else :
            self.i = 1
            self.start = self.start + 200
            self.miss_count = 0
            return self.i + self.start

    def missing_id(self):
        _id = int(self.db.ticket.find({'$or':[{'missing':True,'checks':{'$gte':0},'checked':{'$lte':datetime.now()-timedelta(hours=24)}},{'placeholder':True}]}).sort([('_id',1)]).limit(1)[0]['_id'])
        return _id

    def clear_missing(self):
        self.miss_count = 0

    def found_missing(self):
        self.miss_count = self.miss_count + 1
        if self.miss_count >= 5 :
            print "Found 5 missing, leaving this block"
            self.miss_count = 0
            self.i = 0
            self.start = self.start + 200
            return True
        return False

    ''' # Using min/max
        if self.mins:
            while m.db.find({'_id':self.min_id}).count() :
                self.min_id = self.min_id - 1
            return self.min_id
        else:
            while m.db.find({'_id':self.max_id}).count() :
                self.max_id = self.max_id + 1
            return self.max_id
    '''
    def has_non_missing_following(self, _id) :
        return self.db.ticket.find({'_id':_id+1, 'missing':{'$exists':False},'placeholder':{'$exists':False}}).count() or self.db.ticket.find({'_id':_id+1, 'checks':-1}).count()

    def mark_permanently_missing(self, _id) :
        print "%s: %d" % ("Permanently missing", _id)
        self.db.ticket.update({'_id':_id},{'$set':{'checked':datetime.now(),'checks':-1},'$unset':{'placeholder':1}})

    def has_following(self, next_id) :
        return self.db.ticket.find({'_id':next_id+1, 'placeholder':{'$exists':False}}).count()

    def has_preceding(self, next_id) :
        return self.db.ticket.find({'_id':next_id-1, 'placeholder':{'$exists':False}}).count()

    def get_lmn(self, next_id) :
        if self.has_following(next_id) :
            try :
                return self.db.ticket.find({'_id':next_id+1})[0]['magic-num']
            except :
                return None
        else :
            return None

    def get_pmn(self, next_id) :
        if self.has_preceding(next_id) :
            try :
                return self.db.ticket.find({'_id':next_id-1})[0]['magic-num']
            except :
                return None
        else :
            return None

@route('/new', method='GET')
def get_new_id():
    next_id = m.next_id()
    m.set_placeholder(next_id)
    return {'_id': next_id,
            'lmn': m.get_lmn(next_id),
            'pmn': m.get_pmn(next_id)
            }

@route('/missing', method='GET')
def get_missing_id():
    missing_id = m.missing_id()
    print "%s: %d" % ("Serving missing id", missing_id)
    while m.has_non_missing_following(missing_id) :
        m.mark_permanently_missing(missing_id)
        missing_id = m.missing_id()
    return {'_id': missing_id,
            'lmn': m.get_lmn(missing_id),
            'pmn': m.get_pmn(missing_id)
            }

@route('/insert_missing', method='PUT')
def insert():
    data = request.forms
    _id = int(data['_id'])
    skip = False
    # We got a result back, and it's still missing
    if data.get('missing', False) :
        print "%s: %d (%d)" % ("Still missing", _id, m.miss_count)
        m.db.ticket.update({'_id':_id}, {'$inc':{'checks':1},'$set':{'checked':datetime.now(),'missing':True},'$unset':{'placeholder':1}})
        skip = m.found_missing()
    # We got a result back, and we found it
    else :
        m.insert(data)
        m.clear_missing()

    if skip : # We're skipping, so clear the missing counter
        m.clear_missing()
    else : # We're not skipping
        # Nothing behind it
        if not m.has_following(_id):
            m.set_placeholder(_id + 1)

@route('/insert', method='PUT')
def insert():
    data = request.forms
    try :
        if data['missing'] :
            m.found_missing()
    except :
        m.clear_missing()
    m.insert(data)

if __name__ == '__main__':
    m = Master()
    run(host='129.25.163.19', port=8080)
