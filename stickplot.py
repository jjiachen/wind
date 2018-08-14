# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:11:02 2017
To run rhis program,you need these following inputfile:
'wind_time_v.npy'
'wind_u.npy'
'wind_v.npy'
you can find in the 'wind'
@author: hxu
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num,DateFormatter,WeekdayLocator,DayLocator, MONDAY

year=2014
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
        fig, ax = plt.subplots(figsize=(15,3.5))
    
    q = ax.quiver(date2num(time), [[0]*len(time)], u, v,
                  angles='uv', width=width, headwidth=headwidth,
                  headlength=headlength, headaxislength=headaxislength,
                  **kw)

    ax.axes.get_yaxis().set_visible(False)
    mondays = WeekdayLocator(MONDAY)
    ax.xaxis.set_major_locator(mondays)
    weekFormatter = DateFormatter('%b %d %Y')
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(weekFormatter)
    return q
wind_time=np.load('wind_time_v.npy')
wind_u=np.load('wind_u.npy')
wind_v=np.load('wind_v.npy')
stick_plot(wind_time,wind_u,wind_v,color='green')
plt.xticks(rotation=10)
plt.savefig('stickplot'+str(year),dpi=100)
