# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 15:07:52 2017

@author: huimin
"""
import numpy as np
from datetime import datetime as dt
from datetime import timedelta as td
import netCDF4
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

year=2014
latp=41.9
lonp=-70.3
datet=[dt(2014,11,1),dt(2014,12,1)]
option='one month' #'all year' or 'one time' or 'one month'
def stick_plot(time, u, v, **kw):
    width = kw.pop('width', 0.002)
    headwidth = kw.pop('headwidth', 0)
    headlength = kw.pop('headlength', 0)
    headaxislength = kw.pop('headaxislength', 0)
    angles = kw.pop('angles', 'uv')
    ax = kw.pop('ax', None)
    
    if angles != 'uv':
        raise AssertionError("Stickplot angles must be 'uv' so that"
                             "if *U*==*V* the angle of the arrow on"
                             "the plot is 45 degrees CCW from the *x*-axis.")

    time, u, v = map(np.asanyarray, (time, u, v))
    if not ax:
        fig, ax = plt.subplots(figsize=(15,3))
    
    q = ax.quiver(date2num(time), [[0]*len(time)], u, v,
                  angles='uv', width=width, headwidth=headwidth,
                  headlength=headlength, headaxislength=headaxislength,
                  **kw)

    ax.axes.get_yaxis().set_visible(False)
    ax.xaxis_date()
    return q
    
url_v='/home/hxu/huiminzou/wind/vwnd.sig995.'+str(year)+'.nc'#?vwnd,lat,lon,time' # where I downloaded these from ftp://ftp.cdc.noaa.gov/Datasets/ncep.reanalysis/surface/
url_u='/home/hxu/huiminzou/wind/uwnd.sig995.'+str(year)+'.nc'#?uwnd'
ncv=netCDF4.Dataset(url_v)
ncu=netCDF4.Dataset(url_u)
lat=ncv['lat'][:]
lon=ncv['lon'][:]
# find the node of interest
lat_i = list(np.arange(len(lat[0:])))
lat_i.reverse()
lat = list(lat[0:])
lat.reverse()
lon = list(lon[0:] - 360)
lon_i = list(np.arange(len(lon[0:])))
idlat = int(round(np.interp(latp,lat,lat_i)))
idlon = int(round(np.interp(lonp,lon,lon_i)))
# find the time index where there are estimates every 6 hours
t=ncv['time'][:]
moddate=[]
for k in range(len(t)):
  moddate.append(dt(year,1,1,0,0,0)+td(hours=t[k]-t[0]))
  # datearray = np.array(pd.date_range(dt(year,1,1,0,0,0),freq='6H',periods=len(t)).tolist())
  # vitalii's way as follows:
  # datearray = np.arange(dt(year,1,1,0,0,0),dt(year,1,1,0,0,0)+td(hours=len(t)*4),td(hours=6)).astype(dt)
if option=='one time':   
    iddate=np.argmin(abs(np.array(moddate)-datet))
    uw=ncu['uwnd']
    u=uw[iddate,idlat,idlon]
    vw=ncv['vwnd']
    v=vw[iddate,idlat,idlon]
    print t[iddate]
elif option=='one month':
    u=[]
    v=[]
    datearray = np.arange(datet[0],datet[1],td(hours=6)).astype(dt)
    iddate=[]
    for i in range(len(datearray)):
        iddate.append(np.argmin(abs(np.array(moddate)-datearray[i])))    
    for j in range(len(iddate)):       
        uw=ncu['uwnd']
        u.append(uw[iddate[j],idlat,idlon])
        vw=ncv['vwnd']
        v.append(vw[iddate[j],idlat,idlon])
elif option=='all year':
    uw=ncu['uwnd']
    u=uw[:,idlat,idlon]
    vw=ncv['vwnd']
    v=vw[:,idlat,idlon]
#u=np.load('uwind_stress201411_1_30.npy')
#v=np.load('vwind_stress201411_1_30.npy')
stick_plot(datearray,u,v,color='green')
plt.xticks(rotation=10)
plt.savefig('stickplot20141',dpi=100)