#!/usr/bin/python

from pymongo import MongoClient

db = MongoClient().ppa

locs = open('location.csv', 'a')
locs.write("_id,text,distance,checked,lat,lng\n")
for loc in db.location.find():
    locs.write(
        "%s,%s,%s,%s,%f,%f\n" %
        (loc["_id"],
         loc["text"],
         loc["distance"],
         loc['checked'],
         loc['location']['lat'],
         loc['location']['lng']))

tics = open('ticket.csv', 'a')
tics.write(
    "_id,resolved,magic-num,plate,violationCode,violation,issueTime,valid,location,time,issueDate,meterNumber\n")
for tic in db.ticket.find():
    try:
        if tic['resolved']:
            tics.write(
                ("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n") %
                (tic['_id'],
                 tic['resolved'],
                    tic['magic-num'],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''))
        else:
            tics.write(
                ("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n") %
                (tic['_id'],
                 tic['resolved'],
                    tic['magic-num'],
                    tic['plate'],
                    tic['violationCode'],
                    tic['violation'],
                    tic['issueTime'],
                    tic['valid'],
                    tic['location'],
                    tic['time'],
                    tic['issueDate'],
                    tic['meterNumber']))
    except KeyError:
        pass
