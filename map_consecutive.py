#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from pylab import *
from pymongo import MongoClient
import sys
import fetch
import colorsys
from datetime import timedelta

db = MongoClient().ppa

lat_min = 39.859682 # sorted(lats)[0]   #bottom
lat_max = 40.14319 #sorted(lats)[-4]  #top
lon_min = -75.291367 #sorted(lons)[10]   #left
lon_max = -74.95491 #sorted(lons)[-1]  #right

m = Basemap(
    projection = 'merc',
    llcrnrlat=lat_min, urcrnrlat=lat_max,
    llcrnrlon=lon_min, urcrnrlon=lon_max,
    rsphere=6371200, resolution='l', area_thresh=10000
)
subplot(111, axisbg='black')

for loc in db.ticket.find({'resolved':False}):
    next_one = db.ticket.find_one({'_id': loc['_id'] + 1})
    if next_one != None and (not next_one.get('resolved',True) or not next_one.get('missing',True)):
        try :
            diff = next_one['issueTime'] - loc['issueTime'] 
            if diff == 0 or diff < timedelta(minutes=30):
                try :
                    ll1 = db.location.find_one({'text':fetch.make_nice(loc['location'])})['location']
                    ll2 = db.location.find_one({'text':fetch.make_nice(next_one['location'])})['location']
                    x,y = m([ll1['lng'],ll2['lng']], [ll1['lat'],ll2['lat']])
                    m.plot(x,y,',w-', linewidth=.2, alpha=.3)
                except :
                    pass # Geocoding missing, or placeholder
        except :
            print next_one, loc

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5,10.5)
plt.savefig('figures/myfig.png', facecolor='black', dpi=300, bbox_inches='tight', pad_inches=0, alpha=1)
