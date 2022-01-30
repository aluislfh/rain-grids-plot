import os, glob, sys
import netCDF4 as ncd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from datetime import datetime, timedelta
import h5py as h5py
from dateutil.relativedelta import relativedelta
import dateutil.parser
import time
import matplotlib as mpl


def main():

    # NC data

    rdate = '200412'

    nc1 = ncd.Dataset('stn_interp_'+rdate+'.nc')

    rain1 = nc1.variables['var'][:]
    lons1 = nc1.variables['Lon'][:]
    lats1 = nc1.variables['Lat'][:]

    map1 = Basemap(resolution='h',llcrnrlon=-61.65, llcrnrlat=0.95, urcrnrlon=-56.3, urcrnrlat=8.7)
#    map1 = Basemap(resolution='h',llcrnrlon=-62.37943, llcrnrlat=0.48004, urcrnrlon=-55.78876, urcrnrlat=9.50421, projection='cyl')


    #=====================================================================================

    fplot(map1,'cuba',lons1,lats1,rain1,rdate)


def fplot(m,label,lons1,lats1,rain1,rdate):

    # Define the latitude and longitude data
    x1, y1 = np.float32(np.meshgrid(lons1,lats1))
#    print(x1.shape,y1.shape,x2.shape,y2.shape,rain1.shape,rain2.shape,rain3.shape,rain4.shape,rain5.shape)

    # LAOD FIGURE

    cmap1,norm1,clevs1 = cm_precip()
    width = 8.03
    height = 10.125

    fig = plt.figure(1,figsize=(width,height),dpi=300)

    plt.subplots_adjust(hspace=0.1,wspace=0.1)

    plt.subplot(111)

    plt.title('RF mswep_cdt_gpcc: '.upper()+rdate, fontsize=7,bbox=dict(facecolor='white', alpha=0.65), x=0.5,y=.999,weight = 'demibold',style='oblique', stretch='normal', family='sans-serif')

    m.drawstates(color='gray', linewidth=0.25)
    m.drawcoastlines(color='k', linewidth=0.9)
    m.drawcountries(color='k', linewidth=0.9)

    m.drawmeridians(range(0, 360, 3),labels=[1,0,0,1],fontsize=8, linewidth=0)
    m.drawparallels(range(-180, 180, 3),labels=[1,0,0,1],fontsize=8, linewidth=0)

    W=m.contourf(x1, y1, rain1,clevs1,cmap=cmap1,extend="max")
    W.cmap.set_under((1.0, 1.0, 1.0))
    W.cmap.set_over((0.39,0,0.34))  #((234/255,0/255,199/255))

    cbar = m.colorbar(W,location='right')
#    ax2 = fig.add_axes([0.13, 0.02, 0.76, 0.05])
#    cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap1, spacing='uniform', ticks=clevs1[::2], boundaries=clevs1, format='%2.0f', orientation="horizontal")

    filename = 'multi_rain_plot_'+rdate+'.png'

    plt.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()



# Plot every masked value as white
def cm_precip():

    a = np.round(np.array([0.1,0.25,0.5,1,1.5,2,3,4,5,6,8,10,12,16,20,24,30,36,42,60])*12, 0)

    clevs = np.array(a)
    # Normalize the bin between 0 and 1 (uneven bins are important here)
    norm = [(float(i)-min(a))/(max(a)-min(a)) for i in a]

    C = np.array([[255,255,255],
                [0,250,76],
                [0,227,69],
                [0,203,61],
                [0,180,54],
                [0,156,47],
                [0,133,40],
                [0,109,32],
                [0,86,25],
                [254,250,79],
                [254,198,70],
                [254,146,62],
                [254,93,53],
                [254,41,44],
                [115,6,34],
                [128,5,44],
                [140,5,55],
                [180,3,110],
                [207,1,154],
                [234,0,199]])

    # Create a tuple for every color indicating the normalized position on the colormap and the assigned color.
    COLORS = []
    for i, n in enumerate(norm):
        COLORS.append((n, np.array(C[i])/255.))

    # Create the colormap
    cmap = colors.LinearSegmentedColormap.from_list("precipitation", COLORS)

    return cmap,norm,clevs


main()


