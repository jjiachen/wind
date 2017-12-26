# -*- coding: utf-8 -*-
"""
Created on 6 Feb 2017
@author: JiM
a simpilfied version of Xiaojian code to plot mthly mean u&v
"""
import netCDF4
import numpy as np
#import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from utilities import get_nc_data,sh_bindata # gets our own functions
#HARDCODE
gridscale=0.02
gbox=[-70.75,-69.9,41.63,42.12] # geographic box
yr=-2 # -1 for 2013, -2 for 2012, etc
FNCL='necscoast_worldvec.dat' # NE Continental Shelf Coastline 
CL=np.genfromtxt(FNCL,names=['lon','lat'])
#get u&v from model current or wind
url='''http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3/mean?lat[0:1:48450],latc[0:1:90414],
lon[0:1:48450],lonc[0:1:90414],time[0:1:431],Times[0:1:431],uwind_stress[0:1:431][0:1:90414],vwind_stress[0:1:431][0:1:90414],
u[0:1:431][0:1:44][0:1:90414],v[0:1:431][0:1:44][0:1:90414]''' #model url
data = get_nc_data(url,'time','Times','latc','lonc','uwind_stress','vwind_stress','u','v','lon','lat')# gets data from model
lonc, latc = data['lonc'][:], data['latc'][:]  #quantity:165095 center of grids
lon, lat = data['lon'][:], data['lat'][:]  #quantity:165095 grid nodes
time, Times = data['time'][:], data['Times'][:] #model times
u = data['u']; v = data['v']; # model ocean current
uws= data['uwind_stress']; vws = data['vwind_stress']; # model
index=[]
for i in np.arange(len(Times)):
    if float(Times[i][5])==1 and float(Times[i][6])==1:
        index.append(i) #November index
uc=u[index[yr]][0][:] #surface layer 0 eastward flow
vc=v[index[yr]][0][:] #surface layer 0 northward flow
uwse=uws[index[yr]][:] #eastward windstress
vwsn=vws[index[yr]][:] #northward windstress
xi = np.arange(gbox[0],gbox[1],gridscale) #region of interest
yi = np.arange(gbox[2],gbox[3],gridscale)
xb,yb,ub_mean,ub_median,ub_std,ub_num = sh_bindata(lonc, latc, uc, xi, yi)
xb,yb,vb_mean,vb_median,vb_std,vb_num = sh_bindata(lonc, latc, vc, xi, yi)
xxb,yyb = np.meshgrid(xb, yb)
fig=plt.figure()
ax1=fig.add_subplot(211,aspect=1.3)
Q=plt.quiver(xxb,yyb,ub_mean.T,vb_mean.T,scale=3.)#current vectors
qk=plt.quiverkey(Q,0.7,0.12,.1, r'$.1m/s$', fontproperties={'weight': 'bold'})
ax1.plot(CL['lon'],CL['lat'])
ax1.set_xlim([gbox[0],gbox[1]])
ax1.set_ylim([gbox[2],gbox[3]])
ax1.set_title(str(2014+yr)+' mean surface current')
ax1.set_xticklabels('',visible=False) # shut off xticklabels
xb,yb,uw_mean,uw_median,uw_std,uw_num = sh_bindata(lonc, latc, uwse, xi, yi)
xb,yb,vw_mean,vw_median,vw_std,vw_num = sh_bindata(lonc, latc, vwsn, xi, yi)
ax2=fig.add_subplot(212,aspect=1.3)
Q=plt.quiver(xxb,yyb,uw_mean.T,vw_mean.T,scale=3.)# wind stress vectors
qk=plt.quiverkey(Q,0.7,0.12,.1, r'$.1Pa$', fontproperties={'weight': 'bold'})
ax2.plot(CL['lon'],CL['lat'])
ax2.set_xlim([gbox[0],gbox[1]])
ax2.set_ylim([gbox[2],gbox[3]])
ax2.set_title(str(2014+yr)+' mean wind stress')
plt.show()

