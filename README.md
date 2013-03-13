# PPA (Philadelphia Parking Authority)
This repo is a set of scripts for scraping parking ticket data from the
Philadelphia Parking Authority website. I have yet to find a good use for it.

## Setup
The following Python modules are required:

    $ easy_install pymongo
    $ easy_install requests
    $ easy_install bottle
    $ easy_install beautifulsoup4

## Importing the database
From the same directory as this README:

    $ mongorestore

This creates one database, `ppa`, with two collections:

### `ticket`
Example of an unresolved ticket:

    {
        "_id" : 58536252,
        "magic-num" : 8,
        "issueDate" : "01/18/2013",
        "time" : "11:37PM",
        "issueTime" : ISODate("2013-01-18T23:37:00Z"),
        "location" : "400 BLK N 7TH ST ES",
        "meterNumber" : "7828215",
        "plate" : "PAGNF5261",
        "resolved" : false,
        "valid" : true,
        "violation" : "METER EXPIRED CC",
        "violationCode" : "1210051  C"
    }

Example of a resolved ticket:

    {
        "_id" : 58536710,
        "magic-num" : "5"
        "resolved" : true,
    }

The actual PPA ticket number consists of a consecutive 8-digit number, followed
by a "magic" digit, for which there is a semi-predictable pattern.

### `location`
Locations are geocoded using the Google Geocoding API.

Example of a location:

    {
        "_id" : ObjectId("510afb526f9bdd39b0bc3567"),
        "checked" : true,
        "distance" : 2.9851718406691896,
        "location" : {
            "lat" : 39.9601501,
            "lng" : -75.1971039
        },
        "text" : "3800 LANCASTER AV PHILADELPHIA PA"
    }

Here, `distance` is the distance from this point to City Hall, and is used to
filter out bad geolocations.

## Collecting more data
The system is set up so that the "master" interacts with the DB and receives
RESTful calls from any number of "slaves", which can operate on different
machines. This was done to pre-empt any IP blocking, which did not occur.

    $ ./master.py
    $ ./slave.py

The PPA website is frail, however, and currently cannot handle more than one or
two slaves simultaneously before it goes down. The slaves are rate-limited to
give the site enough breathing room to handle one or two of them. It is *not*
recommended to run more than two slaves.

You can request the data for a specific 8-digit ticket ID using the
single_slave command-line utility:

    $ ./single_slave 58536710

## Geocoding
The "master" does not geocode automatically. This is because the Google
Geocoding API rate-limits geocoding requests, as well as having a daily limit
on the number of requests (2500). In order to play nice, geocoding is done as a
separate function. Simply:

    $ ./geocode.py

## Note
If you fork this repo and produce additional ticket data, please submit a patch
to push a new dump back.

