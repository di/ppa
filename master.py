#!/usr/bin/python

import fetch
import json
import sys
from bottle import route, run, request#, response, abort, template, redirect
from daemon import Daemon
from pymongo import MongoClient
from datetime import datetime

class Master :

    db = None
    min_id = None
    max_id = None
    mins = None

    def __init__(self) :
        self.db = MongoClient().ppa.ticket
        #self.min_id = self.db.find().sort([('_id', 1)]).limit(1)[0]['_id'] - 1
        #self.max_id = self.db.find().sort([('_id', -1)]).limit(1)[0]['_id'] + 1
        self.min_id = 58536288
        self.max_id = 58536288
        self.mins = True
        print "%s: %d" % ("Next max", self.max_id)
        print "%s: %d" % ("Next min", self.min_id)

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
        self.db.save(entity)

    def placeholder(self, _id) :
        try :
            self.db.insert({'_id':int(_id),'placeholder':True})
        except DuplicateKeyError :
            print "Already inserted this one..."

    def next_id(self):
        if self.mins:
            self.mins = False
            while m.db.find({'_id':self.min_id}).count() :
                self.min_id = self.min_id - 1
            return self.min_id
        else:
            self.mins = True
            while m.db.find({'_id':self.max_id}).count() :
                self.max_id = self.max_id + 1
            return self.max_id

@route('/new', method='GET')
def get_new_id():
    next_id = m.next_id()
    m.placeholder(next_id)
    return {'_id': next_id}

@route('/insert', method='PUT')
def insert():
    data = request.forms
    m.insert(data)

if __name__ == '__main__':
    m = Master()
    run(host='129.25.163.19', port=80)
