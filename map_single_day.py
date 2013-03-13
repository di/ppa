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

def _get_colors(num_colors):
    colors=[]
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = np.random.rand()
        if lightness < .25 :
            lightness += .25
        saturation = np.random.rand()
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

db = MongoClient().ppa

lats = []
lons = []
agents = {}

for loc in db.ticket.find({'issueDate':'01/31/2013'}):
    ll = db.location.find_one({'text':fetch.make_nice(loc['location'])})
    #lats.append(ll['location']['lat'])
    #lons.append(ll['location']['lng'])
    _id = int(loc['_id'])
    uniq = _id - (_id % 200)
    if uniq not in agents :
        agents[uniq] = {'lats':[],'lons':[]}
    agents[uniq]['lats'].append(ll['location']['lat'])
    agents[uniq]['lons'].append(ll['location']['lng'])

lat_min = 39.859682 # sorted(lats)[0]   #bottom
lat_max = 40.14319 #sorted(lats)[-4]  #top
lon_min = -75.291367 #sorted(lons)[10]   #left
lon_max = -74.95491 #sorted(lons)[-1]  #right

spatial_resolution = 0.5
fig = plt.figure()

m = Basemap(
    projection = 'merc',
    llcrnrlat=lat_min, urcrnrlat=lat_max,
    llcrnrlon=lon_min, urcrnrlon=lon_max,
    rsphere=6371200, resolution='l', area_thresh=10000
)

colors = _get_colors(len(agents))

subplot(111, axisbg='black')
for i,agent in enumerate(agents.values()) :
    x,y = m(agent['lons'], agent['lats'])
    m.plot(x,y,marker='.',
        markersize=2.0,
        markerfacecolor=colors[i],
        markeredgecolor=colors[i],
        linestyle='None' )

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5,10.5)
plt.savefig('figures/myfig.png', facecolor='black', dpi=300, bbox_inches='tight', pad_inches=0, alpha=1)
